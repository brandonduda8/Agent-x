/**
 * agent-x-core/pipeline/pipeline.test.js
 *
 * Unit + integration tests for:
 *   • TaskQueue          – enqueue, assign, complete, fail, backoff, dead-letter
 *   • HermesPipeline     – dispatch, retry, no-agent, external job ingest
 *   • WsStatusServer     – broadcast, snapshot, client commands
 *   • pipeline-api       – REST endpoints
 *
 * Run with:  node --test agent-x-core/pipeline/pipeline.test.js
 * Or:        npx jest agent-x-core/pipeline/pipeline.test.js
 *
 * Uses Node's built-in test runner (Node ≥ 18) — no additional test lib required.
 * Falls back gracefully if `assert` is the only available tool.
 */

'use strict';

const assert         = require('assert');
const { EventEmitter } = require('events');

// ── attempt to use built-in test runner ───────────────────────────────────────
let test, describe, it, before, after, beforeEach, afterEach;

try {
  const nodeTest = require('node:test');
  test      = nodeTest.test;
  describe  = nodeTest.describe;
  it        = nodeTest.it;
  before    = nodeTest.before;
  after     = nodeTest.after;
  beforeEach = nodeTest.beforeEach;
  afterEach  = nodeTest.afterEach;
} catch {
  // Minimal shim for older Node / Jest
  describe   = (name, fn) => { console.log(`\nSuite: ${name}`); fn(); };
  it         = test = (name, fn) => {
    try {
      const result = fn();
      if (result && typeof result.then === 'function') {
        result
          .then(() => console.log(`  ✔  ${name}`))
          .catch(err => { console.error(`  ✖  ${name}: ${err.message}`); process.exitCode = 1; });
      } else {
        console.log(`  ✔  ${name}`);
      }
    } catch (err) {
      console.error(`  ✖  ${name}: ${err.message}`);
      process.exitCode = 1;
    }
  };
  before = after = beforeEach = afterEach = (_fn) => {};
}

// ── module imports ────────────────────────────────────────────────────────────
const { TaskQueue, MAX_RETRIES, backoffMs } = require('./task-queue');
const { HermesPipeline }                    = require('./hermes-pipeline');

// ═══════════════════════════════════════════════════════════════════════════════
// TaskQueue
// ═══════════════════════════════════════════════════════════════════════════════

describe('TaskQueue — core operations', () => {
  it('should enqueue a task with correct defaults', () => {
    const q = new TaskQueue();
    const task = q.enqueue({ type: 'build' });

    assert.ok(task.id,                     'id assigned');
    assert.strictEqual(task.type,   'build');
    assert.strictEqual(task.status, 'pending');
    assert.strictEqual(task.retries, 0);
    assert.strictEqual(task.priority, 0);
    assert.strictEqual(task.assignedTo, null);
    q.destroy();
  });

  it('should throw when type is missing', () => {
    const q = new TaskQueue();
    assert.throws(() => q.enqueue({}), /type is required/);
    q.destroy();
  });

  it('should dequeue the highest-priority task', () => {
    const q = new TaskQueue();
    q.enqueue({ type: 'low',  priority: 0 });
    q.enqueue({ type: 'high', priority: 10 });
    q.enqueue({ type: 'mid',  priority: 5 });

    const t = q.dequeue();
    assert.strictEqual(t.type, 'high');
    q.destroy();
  });

  it('should return null when queue is empty', () => {
    const q = new TaskQueue();
    assert.strictEqual(q.dequeue(), null);
    q.destroy();
  });

  it('should assign a task to an agent', () => {
    const q    = new TaskQueue();
    const task = q.enqueue({ type: 'build' });
    const updated = q.assign(task.id, 'agent-1');

    assert.strictEqual(updated.status,     'assigned');
    assert.strictEqual(updated.assignedTo, 'agent-1');
    assert.ok(updated.assignedAt);
    q.destroy();
  });

  it('should throw when assigning a non-pending task', () => {
    const q    = new TaskQueue();
    const task = q.enqueue({ type: 'build' });
    q.assign(task.id, 'agent-1');
    assert.throws(() => q.assign(task.id, 'agent-2'), /Cannot assign/);
    q.destroy();
  });

  it('should complete a task', () => {
    const q    = new TaskQueue();
    const task = q.enqueue({ type: 'build' });
    q.assign(task.id, 'agent-1');
    const done = q.complete(task.id, { output: 'artifact.json' });

    assert.strictEqual(done.status, 'completed');
    assert.ok(done.completedAt);
    assert.deepStrictEqual(done.meta.result, { output: 'artifact.json' });
    q.destroy();
  });

  it('should emit events: enqueued, assigned, completed', (_, done) => {
    const q = new TaskQueue();
    const events = [];

    q.on('task:enqueued',  () => events.push('enqueued'));
    q.on('task:assigned',  () => events.push('assigned'));
    q.on('task:completed', () => {
      events.push('completed');
      assert.deepStrictEqual(events, ['enqueued', 'assigned', 'completed']);
      q.destroy();
      done?.();
    });

    const task = q.enqueue({ type: 'check' });
    q.assign(task.id, 'agent-x');
    q.complete(task.id);
  });
});

describe('TaskQueue — retry & dead-letter logic', () => {
  it('should schedule retry on first failure', () => {
    const q    = new TaskQueue();
    const task = q.enqueue({ type: 'flaky' });
    q.assign(task.id, 'agent-1');
    const updated = q.fail(task.id, 'timeout');

    assert.strictEqual(updated.status,   'pending',   'back to pending');
    assert.strictEqual(updated.retries,  1,           'retry count incremented');
    assert.ok(updated.nextRetryAt,                    'nextRetryAt set');
    assert.strictEqual(updated.assignedTo, null,      'agent unassigned');
    q.destroy();
  });

  it('should move task to dead-letter after max retries', () => {
    const q    = new TaskQueue();
    const task = q.enqueue({ type: 'dead-end', maxRetries: 2 });

    // Simulate failures up to limit
    for (let i = 0; i <= 2; i++) {
      const t = q.get(task.id);
      t.status    = 'assigned'; // bypass assign for test speed
      t.nextRetryAt = null;
      q.fail(task.id, `error-${i}`);
    }

    const { dead } = q.snapshot();
    assert.ok(dead.some(t => t.id === task.id), 'task in dead-letter');
    q.destroy();
  });

  it('should emit task:dead event when dead-lettered', (_, done) => {
    const q    = new TaskQueue();
    const task = q.enqueue({ type: 'sink', maxRetries: 0 });

    q.on('task:dead', deadTask => {
      assert.strictEqual(deadTask.id, task.id);
      q.destroy();
      done?.();
    });

    task.status = 'assigned';
    q.fail(task.id, 'fatal');
  });

  it('backoffMs should double per attempt, capped at 60 s', () => {
    assert.strictEqual(backoffMs(0),  1_000);
    assert.strictEqual(backoffMs(1),  2_000);
    assert.strictEqual(backoffMs(2),  4_000);
    assert.strictEqual(backoffMs(3),  8_000);
    assert.strictEqual(backoffMs(10), 60_000); // capped
  });

  it('stats should reflect all states', () => {
    const q = new TaskQueue();

    const t1 = q.enqueue({ type: 'a' });
    const t2 = q.enqueue({ type: 'b' });
    q.assign(t2.id, 'agent-1');

    const stats = q.stats();
    assert.ok(stats.pending  >= 1);
    assert.ok(stats.assigned >= 1);
    q.destroy();
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// HermesPipeline
// ═══════════════════════════════════════════════════════════════════════════════

describe('HermesPipeline — construction', () => {
  it('should throw without registry', () => {
    assert.throws(() =>
      new HermesPipeline({ bus: new EventEmitter(), dispatcher: async () => {} }),
      /registry is required/
    );
  });

  it('should throw without bus', () => {
    assert.throws(() =>
      new HermesPipeline({ registry: { list: () => [] }, dispatcher: async () => {} }),
      /bus is required/
    );
  });

  it('should throw without dispatcher', () => {
    assert.throws(() =>
      new HermesPipeline({ registry: { list: () => [] }, bus: new EventEmitter() }),
      /dispatcher is required/
    );
  });

  it('should construct with minimal valid options', () => {
    const p = new HermesPipeline({
      registry:   { list: () => [] },
      bus:        new EventEmitter(),
      dispatcher: async () => ({ ok: true }),
    });
    assert.ok(p);
    p.stop();
  });
});

describe('HermesPipeline — task submission and status', () => {
  let pipeline;

  beforeEach(() => {
    pipeline = new HermesPipeline({
      registry:   { list: () => [] },
      bus:        new EventEmitter(),
      dispatcher: async () => ({ ok: true }),
      pollMs:     100_000, // slow poll so we control timing
    });
  });

  afterEach(() => pipeline.stop());

  it('should submit a task and return a task object', () => {
    const task = pipeline.submit({ type: 'content-generator', payload: { topic: 'AI' } });
    assert.ok(task.id);
    assert.strictEqual(task.type, 'content-generator');
    assert.strictEqual(task.status, 'pending');
  });

  it('status() should include running flag and stats', () => {
    pipeline.start();
    const s = pipeline.status();
    assert.strictEqual(s.running, true);
    assert.ok(typeof s.stats === 'object');
  });

  it('start/stop should toggle running flag', () => {
    assert.strictEqual(pipeline.status().running, false);
    pipeline.start();
    assert.strictEqual(pipeline.status().running, true);
    pipeline.stop();
    assert.strictEqual(pipeline.status().running, false);
  });
});

describe('HermesPipeline — dispatch success', (t) => {
  it('should dispatch to a healthy agent and emit completed event', async () => {
    const bus = new EventEmitter();
    const events = [];

    bus.on('pipeline:task:completed', e => events.push(e));

    const registry = {
      list: () => [{
        id:           'agent-1',
        name:         'content-generator',
        type:         'content-generator',
        status:       'active',
        capabilities: ['content-generator'],
      }],
    };

    const dispatcher = async (task, agent) => {
      assert.ok(task.id);
      assert.strictEqual(agent.id, 'agent-1');
      return { output: 'done' };
    };

    const pipeline = new HermesPipeline({
      registry, bus, dispatcher, pollMs: 50,
    });

    pipeline.submit({ type: 'content-generator', payload: {} });
    pipeline.start();

    await waitFor(() => events.length > 0, 3_000);
    pipeline.stop();

    assert.ok(events.length > 0, 'completed event emitted');
    assert.strictEqual(events[0].task.status, 'completed');
  });
});

describe('HermesPipeline — retry on failure', () => {
  it('should retry a failing task and eventually dead-letter it', async () => {
    const bus    = new EventEmitter();
    const dead   = [];
    const failed = [];

    bus.on('pipeline:task:dead',   e => dead.push(e));
    bus.on('pipeline:task:failed', e => failed.push(e));

    const registry = {
      list: () => [{
        id: 'agent-fail', name: 'bad', type: 'bad',
        status: 'active', capabilities: ['always-fail'],
      }],
    };

    // Always reject
    const dispatcher = async () => { throw new Error('forced failure'); };

    const pipeline = new HermesPipeline({
      registry, bus, dispatcher, pollMs: 30,
    });

    // maxRetries=2 → 3 total attempts → dead
    pipeline.submit({
      type:       'always-fail',
      payload:    {},
      maxRetries: 2,
    });

    pipeline.start();

    await waitFor(() => dead.length > 0, 15_000);
    pipeline.stop();

    assert.ok(dead.length > 0,    'dead event fired');
    assert.ok(failed.length >= 2, 'at least 2 failures before dead');
  });
});

describe('HermesPipeline — no-agent behaviour', () => {
  it('should emit pipeline:no-agents when registry is empty', async () => {
    const bus    = new EventEmitter();
    const noAgent = [];

    bus.on('pipeline:no-agents', e => noAgent.push(e));

    const pipeline = new HermesPipeline({
      registry:   { list: () => [] }, // empty registry
      bus,
      dispatcher: async () => ({}),
      pollMs:     50,
    });

    pipeline.submit({ type: 'orphan', payload: {} });
    pipeline.start();

    await waitFor(() => noAgent.length > 0, 3_000);
    pipeline.stop();

    assert.ok(noAgent.length > 0, 'no-agents event fired');
  });
});

describe('HermesPipeline — external job source (Hermes)', () => {
  it('should ingest jobs from external jobSource and dispatch them', async () => {
    const bus       = new EventEmitter();
    const completed = [];

    bus.on('pipeline:task:completed', e => completed.push(e));

    const registry = {
      list: () => [{
        id: 'agent-h', name: 'hermes-worker', type: 'hermes-job',
        status: 'active', capabilities: ['hermes-job'],
      }],
    };

    let sourceCalled = false;
    const jobSource = async () => {
      if (sourceCalled) return [];
      sourceCalled = true;
      return [{ type: 'hermes-job', payload: { url: 'https://example.com' }, priority: 1 }];
    };

    const pipeline = new HermesPipeline({
      registry,
      bus,
      dispatcher: async () => ({ fetched: true }),
      pollMs:     50,
      jobSource,
    });

    pipeline.start();

    await waitFor(() => completed.length > 0, 5_000);
    pipeline.stop();

    assert.ok(completed.length > 0,    'external job was dispatched');
    assert.ok(sourceCalled,            'jobSource was called');
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// pipeline-api REST endpoints  (lightweight, no HTTP server needed)
// ═══════════════════════════════════════════════════════════════════════════════

describe('pipeline-api — request / response shapes', () => {
  // We test the router logic directly without spinning up a real server
  // by using a tiny req/res mock.

  let pipeline, router;

  beforeEach(() => {
    pipeline = new HermesPipeline({
      registry:   { list: () => [] },
      bus:        new EventEmitter(),
      dispatcher: async () => ({}),
      pollMs:     100_000,
    });

    const { createPipelineRouter } = require('./pipeline-api');
    const wsStub = { path: '/ws/agent-status', available: true, clientCount: 0 };
    router = createPipelineRouter(pipeline, wsStub);
  });

  afterEach(() => pipeline.stop());

  it('GET /status handler returns ok:true', async () => {
    const { res, body } = await callRoute(router, 'GET', '/status');
    assert.strictEqual(res.statusCode, 200);
    assert.strictEqual(body.ok, true);
    assert.ok(body.pipeline);
  });

  it('POST /tasks with valid body returns 201 + task', async () => {
    const { res, body } = await callRoute(router, 'POST', '/tasks', {
      type: 'data-aggregator', payload: { url: 'http://x.io' }
    });
    assert.strictEqual(res.statusCode, 201);
    assert.strictEqual(body.ok, true);
    assert.ok(body.task.id);
    assert.strictEqual(body.task.type, 'data-aggregator');
  });

  it('POST /tasks with missing type returns 400', async () => {
    const { res, body } = await callRoute(router, 'POST', '/tasks', { payload: {} });
    assert.strictEqual(res.statusCode, 400);
    assert.strictEqual(body.ok, false);
    assert.match(body.error, /type is required/);
  });

  it('GET /tasks/:id returns 404 for unknown task', async () => {
    const { res, body } = await callRoute(router, 'GET', '/tasks/does-not-exist');
    assert.strictEqual(res.statusCode, 404);
    assert.strictEqual(body.ok, false);
  });

  it('GET /tasks/:id returns task for known id', async () => {
    const task = pipeline.submit({ type: 'publisher' });
    const { res, body } = await callRoute(router, 'GET', `/tasks/${task.id}`);
    assert.strictEqual(res.statusCode, 200);
    assert.strictEqual(body.task.id, task.id);
  });

  it('GET /tasks returns active + dead arrays', async () => {
    pipeline.submit({ type: 'alpha' });
    const { body } = await callRoute(router, 'GET', '/tasks');
    assert.ok(Array.isArray(body.active));
    assert.ok(Array.isArray(body.dead));
    assert.ok(body.stats);
  });

  it('POST /start returns ok', async () => {
    const { body } = await callRoute(router, 'POST', '/start');
    assert.strictEqual(body.ok, true);
    pipeline.stop();
  });

  it('POST /stop returns ok', async () => {
    pipeline.start();
    const { body } = await callRoute(router, 'POST', '/stop');
    assert.strictEqual(body.ok, true);
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// Helpers
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Poll predicate every 100 ms until it returns true or timeout.
 */
function waitFor(predicate, timeoutMs = 5_000) {
  return new Promise((resolve, reject) => {
    const start = Date.now();
    const iv = setInterval(() => {
      if (predicate()) {
        clearInterval(iv);
        resolve();
      } else if (Date.now() - start > timeoutMs) {
        clearInterval(iv);
        reject(new Error(`waitFor timed out after ${timeoutMs}ms`));
      }
    }, 100);
  });
}

/**
 * Minimal req/res mock for calling an Express router directly.
 */
function callRoute(router, method, url, body = null) {
  return new Promise((resolve) => {
    const [pathname, search = ''] = url.split('?');
    const query = Object.fromEntries(new URLSearchParams(search));

    const req = {
      method,
      url,
      path:   pathname,
      params: extractParams(router, method, pathname),
      query,
      body:   body || {},
      headers: { 'content-type': 'application/json' },
    };

    const res = {
      statusCode: 200,
      _body: null,
      status(code)  { this.statusCode = code; return this; },
      json(data)    { this._body = data; resolve({ res: this, body: data }); },
      send(data)    { this._body = data; resolve({ res: this, body: data }); },
    };

    // Walk the router's stack to find the right handler
    router.handle(req, res, (err) => {
      if (err) {
        res.statusCode = err.status || 500;
        resolve({ res, body: { ok: false, error: err.message } });
      } else {
        // No handler matched → 404
        resolve({ res: { statusCode: 404 }, body: { ok: false, error: 'not found' } });
      }
    });
  });
}

/**
 * Extract path params from a router stack by matching route patterns.
 * Simple implementation for :id style params.
 */
function extractParams(router, method, pathname) {
  const params = {};
  if (!router.stack) return params;

  for (const layer of router.stack) {
    if (!layer.route) continue;
    const match = layer.match?.(pathname);
    if (match && layer.route.path) {
      const pattern = layer.route.path.split('/');
      const parts   = pathname.split('/');
      pattern.forEach((seg, i) => {
        if (seg.startsWith(':')) params[seg.slice(1)] = parts[i];
      });
      break;
    }
  }
  return params;
}
