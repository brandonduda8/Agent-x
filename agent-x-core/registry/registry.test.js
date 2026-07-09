/**
 * Agent Registry & Heartbeat Monitor — Self-contained Smoke Tests
 * =============================================================================
 * Zero external test-framework dependencies — uses Node's built-in assert
 * module.  Designed to run in Termux (Android) and standard Linux:
 *
 *   node agent-x-core/registry/registry.test.js
 *
 * Exit code:
 *   0 — all tests passed
 *   1 — one or more tests failed
 *
 * Data isolation:
 *   Uses a temp file so tests never touch data/agents.json in production.
 * =============================================================================
 */

'use strict';

const assert = require('assert');
const fs     = require('fs');
const path   = require('path');
const os     = require('os');

// --------------------------------------------------------------------------- #
// Redirect the registry's store path to a temp file for test isolation
// --------------------------------------------------------------------------- #

// The registry resolves STORE_PATH at require-time relative to __dirname, so we
// monkey-patch fs.readFileSync / writeFileSync before requiring the module.
const TEMP_STORE = path.join(
  os.tmpdir(),
  `agent-x-test-${Date.now()}-${process.pid}.json`,
);

// Initialise temp store
fs.writeFileSync(TEMP_STORE, JSON.stringify({ agents: [] }, null, 2), 'utf8');

// Patch path.resolve so the registry picks up our temp file
const originalResolve = path.resolve.bind(path);
path.resolve = (...args) => {
  const result = originalResolve(...args);
  if (result.endsWith('data/agents.json')) return TEMP_STORE;
  return result;
};

// Now require the registry (it will capture the patched path)
const registry = require('./agent-registry');
const monitor  = require('./heartbeat-monitor');

// --------------------------------------------------------------------------- #
// Tiny test harness
// --------------------------------------------------------------------------- #

let passed = 0;
let failed = 0;
const failures = [];

function test(name, fn) {
  try {
    fn();
    console.log(`  ✔  ${name}`);
    passed++;
  } catch (e) {
    console.error(`  ✘  ${name}`);
    console.error(`     → ${e.message}`);
    failures.push({ name, message: e.message });
    failed++;
  }
}

function section(title) {
  console.log(`\n── ${title} ──`);
}

// --------------------------------------------------------------------------- #
// Helpers
// --------------------------------------------------------------------------- #

/** Wipe the temp store back to an empty state between test groups. */
function resetStore() {
  fs.writeFileSync(TEMP_STORE, JSON.stringify({ agents: [] }, null, 2), 'utf8');
}

// --------------------------------------------------------------------------- #
// Tests
// --------------------------------------------------------------------------- #

section('1. Validation — createAgent');

test('rejects missing name', () => {
  const { valid, errors } = registry.validateCreatePayload({ type: 'worker' });
  assert.strictEqual(valid, false);
  assert.ok(errors.some((e) => e.includes('"name"')));
});

test('rejects missing type', () => {
  const { valid, errors } = registry.validateCreatePayload({ name: 'Alpha' });
  assert.strictEqual(valid, false);
  assert.ok(errors.some((e) => e.includes('"type"')));
});

test('rejects invalid status', () => {
  const { valid, errors } = registry.validateCreatePayload({
    name: 'X', type: 'worker', status: 'unknown',
  });
  assert.strictEqual(valid, false);
  assert.ok(errors.some((e) => e.includes('"status"')));
});

test('rejects non-array capabilities', () => {
  const { valid, errors } = registry.validateCreatePayload({
    name: 'X', type: 'worker', capabilities: 'draft',
  });
  assert.strictEqual(valid, false);
  assert.ok(errors.some((e) => e.includes('"capabilities"')));
});

test('accepts valid minimal payload', () => {
  const { valid } = registry.validateCreatePayload({ name: 'Alpha', type: 'worker' });
  assert.strictEqual(valid, true);
});

test('accepts full valid payload', () => {
  const { valid } = registry.validateCreatePayload({
    name: 'Beta', type: 'orchestrator', capabilities: ['draft', 'aggregate'], status: 'idle',
  });
  assert.strictEqual(valid, true);
});

// --------------------------------------------------------------------------- #
section('2. Validation — updateAgent');

test('rejects immutable id field', () => {
  const { valid, errors } = registry.validateUpdatePayload({ id: 'new-id' });
  assert.strictEqual(valid, false);
  assert.ok(errors.some((e) => e.includes('"id"')));
});

test('rejects immutable created_at field', () => {
  const { valid, errors } = registry.validateUpdatePayload({ created_at: '2024-01-01' });
  assert.strictEqual(valid, false);
  assert.ok(errors.some((e) => e.includes('"created_at"')));
});

test('accepts empty update payload (no-op patch)', () => {
  const { valid } = registry.validateUpdatePayload({});
  assert.strictEqual(valid, true);
});

test('accepts partial update payload', () => {
  const { valid } = registry.validateUpdatePayload({ status: 'active' });
  assert.strictEqual(valid, true);
});

// --------------------------------------------------------------------------- #
section('3. CRUD — createAgent');

resetStore();

let agentA, agentB;

test('creates agent and returns it', () => {
  const result = registry.createAgent({ name: 'Alpha', type: 'worker', capabilities: ['draft'] });
  assert.strictEqual(result.ok, true);
  assert.ok(result.agent.id);
  assert.strictEqual(result.agent.name, 'Alpha');
  assert.strictEqual(result.agent.type, 'worker');
  assert.deepStrictEqual(result.agent.capabilities, ['draft']);
  assert.strictEqual(result.agent.status, 'idle');
  assert.strictEqual(result.agent.current_task_id, null);
  assert.strictEqual(result.agent.last_heartbeat, null);
  assert.ok(result.agent.created_at);
  assert.ok(result.agent.updated_at);
  agentA = result.agent;
});

test('creates a second agent independently', () => {
  const result = registry.createAgent({ name: 'Beta', type: 'orchestrator', status: 'active' });
  assert.strictEqual(result.ok, true);
  assert.ok(result.agent.id);
  assert.notStrictEqual(result.agent.id, agentA.id);
  agentB = result.agent;
});

test('returns error for invalid create payload', () => {
  const result = registry.createAgent({ type: 'worker' }); // missing name
  assert.strictEqual(result.ok, false);
  assert.ok(Array.isArray(result.errors));
});

// --------------------------------------------------------------------------- #
section('4. CRUD — listAgents');

test('lists all agents', () => {
  const agents = registry.listAgents();
  assert.strictEqual(agents.length, 2);
});

test('filters by status', () => {
  const active = registry.listAgents({ status: 'active' });
  assert.strictEqual(active.length, 1);
  assert.strictEqual(active[0].id, agentB.id);
});

test('filters by type', () => {
  const workers = registry.listAgents({ type: 'worker' });
  assert.strictEqual(workers.length, 1);
  assert.strictEqual(workers[0].id, agentA.id);
});

test('filter for non-existent status returns empty array', () => {
  const offline = registry.listAgents({ status: 'offline' });
  assert.strictEqual(offline.length, 0);
});

// --------------------------------------------------------------------------- #
section('5. CRUD — getAgent');

test('returns existing agent by id', () => {
  const agent = registry.getAgent(agentA.id);
  assert.ok(agent);
  assert.strictEqual(agent.id, agentA.id);
});

test('returns null for unknown id', () => {
  const agent = registry.getAgent('00000000-0000-0000-0000-000000000000');
  assert.strictEqual(agent, null);
});

// --------------------------------------------------------------------------- #
section('6. CRUD — updateAgent');

test('updates allowed fields', () => {
  const result = registry.updateAgent(agentA.id, {
    name: 'Alpha-Updated', status: 'active', current_task_id: 'task-001',
  });
  assert.strictEqual(result.ok, true);
  assert.strictEqual(result.agent.name, 'Alpha-Updated');
  assert.strictEqual(result.agent.status, 'active');
  assert.strictEqual(result.agent.current_task_id, 'task-001');
});

test('update is persisted (read back)', () => {
  const agent = registry.getAgent(agentA.id);
  assert.strictEqual(agent.name, 'Alpha-Updated');
  assert.strictEqual(agent.current_task_id, 'task-001');
});

test('returns notFound for unknown id', () => {
  const result = registry.updateAgent('no-such-id', { status: 'idle' });
  assert.strictEqual(result.ok, false);
  assert.strictEqual(result.notFound, true);
});

test('rejects immutable field in update', () => {
  const result = registry.updateAgent(agentA.id, { id: 'hacked' });
  assert.strictEqual(result.ok, false);
  assert.ok(result.errors.some((e) => e.includes('"id"')));
});

test('updated_at advances after update', () => {
  const before = agentA.updated_at;
  // Small sleep to ensure timestamp differs
  const start = Date.now();
  while (Date.now() - start < 5) {} // busy-wait 5ms
  registry.updateAgent(agentA.id, { status: 'idle' });
  const after = registry.getAgent(agentA.id).updated_at;
  assert.ok(new Date(after) >= new Date(before));
});

// --------------------------------------------------------------------------- #
section('7. CRUD — deleteAgent');

test('deletes existing agent', () => {
  const result = registry.deleteAgent(agentB.id);
  assert.strictEqual(result.ok, true);
});

test('deleted agent no longer returned by list', () => {
  const agents = registry.listAgents();
  assert.ok(!agents.some((a) => a.id === agentB.id));
});

test('returns notFound for already-deleted id', () => {
  const result = registry.deleteAgent(agentB.id);
  assert.strictEqual(result.ok, false);
  assert.strictEqual(result.notFound, true);
});

// --------------------------------------------------------------------------- #
section('8. Heartbeat — recordHeartbeat');

resetStore();
const hbResult = registry.createAgent({ name: 'Gamma', type: 'worker' });
const agentC   = hbResult.agent;

test('records heartbeat and updates last_heartbeat', () => {
  const result = registry.recordHeartbeat(agentC.id, { status: 'active' });
  assert.strictEqual(result.ok, true);
  assert.ok(result.agent.last_heartbeat);
  assert.strictEqual(result.agent.status, 'active');
});

test('heartbeat updates current_task_id', () => {
  const result = registry.recordHeartbeat(agentC.id, { current_task_id: 'task-xyz' });
  assert.strictEqual(result.ok, true);
  assert.strictEqual(result.agent.current_task_id, 'task-xyz');
});

test('heartbeat with no payload keeps existing status (if not stale/offline)', () => {
  // Agent is currently 'active' — no status in payload → stays 'active'
  const result = registry.recordHeartbeat(agentC.id, {});
  assert.strictEqual(result.ok, true);
  assert.strictEqual(result.agent.status, 'active');
});

test('heartbeat revives stale agent to idle when no status provided', () => {
  // Force agent to stale
  registry.updateAgent(agentC.id, { status: 'stale' });
  const result = registry.recordHeartbeat(agentC.id); // no payload
  assert.strictEqual(result.ok, true);
  assert.strictEqual(result.agent.status, 'idle');
});

test('returns notFound for heartbeat on unknown id', () => {
  const result = registry.recordHeartbeat('no-such-id');
  assert.strictEqual(result.ok, false);
  assert.strictEqual(result.notFound, true);
});

test('rejects invalid status in heartbeat payload', () => {
  const result = registry.recordHeartbeat(agentC.id, { status: 'broken' });
  assert.strictEqual(result.ok, false);
  assert.ok(Array.isArray(result.errors));
});

// --------------------------------------------------------------------------- #
section('9. Heartbeat — markStaleAgents');

resetStore();

test('marks agent stale when last_heartbeat exceeds threshold', () => {
  // Create agent with a heartbeat timestamp far in the past
  const r   = registry.createAgent({ name: 'Old', type: 'worker' });
  const old = r.agent;

  // Directly write an old last_heartbeat (2 minutes ago)
  const agents   = JSON.parse(fs.readFileSync(TEMP_STORE, 'utf8')).agents;
  const idx      = agents.findIndex((a) => a.id === old.id);
  agents[idx].last_heartbeat = new Date(Date.now() - 120_000).toISOString();
  agents[idx].status         = 'active';
  fs.writeFileSync(TEMP_STORE, JSON.stringify({ agents }, null, 2), 'utf8');

  const staled = registry.markStaleAgents(60_000); // 60 s threshold
  assert.strictEqual(staled.length, 1);
  assert.strictEqual(staled[0].id, old.id);
  assert.strictEqual(staled[0].status, 'stale');
});

test('does not mark fresh agents stale', () => {
  // Fresh agent with a very recent heartbeat
  const r = registry.createAgent({ name: 'Fresh', type: 'worker' });
  registry.recordHeartbeat(r.agent.id, { status: 'active' });

  const staled = registry.markStaleAgents(60_000);
  // The 'Old' agent is already stale from previous test, so count should be 0 new ones
  assert.ok(!staled.some((a) => a.name === 'Fresh'));
});

test('does not touch offline agents', () => {
  const r = registry.createAgent({ name: 'Dead', type: 'worker' });
  registry.updateAgent(r.agent.id, { status: 'offline' });

  const staled = registry.markStaleAgents(1); // 1ms threshold — everything should stale
  // Offline agents must remain offline
  const dead = registry.getAgent(r.agent.id);
  assert.strictEqual(dead.status, 'offline');
  assert.ok(!staled.some((a) => a.id === r.agent.id));
});

// --------------------------------------------------------------------------- #
section('10. HeartbeatMonitor');

test('monitor starts and stops cleanly', () => {
  assert.strictEqual(monitor.isRunning, false);
  monitor.start();
  assert.strictEqual(monitor.isRunning, true);
  monitor.stop();
  assert.strictEqual(monitor.isRunning, false);
});

test('calling start() twice is safe (no-op)', () => {
  monitor.start();
  monitor.start(); // second call should be a no-op
  assert.strictEqual(monitor.isRunning, true);
  monitor.stop();
});

test('tick() increments tickCount', () => {
  const before = monitor.tickCount;
  monitor.tick();
  assert.strictEqual(monitor.tickCount, before + 1);
});

test('summary() returns correct shape', () => {
  const s = monitor.summary();
  assert.ok(typeof s.total   === 'number');
  assert.ok(typeof s.active  === 'number');
  assert.ok(typeof s.idle    === 'number');
  assert.ok(typeof s.stale   === 'number');
  assert.ok(typeof s.offline === 'number');
});

test('summary() totals match listAgents() length', () => {
  const total  = registry.listAgents().length;
  const sum    = monitor.summary();
  assert.strictEqual(sum.total, total);
});

test('monitor emits stale event when agents become stale', (done) => {
  // This test is synchronous — we call tick() manually instead of waiting for
  // the interval, so we use a flag rather than a done callback.
  let emitted = false;
  monitor.once('stale', () => { emitted = true; });

  // Force the store to have an agent with an ancient heartbeat
  resetStore();
  const r = registry.createAgent({ name: 'AboutToStale', type: 'worker' });
  const agents = JSON.parse(fs.readFileSync(TEMP_STORE, 'utf8')).agents;
  const idx    = agents.findIndex((a) => a.id === r.agent.id);
  agents[idx].last_heartbeat = new Date(Date.now() - 200_000).toISOString();
  agents[idx].status         = 'active';
  fs.writeFileSync(TEMP_STORE, JSON.stringify({ agents }, null, 2), 'utf8');

  monitor.tick();
  assert.strictEqual(emitted, true, 'Expected "stale" event to be emitted');
});

// --------------------------------------------------------------------------- #
section('11. Persistence — data survives module reload simulation');

test('data written by createAgent can be re-read by listAgents', () => {
  resetStore();
  registry.createAgent({ name: 'Persist-1', type: 'worker' });
  registry.createAgent({ name: 'Persist-2', type: 'orchestrator' });

  // listAgents re-reads from disk each call
  const agents = registry.listAgents();
  assert.strictEqual(agents.length, 2);
  assert.ok(agents.some((a) => a.name === 'Persist-1'));
  assert.ok(agents.some((a) => a.name === 'Persist-2'));
});

test('update is immediately visible in subsequent reads', () => {
  const id     = registry.listAgents()[0].id;
  registry.updateAgent(id, { status: 'active', current_task_id: 'persist-task' });
  const agent  = registry.getAgent(id);
  assert.strictEqual(agent.status, 'active');
  assert.strictEqual(agent.current_task_id, 'persist-task');
});

// --------------------------------------------------------------------------- #
// Cleanup
// --------------------------------------------------------------------------- #
try { fs.unlinkSync(TEMP_STORE); } catch (_) {}

// --------------------------------------------------------------------------- #
// Results
// --------------------------------------------------------------------------- #
console.log('\n' + '═'.repeat(55));
console.log(`  PASSED:  ${passed}`);
console.log(`  FAILED:  ${failed}`);
console.log('═'.repeat(55));

if (failed > 0) {
  console.error('\nFailed tests:');
  for (const f of failures) {
    console.error(`  • ${f.name}`);
    console.error(`    ${f.message}`);
  }
  process.exit(1);
} else {
  console.log('\n  All tests passed ✔');
  process.exit(0);
}
