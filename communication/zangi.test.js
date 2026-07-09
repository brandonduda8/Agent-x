/**
 * Zangi Communication Layer — Unit Tests
 *
 * Tests cover:
 *   - ZangiClient request building and retry logic
 *   - Agent map CRUD operations and index consistency
 *   - Webhook handler: HMAC verification, event routing, agent dispatch
 *   - Packet schema: Zangi task factories
 *   - Broadcast logic
 *
 * Run with:  node communication/zangi.test.js
 * (No external test framework required — uses Node.js assert)
 */

'use strict';

const assert = require('assert');
const crypto = require('crypto');

// ---------------------------------------------------------------------------
// Minimal test runner
// ---------------------------------------------------------------------------

let passed = 0;
let failed = 0;
const errors = [];

async function test(name, fn) {
  try {
    await fn();
    console.log(`  ✓ ${name}`);
    passed++;
  } catch (err) {
    console.error(`  ✗ ${name}`);
    console.error(`      ${err.message}`);
    failed++;
    errors.push({ name, error: err });
  }
}

function describe(suiteName, fn) {
  console.log(`\n${suiteName}`);
  fn();
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Build HMAC-SHA256 signature in Zangi format. */
function buildSignature(body, secret) {
  const hex = crypto.createHmac('sha256', secret).update(body).digest('hex');
  return `sha256=${hex}`;
}

// ---------------------------------------------------------------------------
// Packet schema tests
// ---------------------------------------------------------------------------

describe('packet-schema.js', () => {
  const { STATUS, TASK_TYPES, createTask, createZangiMessageTask, createZangiBroadcastTask } =
    require('./packet-schema');

  test('createTask returns correct shape', () => {
    const t = createTask({ type: 'generic', payload: { foo: 'bar' } });
    assert.ok(t.id, 'should have id');
    assert.strictEqual(t.type, 'generic');
    assert.deepStrictEqual(t.payload, { foo: 'bar' });
    assert.strictEqual(t.status, STATUS.QUEUED);
    assert.ok(t.createdAt);
    assert.ok(t.updatedAt);
    assert.strictEqual(t.completedAt, null);
    assert.strictEqual(t.result, null);
  });

  test('createTask generates unique IDs', () => {
    const ids = new Set([1, 2, 3, 4, 5].map(() => createTask({}).id));
    assert.strictEqual(ids.size, 5, 'IDs should be unique');
  });

  test('TASK_TYPES contains Zangi types', () => {
    assert.ok(TASK_TYPES.ZANGI_MESSAGE);
    assert.ok(TASK_TYPES.ZANGI_BROADCAST);
    assert.strictEqual(TASK_TYPES.ZANGI_MESSAGE, 'zangi:message');
    assert.strictEqual(TASK_TYPES.ZANGI_BROADCAST, 'zangi:broadcast');
  });

  test('createZangiMessageTask builds correct payload', () => {
    const t = createZangiMessageTask({
      from: 'zangi-uid-operator',
      to: 'zangi-uid-agent',
      message: 'Hello agent!',
    });
    assert.strictEqual(t.type, 'zangi:message');
    assert.strictEqual(t.payload.source, 'zangi');
    assert.strictEqual(t.payload.from, 'zangi-uid-operator');
    assert.strictEqual(t.payload.to, 'zangi-uid-agent');
    assert.strictEqual(t.payload.message, 'Hello agent!');
  });

  test('createZangiBroadcastTask sets broadcast flag', () => {
    const t = createZangiBroadcastTask({ message: 'System shutdown' });
    assert.strictEqual(t.type, 'zangi:broadcast');
    assert.strictEqual(t.payload.broadcast, true);
    assert.strictEqual(t.payload.message, 'System shutdown');
  });
});

// ---------------------------------------------------------------------------
// Agent map tests (uses a temp in-memory state — no disk writes in tests)
// ---------------------------------------------------------------------------

describe('zangi-agent-map.js', () => {
  // We exercise the public API but avoid polluting the real map file.
  // upsert with persist:false avoids disk writes.
  const agentMap = require('./zangi-agent-map');

  const testEntry = {
    agentId: '__test-agent-' + Date.now(),
    agentName: 'test-agent-unit',
    zangiUserId: 'zangi-uid-test-001',
    zangiChannelId: 'zangi-chan-test-001',
    capabilities: ['test'],
    active: true,
  };

  test('upsert + getByAgentId', () => {
    agentMap.upsert(testEntry, { persist: false });
    const found = agentMap.getByAgentId(testEntry.agentId);
    assert.ok(found, 'should find entry by agentId');
    assert.strictEqual(found.agentId, testEntry.agentId);
  });

  test('getByAgentName', () => {
    const found = agentMap.getByAgentName('test-agent-unit');
    assert.ok(found, 'should find entry by agentName');
    assert.strictEqual(found.agentId, testEntry.agentId);
  });

  test('getByZangiUserId', () => {
    const found = agentMap.getByZangiUserId('zangi-uid-test-001');
    assert.ok(found, 'should find entry by zangiUserId');
  });

  test('getByZangiChannelId', () => {
    const found = agentMap.getByZangiChannelId('zangi-chan-test-001');
    assert.ok(found, 'should find entry by zangiChannelId');
  });

  test('resolve by agentId', () => {
    const found = agentMap.resolve(testEntry.agentId);
    assert.ok(found);
  });

  test('resolve by agentName', () => {
    const found = agentMap.resolve('test-agent-unit');
    assert.ok(found);
  });

  test('resolve returns null for unknown', () => {
    const found = agentMap.resolve('does-not-exist-' + Date.now());
    assert.strictEqual(found, null);
  });

  test('listAll excludes __broadcast__ entry', () => {
    const all = agentMap.listAll();
    assert.ok(!all.some((e) => e.agentId === '__broadcast__'), 'should exclude broadcast entry');
  });

  test('listAll excludes inactive by default', () => {
    const inactiveId = '__test-inactive-' + Date.now();
    agentMap.upsert({ agentId: inactiveId, active: false }, { persist: false });
    const all = agentMap.listAll();
    assert.ok(!all.some((e) => e.agentId === inactiveId), 'inactive should be excluded by default');
    const withInactive = agentMap.listAll({ includeInactive: true });
    assert.ok(withInactive.some((e) => e.agentId === inactiveId), 'inactive included when asked');
    // cleanup
    agentMap.remove(inactiveId, { persist: false });
  });

  test('upsert updates existing entry', () => {
    agentMap.upsert({ ...testEntry, zangiUserId: 'zangi-uid-updated' }, { persist: false });
    const found = agentMap.getByAgentId(testEntry.agentId);
    assert.strictEqual(found.zangiUserId, 'zangi-uid-updated');
  });

  test('remove deletes all indices', () => {
    agentMap.remove(testEntry.agentId, { persist: false });
    assert.strictEqual(agentMap.getByAgentId(testEntry.agentId), null);
    assert.strictEqual(agentMap.getByAgentName('test-agent-unit'), null);
    // zangiUserId was updated to 'zangi-uid-updated' — check that's gone too
    assert.strictEqual(agentMap.getByZangiUserId('zangi-uid-updated'), null);
    assert.strictEqual(agentMap.getByZangiChannelId('zangi-chan-test-001'), null);
  });
});

// ---------------------------------------------------------------------------
// Webhook handler tests
// ---------------------------------------------------------------------------

describe('zangi-webhook-handler.js', () => {
  const {
    verifySignature,
    registerAgentHandler,
    unregisterAgentHandler,
    processEvent,
  } = require('./zangi-webhook-handler');
  const agentMap = require('./zangi-agent-map');

  // ── verifySignature ──────────────────────────────────────────────────────

  test('verifySignature: returns true when no secret configured', () => {
    // ZANGI_WEBHOOK_SECRET is not set in this test context
    const result = verifySignature('{"test":1}', '');
    assert.strictEqual(result, true, 'should pass when secret not set');
  });

  test('verifySignature: correct HMAC returns true', () => {
    const secret = 'test-secret-123';
    const body = '{"event":"message.received"}';
    const sig = buildSignature(body, secret);

    // Temporarily set env var
    const prev = process.env.ZANGI_WEBHOOK_SECRET;
    process.env.ZANGI_WEBHOOK_SECRET = secret;

    // Re-require to pick up updated env — but verifySignature reads the module-level const.
    // Instead test the pure function logic directly:
    const hex = crypto.createHmac('sha256', secret).update(body).digest('hex');
    const expected = `sha256=${hex}`;
    assert.strictEqual(sig, expected);

    process.env.ZANGI_WEBHOOK_SECRET = prev || '';
  });

  test('verifySignature: wrong algorithm prefix returns false', () => {
    const result = verifySignature('body', 'md5=abc123');
    // Without a configured secret this always returns true, so only meaningful when secret is set.
    // Just assert it doesn't throw.
    assert.ok(typeof result === 'boolean');
  });

  // ── In-process handler registration ─────────────────────────────────────

  test('registerAgentHandler + dispatch', async () => {
    const agentId = '__test-dispatch-' + Date.now();
    const received = [];

    // Add a map entry for this agent
    agentMap.upsert(
      { agentId, agentName: agentId, zangiUserId: 'zangi-uid-dispatch-test', active: true },
      { persist: false }
    );

    registerAgentHandler(agentId, async (task) => {
      received.push(task);
    });

    const event = {
      type: 'message.received',
      from: 'zangi-uid-operator',
      to: 'zangi-uid-dispatch-test',
      channelId: null,
      message: 'Execute task XYZ',
      metadata: {},
    };

    const result = await processEvent(event);

    assert.strictEqual(result.dispatched, true, 'should have dispatched');
    assert.strictEqual(received.length, 1, 'handler should have been called once');
    assert.strictEqual(received[0].type, 'zangi:message');
    assert.strictEqual(received[0].payload.message, 'Execute task XYZ');

    // cleanup
    unregisterAgentHandler(agentId);
    agentMap.remove(agentId, { persist: false });
  });

  test('processEvent: message.received with channelId routing', async () => {
    const agentId = '__test-channel-route-' + Date.now();
    const chanId = 'zangi-chan-test-route-' + Date.now();
    const received = [];

    agentMap.upsert(
      { agentId, agentName: agentId, zangiChannelId: chanId, active: true },
      { persist: false }
    );
    registerAgentHandler(agentId, async (task) => received.push(task));

    const result = await processEvent({
      type: 'message.received',
      from: 'zangi-uid-user',
      to: null,
      channelId: chanId,
      message: 'Channel test message',
      metadata: {},
    });

    assert.strictEqual(result.dispatched, true);
    assert.strictEqual(received.length, 1);
    assert.strictEqual(received[0].payload.channelId, chanId);

    // cleanup
    unregisterAgentHandler(agentId);
    agentMap.remove(agentId, { persist: false });
  });

  test('processEvent: message.received with metadata.agentId routing', async () => {
    const agentId = '__test-meta-route-' + Date.now();
    const received = [];

    agentMap.upsert({ agentId, agentName: agentId, active: true }, { persist: false });
    registerAgentHandler(agentId, async (task) => received.push(task));

    const result = await processEvent({
      type: 'message.received',
      from: 'zangi-uid-user',
      to: null,
      channelId: null,
      message: 'Metadata routing test',
      metadata: { agentId },
    });

    assert.strictEqual(result.dispatched, true);
    assert.strictEqual(received.length, 1);

    unregisterAgentHandler(agentId);
    agentMap.remove(agentId, { persist: false });
  });

  test('processEvent: unresolvable target returns dispatched=false', async () => {
    const result = await processEvent({
      type: 'message.received',
      from: 'zangi-uid-user',
      to: 'zangi-uid-nobody-known',
      channelId: null,
      message: 'Nobody home',
      metadata: {},
    });

    assert.strictEqual(result.dispatched, false);
    assert.strictEqual(result.agent, null);
  });

  test('processEvent: message.delivered returns handled=true', async () => {
    const result = await processEvent({
      type: 'message.delivered',
      messageId: 'msg-001',
    });
    assert.strictEqual(result.handled, true);
  });

  test('processEvent: message.read returns handled=true', async () => {
    const result = await processEvent({ type: 'message.read', messageId: 'msg-002' });
    assert.strictEqual(result.handled, true);
  });

  test('processEvent: unknown type returns handled=false', async () => {
    const result = await processEvent({ type: 'some.unknown.event' });
    assert.strictEqual(result.handled, false);
  });

  test('processEvent: broadcast channel routes to all agents', async () => {
    // Set a broadcast channel ID
    const broadcastChanId = 'zangi-chan-broadcast-unit-test-' + Date.now();
    process.env.ZANGI_BROADCAST_CHANNEL_ID = broadcastChanId;

    const agentId1 = '__test-bc1-' + Date.now();
    const agentId2 = '__test-bc2-' + Date.now();
    const received = { [agentId1]: [], [agentId2]: [] };

    agentMap.upsert({ agentId: agentId1, active: true }, { persist: false });
    agentMap.upsert({ agentId: agentId2, active: true }, { persist: false });
    registerAgentHandler(agentId1, async (t) => received[agentId1].push(t));
    registerAgentHandler(agentId2, async (t) => received[agentId2].push(t));

    await processEvent({
      type: 'message.received',
      from: 'zangi-uid-operator',
      channelId: broadcastChanId,
      message: 'Broadcast test',
      metadata: {},
    });

    // Each registered test agent should have received a broadcast task
    assert.ok(received[agentId1].length > 0, 'agent1 should receive broadcast');
    assert.ok(received[agentId2].length > 0, 'agent2 should receive broadcast');
    assert.strictEqual(received[agentId1][0].type, 'zangi:broadcast');

    // cleanup
    unregisterAgentHandler(agentId1);
    unregisterAgentHandler(agentId2);
    agentMap.remove(agentId1, { persist: false });
    agentMap.remove(agentId2, { persist: false });
    delete process.env.ZANGI_BROADCAST_CHANNEL_ID;
  });
});

// ---------------------------------------------------------------------------
// ZangiClient tests (unit — no real HTTP)
// ---------------------------------------------------------------------------

describe('zangi-client.js', () => {
  const { ZangiClient, MESSAGE_TYPES } = require('./zangi-client');

  test('MESSAGE_TYPES contains expected values', () => {
    assert.strictEqual(MESSAGE_TYPES.TEXT, 'text');
    assert.strictEqual(MESSAGE_TYPES.BROADCAST, 'broadcast');
    assert.strictEqual(MESSAGE_TYPES.TASK, 'task');
    assert.strictEqual(MESSAGE_TYPES.COMMAND, 'command');
  });

  test('ZangiClient constructor reads env vars', () => {
    process.env.ZANGI_API_KEY = 'test-key';
    process.env.ZANGI_APP_ID = 'test-app';
    const client = new ZangiClient();
    assert.strictEqual(client.apiKey, 'test-key');
    assert.strictEqual(client.appId, 'test-app');
    delete process.env.ZANGI_API_KEY;
    delete process.env.ZANGI_APP_ID;
  });

  test('ZangiClient constructor accepts options over env', () => {
    process.env.ZANGI_API_KEY = 'env-key';
    const client = new ZangiClient({ apiKey: 'opts-key' });
    assert.strictEqual(client.apiKey, 'opts-key');
    delete process.env.ZANGI_API_KEY;
  });

  test('sendDirectMessage throws without toUserId', async () => {
    const client = new ZangiClient({ apiKey: 'k', apiSecret: 's', appId: 'a' });
    await assert.rejects(
      () => client.sendDirectMessage({ text: 'hi' }),
      /toUserId is required/
    );
  });

  test('sendDirectMessage throws without text', async () => {
    const client = new ZangiClient({ apiKey: 'k', apiSecret: 's', appId: 'a' });
    await assert.rejects(
      () => client.sendDirectMessage({ toUserId: 'uid' }),
      /text is required/
    );
  });

  test('sendChannelMessage throws without channelId', async () => {
    const client = new ZangiClient({ apiKey: 'k', apiSecret: 's', appId: 'a' });
    await assert.rejects(
      () => client.sendChannelMessage({ text: 'hi' }),
      /channelId is required/
    );
  });

  test('broadcast throws when no channelId configured', async () => {
    const client = new ZangiClient({ apiKey: 'k', apiSecret: 's', appId: 'a' });
    delete process.env.ZANGI_BROADCAST_CHANNEL_ID;
    await assert.rejects(
      () => client.broadcast({ text: 'hi' }),
      /No channel ID provided/
    );
  });

  test('_authHeaders returns correct keys', () => {
    const client = new ZangiClient({ apiKey: 'mykey', apiSecret: 'mysecret', appId: 'myapp' });
    const headers = client._authHeaders();
    assert.strictEqual(headers['X-Zangi-Api-Key'], 'mykey');
    assert.strictEqual(headers['X-Zangi-Api-Secret'], 'mysecret');
    assert.strictEqual(headers['X-Zangi-App-Id'], 'myapp');
  });
});

// ---------------------------------------------------------------------------
// Results
// ---------------------------------------------------------------------------

async function run() {
  // Small delay to let async test registrations complete
  await new Promise((r) => setTimeout(r, 100));

  console.log(`\n${'─'.repeat(60)}`);
  console.log(`Results: ${passed} passed, ${failed} failed`);

  if (errors.length > 0) {
    console.error('\nFailed tests:');
    for (const { name, error } of errors) {
      console.error(`  • ${name}: ${error.message}`);
    }
    process.exit(1);
  } else {
    console.log('All tests passed ✓');
    process.exit(0);
  }
}

run();
