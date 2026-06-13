/**
 * Agent: Orchestrator
 * Responsibility: run other agents in sequence with inputs and outputs.
 * Revenue pattern: multi-pipeline campaigns without manual coordination.
 */

const { spawn } = require('child_process');
const path = require('path');

function respond(envelope) {
  const out = JSON.stringify(envelope);
  process.stdout.write(out + '\n');
}

function runAgent(scriptName, envelope) {
  return new Promise(function(resolve) {
    const script = path.join(__dirname, scriptName);
    const child = spawn(process.execPath, [script], { stdio: ['pipe', 'pipe', 'inherit'] });
    const out = {};
    let buffer = '';
    child.stdout.on('data', function(chunk) {
      buffer += chunk.toString();
      while (buffer.indexOf('\n') !== -1) {
        const line = buffer.slice(0, buffer.indexOf('\n'));
        buffer = buffer.slice(buffer.indexOf('\n') + 1);
        if (!line.trim()) continue;
        const parsed = JSON.parse(line);
        if (parsed && parsed.ok && parsed.requestId === envelope.requestId) {
          child.kill();
          resolve({ script: scriptName, exit: 'ok', result: parsed.result });
          return;
        }
      }
    });
    child.stdin.write(JSON.stringify(envelope) + '\n');
    child.stderr.on('data', function(d) { console.error('[orchestrator:' + scriptName + '] ' + d.toString()); });
    child.on('error', function(err) { resolve({ script: scriptName, exit: 'error', error: err.message }); });
    setTimeout(function() {
      try { child.kill(); } catch (e) {}
      resolve({ script: scriptName, exit: 'timeout', error: 'agent_timeout' });
    }, 120000);
  });
}

async function run(action, payload) {
  payload = payload || {};
  try {
    if (action === 'pipeline') {
      const steps = Array.isArray(payload.steps) ? payload.steps : [];
      const outputs = [];
      for (const step of steps) {
        const result = await runAgent(step.agent, Object.assign({}, step.envelope || {}, { action: step.action, requestId: step.requestId || payload.requestId, payload: step.payload || {} }));
        outputs.push(result);
      }
      return { ok: true, result: { steps: outputs, requestId: payload.requestId } };
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
