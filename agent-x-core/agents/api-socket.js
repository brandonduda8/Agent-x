/**
 * Agent: API Socket
 * Responsibility: Manage all outbound HTTP API connections.
 * Pattern: Single executable with stdio JSON protocol, accepts requests
 * from orchestrator or cron and returns a compact result envelope.
 */

const axios = require('axios');
const fs = require('fs');

function respond(envelope) {
  const out = JSON.stringify(envelope);
  process.stdout.write(out + '\n');
}

async function fetchOrThrow(url, opts) {
  opts = opts || {};
  const res = await axios.get(url, { timeout: 15000, ...opts });
  return {
    status: res.status,
    headers: res.headers,
    data: res.data,
    source: { kind: 'http', method: 'get', url: url }
  };
}

async function postJSON(url, body, headers) {
  headers = headers || {};
  const res = await axios.post(url, body, {
    headers: { 'Content-Type': 'application/json', ...headers },
    timeout: 20000
  });
  return {
    status: res.status,
    headers: res.headers,
    data: res.data,
    source: { kind: 'http', method: 'post', url: url }
  };
}

async function run(action, payload) {
  payload = payload || {};
  try {
    let result;
    switch (action) {
      case 'get':
        result = await fetchOrThrow(payload.url);
        break;
      case 'post':
        result = await postJSON(payload.url, payload.body, payload.headers);
        break;
      case 'health':
        return { ok: true };
      default:
        throw new Error('Unknown action: ' + action);
    }
    return result;
  } catch (err) {
    return {
      ok: false,
      error: {
        message: err.message,
        code: err.code,
        status: err.response ? err.response.status : null
      }
    };
  }
}

process.stdin.setEncoding('utf8');
let buffer = '';
process.stdin.on('data', function(chunk) {
  buffer += chunk;
  while (buffer.indexOf('\n') !== -1) {
    const line = buffer.slice(0, buffer.indexOf('\n'));
    buffer = buffer.slice(buffer.indexOf('\n') + 1);
    if (!line.trim()) continue;
    let envelope;
    try {
      envelope = JSON.parse(line);
    } catch (e) {
      respond({ ok: false, error: 'Invalid JSON input' });
      continue;
    }
    const action = envelope.action;
    const payload = envelope.payload || {};
    const requestId = envelope.requestId || null;
    run(action, payload).then(function(result) {
      respond({ ok: true, requestId: requestId, result: result });
    });
  }
});
