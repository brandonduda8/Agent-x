/**
 * Agent: Watchdog
 * Responsibility: monitor core/twin health and emit recovery signals.
 */

const http = require('http');

function respond(envelope) {
  const out = JSON.stringify(envelope);
  process.stdout.write(out + '\n');
}

function probe(url) {
  return new Promise(function(resolve) {
    const start = Date.now();
    const request = http.get(url, function(res) {
      let body = '';
      res.on('data', function(chunk) { body += chunk; });
      res.on('end', function() {
        resolve({ ok: true, url: url, status: res.statusCode, latencyMs: Date.now() - start });
      });
    });
    request.on('error', function(err) {
      resolve({ ok: false, url: url, error: err.message, latencyMs: Date.now() - start });
    });
    request.setTimeout(8000, function() {
      request.destroy();
      resolve({ ok: false, url: url, error: 'timeout', latencyMs: Date.now() - start });
    });
  });
}

async function run(action, payload) {
  payload = payload || {};
  try {
    if (action === 'probe') {
      const targets = Array.isArray(payload.targets) ? payload.targets : [];
      const results = [];
      for (const u of targets) { results.push(await probe(u)); }
      return { ok: true, result: { checks: results, at: new Date().toISOString() } };
    }
    return { ok: false, error: 'Unknown action: ' + action };
  } catch (err) {
    return { ok: false, error: err.message };
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
    run(action, payload).then(function(result) {
      respond({ ok: true, requestId: envelope.requestId || null, ...result });
    });
  }
});
