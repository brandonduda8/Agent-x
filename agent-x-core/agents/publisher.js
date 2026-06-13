/**
 * Agent: Publisher
 * Responsibility: Deliver approved assets to external endpoints.
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');

function respond(envelope) {
  const out = JSON.stringify(envelope);
  process.stdout.write(out + '\n');
}

function loadArtifact(artifactId) {
  const file = path.join(__dirname, '..', '..', 'digital-twin', 'artifacts', artifactId + '.json');
  if (!fs.existsSync(file)) return null;
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function buildBody(content) {
  if (!content) return null;
  return {
    title: content.title,
    body: content.body,
    tags: content.tags || [],
    outline: content.outline || []
  };
}

async function publishTo(platform, credentials, artifactId) {
  const asset = loadArtifact(artifactId);
  if (!asset) throw new Error('Artifact not found');
  const body = buildBody(asset);
  if (!body) throw new Error('No publishable content derived from artifact');

  let destination;
  if (platform === 'webhook') {
    destination = { url: credentials.endpoint };
  } else if (platform === 'api') {
    destination = { url: credentials.endpoint, headers: credentials.headers || {} };
  } else {
    throw new Error('Unsupported platform: ' + platform);
  }

  const res = await axios.post(destination.url, body, {
    headers: { 'Content-Type': 'application/json', ...(destination.headers || {}) },
    timeout: 20000,
    validateStatus: function() { return true; }
  });
  return {
    platform: platform,
    receivedUrl: destination.url,
    status: res.status,
    response: res.data
  };
}

async function run(action, payload) {
  payload = payload || {};
  try {
    if (action === 'publish') {
      const receipt = await publishTo(payload.platform, payload.credentials || {}, payload.artifactId);
      return { ok: true, result: receipt };
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
