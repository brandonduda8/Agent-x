/**
 * Agent: Infrastructure
 * Responsibility: Service lifecycle, env validation, network probes.
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const fs = require('fs');
const path = require('path');

const execAsync = promisify(exec);
const HOME = process.env.HOME || process.env.USERPROFILE || '/tmp';
const AGENT_X = path.join(HOME, 'agent-x');

function respond(envelope) {
  const out = JSON.stringify(envelope);
  process.stdout.write(out + '\n');
}

async function startServices(ports, background) {
  ports = ports || [3000, 3001];
  background = background !== false;
  const base = path.join(__dirname, '..');
  const core = path.join(base, 'index.js');
  const twin = path.join(base, '..', 'digital-twin', 'index.js');
  const started = [];
  const failed = [];
  for (const script of [core, twin]) {
    const isCore = String(script).indexOf('agent-x-core') !== -1;
    const port = isCore ? ports[0] : ports[1];
    try {
      const cmd = 'node ' + script;
      if (background) {
        const child = exec(cmd);
        if (child.pid) started.push({ script: script, pid: child.pid, port: port });
      } else {
        const r = await execAsync(cmd, { timeout: 3000 });
        started.push({ script: script, stdout: r.stdout });
      }
    } catch (e) {
      failed.push({ script: script, error: e.message });
    }
  }
  return { ok: true, started: started, failed: failed };
}

async function serviceStatus() {
  const logsDir = path.join(AGENT_X, 'logs');
  let summary = { logsDir: logsDir, exists: fs.existsSync(logsDir) };
  try {
    const { stdout } = await execAsync('lsof -iTCP -sTCP:LISTEN -P 2>/dev/null || true');
    summary.listeners = stdout.split('\n').reduce(function(acc, line) {
      const m = line.match(/\*:(\d+)/);
      if (m) acc.push(Number(m[1]));
      return acc;
    }, []);
  } catch (e) {
    summary.listeners = [];
  }
  return { ok: true, summary: summary };
}

async function envCheck() {
  const checks = {
    NODE_RUNTIME: typeof process.version,
    HOME: process.env.HOME,
    AGENT_X_EXISTS: fs.existsSync(AGENT_X)
  };
  return { ok: true, checks: checks };
}

async function networkProbe(target) {
  target = target || 'https://api.openai.com';
  const start = Date.now();
  try {
    await execAsync('curl -I -s -o /dev/null -w "%{http_code} %{time_total}" ' + target);
    return { ok: true, target: target, durationMs: Date.now() - start };
  } catch (e) {
    return { ok: false, target: target, error: e.message, durationMs: Date.now() - start };
  }
}

async function run(action, payload) {
  payload = payload || {};
  try {
    switch (action) {
      case 'services.start':
        return await startServices(payload.ports, payload.background);
      case 'services.status':
        return await serviceStatus();
      case 'env.check':
        return await envCheck();
      case 'network.probe':
        return await networkProbe(payload.target);
      default:
        return { ok: false, error: 'Unknown action: ' + action };
    }
  } catch (e) {
    return { ok: false, error: { message: e.message, stack: e.stack } };
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
