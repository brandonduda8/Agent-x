/**
 * Agent: Data Aggregator
 * Responsibility: Enrich, normalize, and summarize datasets.
 * Revenue use: price tracking, sourcing leads, market signals.
 */

const axios = require('axios');

function respond(envelope) {
  const out = JSON.stringify(envelope);
  process.stdout.write(out + '\n');
}

async function fetchMany(urls, limit) {
  limit = limit || 10;
  const results = [];
  for (const url of (urls || []).slice(0, limit)) {
    try {
      const resp = await axios.get(url, { timeout: 10000 });
      results.push({ url: url, ok: true, status: resp.status });
    } catch (e) {
      results.push({ url: url, ok: false, error: e.message });
    }
  }
  return results;
}

function summarize(fetched) {
  const ok = fetched.filter(function(x){ return x.ok; }).length;
  const failed = fetched.filter(function(x){ return !x.ok; }).length;
  return { ok: ok, failed: failed, total: fetched.length };
}

async function run(action, payload) {
  payload = payload || {};
  try {
    if (action === 'aggregate') {
      const sourceUrls = Array.isArray(payload.sourceUrls) ? payload.sourceUrls : [];
      const fetched = await fetchMany(sourceUrls, 10);
      const summary = summarize(fetched);
      return {
        ok: true,
        result: {
          summary: summary,
          fetched: fetched,
          meta: { metric: payload.metric || 'enriched', timeWindow: payload.timeWindow || '24h' }
        }
      };
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
