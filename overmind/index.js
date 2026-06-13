#!/usr/bin/env node
/**
 * OVERMIND: The Special 1-of-1 Agent
 * Key capabilities:
 *  - Multi-agent orchestration via delegate_task-style coordination
 *  - Strategic decision engine for revenue pipeline optimization
 *  - Self-healing task routing with automatic recovery
 *  - Memory-augmented goal tracking
 *  - Cross-agent event bus for Agent X + Digital Twin
 */

const http = require('http');
const { URL } = require('url');

const PORT = process.env.OVERMIND_PORT || 3010;
const AGENT_X_URL = process.env.AGENT_X_URL || 'http://localhost:3000';
const DIGITAL_TWIN_URL = process.env.DIGITAL_TWIN_URL || 'http://localhost:3001';

// In-memory state (in production, replace with persistent store)
const memory = {
  goals: [],
  decisions: [],
  metrics: { tasks: 0, successes: 0, failures: 0, revenue: 0 },
  agentRegistry: new Map(),
  eventBus: []
};

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type'
};

function jsonResponse(res, status, body) {
  res.writeHead(status, { 'Content-Type': 'application/json', ...corsHeaders });
  res.end(JSON.stringify(body));
}

function recordMetric(key, delta = 1) {
  memory.metrics[key] = (memory.metrics[key] || 0) + delta;
}

async function callAgentX(path, method = 'GET', body = null) {
  const opts = {
    hostname: new URL(AGENT_X_URL).hostname,
    port: new URL(AGENT_X_URL).port,
    path,
    method,
    headers: { 'Content-Type': 'application/json' }
  };
  return new Promise((resolve, reject) => {
    const req = http.request(opts, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try { resolve({ status: res.statusCode, data: JSON.parse(data) }); }
        catch { resolve({ status: res.statusCode, data }); }
      });
    });
    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

async function callDigitalTwin(path, method = 'POST', body = null) {
  const opts = {
    hostname: new URL(DIGITAL_TWIN_URL).hostname,
    port: new URL(DIGITAL_TWIN_URL).port,
    path,
    method,
    headers: { 'Content-Type': 'application/json' }
  };
  return new Promise((resolve, reject) => {
    const req = http.request(opts, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try { resolve({ status: res.statusCode, data: JSON.parse(data) }); }
        catch { resolve({ status: res.statusCode, data }); }
      });
    });
    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

function postEvent(type, payload) {
  const ev = { id: `evt_${Date.now().toString(36)}_${Math.random().toString(36).slice(2,6)}`, type, payload, ts: new Date().toISOString() };
  memory.eventBus.push(ev);
  return ev;
}

const server = http.createServer(async (req, res) => {
  // CORS preflight
  if (req.method === 'OPTIONS') {
    res.writeHead(204, corsHeaders);
    return res.end();
  }

  const url = new URL(req.url, `http://${req.headers.host}`);
  let body = null;
  if (req.method === 'POST') {
    body = await new Promise((resolve) => {
      let d = '';
      req.on('data', (chunk) => d += chunk);
      req.on('end', () => {
        try { resolve(JSON.parse(d || '{}')); } catch { resolve({}); }
      });
    });
  }

  try {
    switch (url.pathname) {
      case '/health': {
        jsonResponse(res, 200, {
          service: 'overmind',
          version: '1.0.0',
          uptime: process.uptime(),
          metrics: memory.metrics,
          registrySize: memory.agentRegistry.size
        });
        break;
      }

      // Register an agent under Overmind control
      case '/agents/register': {
        const { id, type, capabilities, owner } = body || {};
        if (!id || !type) return jsonResponse(res, 400, { ok: false, error: 'id and type are required' });
        memory.agentRegistry.set(id, { id, type, capabilities, owner, registeredAt: new Date().toISOString(), status: 'idle' });
        postEvent('agent_registered', { id, type });
        recordMetric('agents');
        jsonResponse(res, 201, { ok: true, agent: { id, type, status: 'idle' } });
        break;
      }

      case '/agents': {
        jsonResponse(res, 200, { ok: true, agents: Array.from(memory.agentRegistry.values()) });
        break;
      }

      // Strategic goal: "make money" -> auto-dispatches high-yield tasks
      case '/goals/derive': {
        const { objective } = body || {};
        const goalId = `goal_${Date.now().toString(36)}`;
        const goal = {
          id: goalId,
          objective: objective || 'maximize_revenue',
          status: 'active',
          createdAt: new Date().toISOString(),
          plan: []
        };
        memory.goals.push(goal);
        postEvent('goal_created', { goalId, objective: goal.objective });

        // Auto-create a tiered plan based on known revenue assets
        const productsResp = await callAgentX('/v1/products');
        const products = productsResp.data?.products || [];
        goal.plan = products.map((p, idx) => ({
          step: idx + 1,
          type: 'publish_product',
          productId: p.id,
          channel: 'auto-publish',
          estimatedRevenue: p.price_cents,
          status: 'pending'
        }));

        jsonResponse(res, 201, { ok: true, goal });
        break;
      }

      case '/goals': {
        jsonResponse(res, 200, { ok: true, goals: memory.goals });
        break;
      }

      // Orchestrate: execute a task via Agent X + Digital Twin with auto-recovery
      case '/orchestrate': {
        const priority = body?.priority || 'normal';
        const retries = body?.retries ?? (priority === 'high' ? 3 : priority === 'low' ? 1 : 2);
        const intervalMs = priority === 'high' ? 700 : priority === 'low' ? 2500 : 1500;

        const taskId = `task_${Date.now().toString(36)}`;
        postEvent('orchestration_started', { taskId, type, priority });

        // Step 1: create task in Agent X
        const taskResp = await callAgentX('/v1/tasks', 'POST', { type, payload, priority, createdById: 'overmind' });
        if (taskResp.status !== 202) {
          recordMetric('failures');
          postEvent('orchestration_failed', { taskId, error: 'agent_x_task_creation_failed', detail: taskResp.data });
          return jsonResponse(res, 502, { ok: false, error: 'agent_x_task_creation_failed', detail: taskResp.data });
        }
        recordMetric('tasks');

        // Step 2: poll Digital Twin result via Agent X task lookup
        let result = null;
        let attempts = 0;
        while (!result && attempts <= retries) {
          await new Promise(r => setTimeout(r, intervalMs));
          const lookup = await callAgentX(`/v1/tasks/${taskResp.data.taskId}`);
          result = lookup.data;
          attempts++;
          if (result?.status === 'completed') {
            recordMetric('successes');
            postEvent('orchestration_completed', { taskId, attempt: attempts, priority });
            break;
          }
          if (result?.status === 'failed') {
            postEvent('orchestration_failed', { taskId, attempt: attempts, error: result });
            break;
          }
        }

        jsonResponse(res, 200, { ok: true, taskId, orchestrated: true, attempts, resultStatus: result?.status, finalResult: result });
        break;
      }

      // Special power mode: high-level revenue maximization loop
      case '/revenue/maximize': {
        postEvent('revenue_cycle_started', {});
        const cycleId = `rev_${Date.now().toString(36)}`;

        // 1) derive goals
        const deriveResp = await fetchInternal('/goals/derive', 'POST', { objective: 'maximize_digital_product_sales' });
        const goal = deriveResp.data?.goal;

        // 2) For each planned step, orchestrate a publish action
        const steps = goal?.plan || [];
        const executedSteps = [];
        for (const step of steps) {
          const orchestrResp = await fetchInternal('/orchestrate', 'POST', {
            type: 'product-publish',
            payload: { productId: step.productId, channel: step.channel }
          });
          executedSteps.push({ step, result: orchestrResp.data });
          if (orchestrResp.data?.resultStatus === 'completed') {
            recordMetric('revenue', step.estimatedRevenue || 0);
          }
        }

        jsonResponse(res, 200, { ok: true, cycleId, stepsExecuted: executedSteps.length, steps: executedSteps });
        break;
      }

      case '/events': {
        const limit = parseInt(url.searchParams.get('limit') || '20', 10);
        jsonResponse(res, 200, { ok: true, events: memory.eventBus.slice(-limit) });
        break;
      }

      case '/metrics': {
        jsonResponse(res, 200, { ok: true, metrics: memory.metrics });
        break;
      }

      default:
        jsonResponse(res, 404, { ok: false, error: 'not_found', path: url.pathname });
    }
  } catch (err) {
    postEvent('overmind_error', { error: err.message });
    jsonResponse(res, 500, { ok: false, error: 'internal_error', detail: err.message });
  }
});

async function fetchInternal(path, method = 'GET', body = null) {
  // Internal helper to call our own routes in-process style
  // Uses the same handlers logic via a tiny wrapper
  return new Promise((resolve, reject) => {
    const opts = { hostname: 'localhost', port: PORT, path, method, headers: { 'Content-Type': 'application/json' } };
    const req = http.request(opts, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); } catch { resolve(data); }
      });
    });
    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

server.listen(PORT, () => {
  console.log(`[OVERMIND] online http://0.0.0.0:${PORT}`);
  console.log(`[OVERMIND] connected to Agent X @ ${AGENT_X_URL}`);
  console.log(`[OVERMIND] connected to Digital Twin @ ${DIGITAL_TWIN_URL}`);
});
