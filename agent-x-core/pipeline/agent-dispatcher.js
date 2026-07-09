/**
 * agent-x-core/pipeline/agent-dispatcher.js
 *
 * Bridges HermesPipeline task dispatch to the actual worker agents.
 *
 * Strategy (in order of preference):
 *  1. If the agent record carries an `httpEndpoint`, POST the task there
 *     and wait for a JSON response.
 *  2. If the agent is a stdio-based worker (registered in AGENT_RUNNERS),
 *     spawn it as a child process, write the task to stdin, read stdout.
 *  3. If neither is available, resolve with a simulated result
 *     (graceful degradation — useful in test/dev).
 *
 * Returns a plain object { status, result, agentId, taskId, durationMs }.
 */

'use strict';

const { execFile }  = require('child_process');
const path          = require('path');

// HTTP client (optional — falls back gracefully if not installed)
let axios;
try { axios = require('axios'); } catch { axios = null; }

// ── worker runner map ─────────────────────────────────────────────────────────
// Maps agent `type` → relative path from repo root to the JS runner script.
const AGENTS_DIR = path.resolve(__dirname, '../agents');
const AGENT_RUNNERS = {
  'content-generator': path.join(AGENTS_DIR, 'content-generator.js'),
  'data-aggregator':   path.join(AGENTS_DIR, 'data-aggregator.js'),
  'infrastructure':    path.join(AGENTS_DIR, 'infrastructure.js'),
  'publisher':         path.join(AGENTS_DIR, 'publisher.js'),
  'api-socket':        path.join(AGENTS_DIR, 'api-socket.js'),
  'orchestrator':      path.join(AGENTS_DIR, 'orchestrator.js'),
};

const STDIO_TIMEOUT_MS = 25_000;

// ─────────────────────────────────────────────────────────────────────────────

/**
 * Dispatch a task to an agent.
 *
 * @param {import('./task-queue').Task} task
 * @param {Object}                      agent  – registry agent record
 * @returns {Promise<Object>}                  – { status, result, agentId, taskId, durationMs }
 */
async function dispatch(task, agent) {
  const start = Date.now();

  let result;

  if (agent.httpEndpoint) {
    result = await dispatchHttp(task, agent);
  } else if (AGENT_RUNNERS[agent.type]) {
    result = await dispatchStdio(task, agent);
  } else {
    result = await dispatchSimulated(task, agent);
  }

  return {
    status:     'ok',
    agentId:    agent.id,
    taskId:     task.id,
    durationMs: Date.now() - start,
    ...result,
  };
}

// ── HTTP dispatch ─────────────────────────────────────────────────────────────

async function dispatchHttp(task, agent) {
  if (!axios) {
    throw new Error('axios not installed; cannot dispatch via HTTP');
  }
  const url = `${agent.httpEndpoint}/task`;
  const response = await axios.post(url, {
    taskId:  task.id,
    type:    task.type,
    payload: task.payload,
    meta:    task.meta,
  }, {
    timeout: 28_000,
    headers: { 'Content-Type': 'application/json' },
  });

  return { result: response.data };
}

// ── stdio (child-process) dispatch ────────────────────────────────────────────

function dispatchStdio(task, agent) {
  return new Promise((resolve, reject) => {
    const scriptPath = AGENT_RUNNERS[agent.type];
    const inputJson  = JSON.stringify({
      taskId:  task.id,
      type:    task.type,
      payload: task.payload,
      meta:    task.meta,
    });

    let stdout = '';
    let stderr = '';
    let timedOut = false;

    const child = execFile(
      process.execPath,   // node binary
      [scriptPath],
      { timeout: STDIO_TIMEOUT_MS, env: { ...process.env, TASK_JSON: inputJson } },
      (err, out, err2) => {
        if (timedOut) return;
        if (err) {
          reject(new Error(`stdio agent error: ${err.message} | stderr: ${stderr.slice(0, 300)}`));
          return;
        }
        try {
          const parsed = JSON.parse(out.trim() || '{}');
          resolve({ result: parsed });
        } catch {
          resolve({ result: { raw: out.trim() } });
        }
      }
    );

    if (child.stdin) {
      child.stdin.write(inputJson);
      child.stdin.end();
    }
    if (child.stdout) child.stdout.on('data', d => { stdout += d; });
    if (child.stderr) child.stderr.on('data', d => { stderr += d; });

    setTimeout(() => {
      timedOut = true;
      try { child.kill('SIGTERM'); } catch { /* already dead */ }
      reject(new Error(`stdio agent timed out after ${STDIO_TIMEOUT_MS}ms`));
    }, STDIO_TIMEOUT_MS);
  });
}

// ── simulated dispatch (dev / fallback) ───────────────────────────────────────

async function dispatchSimulated(task, agent) {
  // Simulate a brief processing delay
  await sleep(Math.random() * 200 + 50);
  return {
    result: {
      simulated: true,
      message:   `Task '${task.type}' processed by simulated agent '${agent.name || agent.id}'`,
      taskId:    task.id,
    },
  };
}

// ── util ──────────────────────────────────────────────────────────────────────

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

module.exports = { dispatch, AGENT_RUNNERS };
