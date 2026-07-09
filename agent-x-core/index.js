/**
 * Agent X — Command Center (agent-x-core)
 * =============================================================================
 * Express 5 server, Port 3000 (default).
 *
 * Routes
 * ──────
 * GET  /health          — liveness probe
 * POST /v1/tasks        — submit a task to the orchestrator
 * GET  /v1/status       — overall system status
 *
 * GET    /api/agents                        — list agents
 * POST   /api/agents                        — register agent
 * GET    /api/agents/:id                    — get agent
 * PATCH  /api/agents/:id                    — update agent
 * DELETE /api/agents/:id                    — remove agent
 * POST   /api/agents/:id/heartbeat          — liveness ping
 * GET    /api/agents/heartbeat/summary      — registry-wide counts
 * =============================================================================
 */

'use strict';

require('dotenv').config();

const express  = require('express');
const cors     = require('cors');
const { v4: uuidv4 } = require('uuid');
const path     = require('path');
const fs       = require('fs');

// Internal modules
const agentsRouter  = require('./routes/agents');
const hbMonitor     = require('./registry/heartbeat-monitor');

// --------------------------------------------------------------------------- #
// App setup
// --------------------------------------------------------------------------- #
const app  = express();
const PORT = parseInt(process.env.PORT || '3000', 10);

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// --------------------------------------------------------------------------- #
// Request logger (dev-friendly one-liner per request)
// --------------------------------------------------------------------------- #
app.use((req, _res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.originalUrl}`);
  next();
});

// --------------------------------------------------------------------------- #
// Health check
// --------------------------------------------------------------------------- #
app.get('/health', (_req, res) => {
  res.json({
    ok      : true,
    service : 'agent-x-core',
    port    : PORT,
    uptime  : process.uptime(),
    time    : new Date().toISOString(),
  });
});

// --------------------------------------------------------------------------- #
// Task submission  (stub — wires into orchestrator)
// --------------------------------------------------------------------------- #
app.post('/v1/tasks', (req, res) => {
  const { type, payload } = req.body || {};

  if (!type) {
    return res.status(422).json({ ok: false, error: '"type" is required' });
  }

  const task = {
    id        : uuidv4(),
    type,
    payload   : payload || {},
    status    : 'queued',
    created_at: new Date().toISOString(),
  };

  // Persist to tasks.json
  try {
    const tasksPath = path.resolve(__dirname, 'tasks.json');
    let tasks = [];
    try { tasks = JSON.parse(fs.readFileSync(tasksPath, 'utf8')); } catch (_) {}
    if (!Array.isArray(tasks)) tasks = [];
    tasks.push(task);
    fs.writeFileSync(tasksPath, JSON.stringify(tasks, null, 2), 'utf8');
  } catch (e) {
    console.error('[tasks] Could not persist task:', e.message);
  }

  res.status(201).json({ ok: true, data: { task } });
});

// --------------------------------------------------------------------------- #
// System status
// --------------------------------------------------------------------------- #
app.get('/v1/status', (_req, res) => {
  const summary = hbMonitor.summary();
  res.json({
    ok     : true,
    data   : {
      service  : 'agent-x-core',
      uptime   : process.uptime(),
      time     : new Date().toISOString(),
      registry : summary,
      monitor  : {
        running   : hbMonitor.isRunning,
        tickCount : hbMonitor.tickCount,
        intervalMs: hbMonitor.intervalMs,
        staleMs   : hbMonitor.staleMs,
      },
    },
  });
});

// --------------------------------------------------------------------------- #
// Agent Registry routes
// --------------------------------------------------------------------------- #
app.use('/api/agents', agentsRouter);

// --------------------------------------------------------------------------- #
// 404 fallback
// --------------------------------------------------------------------------- #
app.use((_req, res) => {
  res.status(404).json({ ok: false, error: 'Route not found' });
});

// --------------------------------------------------------------------------- #
// Global error handler
// --------------------------------------------------------------------------- #
// eslint-disable-next-line no-unused-vars
app.use((err, _req, res, _next) => {
  console.error('[error]', err);
  res.status(500).json({ ok: false, error: err.message || 'Internal server error' });
});

// --------------------------------------------------------------------------- #
// Start
// --------------------------------------------------------------------------- #
const server = app.listen(PORT, () => {
  console.log(`[agent-x-core] Listening on port ${PORT}`);

  // Start heartbeat monitor once the server is up
  hbMonitor.start();

  hbMonitor.on('stale', ({ agents }) => {
    console.warn(
      `[heartbeat-monitor] ⚠️  ${agents.length} agent(s) marked stale:`,
      agents.map((a) => `${a.name} (${a.id})`).join(', '),
    );
  });

  hbMonitor.on('error', (e) => {
    console.error('[heartbeat-monitor] Internal error:', e.message);
  });
});

// --------------------------------------------------------------------------- #
// Graceful shutdown
// --------------------------------------------------------------------------- #
const shutdown = (signal) => {
  console.log(`\n[agent-x-core] ${signal} received — shutting down…`);
  hbMonitor.stop();
  server.close(() => {
    console.log('[agent-x-core] Server closed.');
    process.exit(0);
  });
  // Force exit if close hangs
  setTimeout(() => process.exit(1), 5000).unref();
};

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT',  () => shutdown('SIGINT'));

module.exports = { app, server };
