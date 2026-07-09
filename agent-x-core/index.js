/**
 * agent-x-core/index.js
 * =============================================================================
 * Command Center — Express HTTP API  (Port 3000)
 *
 * Mounts:
 *   /v1/registry  — Agent registry REST API  (agent registration, heartbeats)
 *   /api/agents   — Upgrade & config-versioning API
 *   /api          — General agent route (agents.js)
 *   /health       — Liveness probe
 * =============================================================================
 */

'use strict';

require('dotenv').config();

const express  = require('express');
const cors     = require('cors');
const path     = require('path');

const app  = express();
const PORT = process.env.PORT || 3000;

// ---------------------------------------------------------------------------
// Global middleware
// ---------------------------------------------------------------------------

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// Request logger (lightweight)
app.use((req, _res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
  next();
});

// ---------------------------------------------------------------------------
// Routes
// ---------------------------------------------------------------------------

// Liveness probe
app.get('/health', (_req, res) => {
  res.json({ ok: true, service: 'agent-x-core', ts: new Date().toISOString() });
});

// Agent registry  (registration, heartbeat, list, deregister)
try {
  const registryRouter = require('./registry/registry-api');
  app.use('/v1/registry', registryRouter);
  console.log('[index] Mounted /v1/registry');
} catch (err) {
  console.warn('[index] registry-api not available:', err.message);
}

// Upgrade & config-versioning API
// Handles /api/agents/:id/upgrade, /api/agents/:id/configs, /api/audit, etc.
try {
  const upgradeRouter = require('./routes/upgrade');
  app.use('/api/agents', upgradeRouter);
  // Also expose audit at top-level /api/audit for convenience
  app.use('/api', upgradeRouter);
  console.log('[index] Mounted /api/agents (upgrade + config versioning)');
} catch (err) {
  console.warn('[index] upgrade router not available:', err.message);
}

// General agents route
try {
  const agentsRouter = require('./routes/agents');
  app.use('/api/agents', agentsRouter);
  console.log('[index] Mounted /api/agents (general)');
} catch (err) {
  console.warn('[index] agents route not available:', err.message);
}

// ---------------------------------------------------------------------------
// Heartbeat monitor — start on boot
// ---------------------------------------------------------------------------

try {
  const HeartbeatMonitor = require('./registry/heartbeat-monitor');
  const registry         = require('./registry/agent-registry');

  const monitor = new HeartbeatMonitor();

  // When an agent goes dead, log it (watchdog can subscribe separately)
  monitor.onDead(agent => {
    console.error(`[heartbeat] DEAD: ${agent.name} (${agent.id})`);
  });

  monitor.start();
} catch (err) {
  console.warn('[index] Heartbeat monitor not started:', err.message);
}

// ---------------------------------------------------------------------------
// 404 / global error handler
// ---------------------------------------------------------------------------

app.use((_req, res) => {
  res.status(404).json({ ok: false, error: 'Not found' });
});

// eslint-disable-next-line no-unused-vars
app.use((err, _req, res, _next) => {
  console.error('[index] Unhandled error:', err);
  res.status(500).json({ ok: false, error: err.message || 'Internal server error' });
});

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------

app.listen(PORT, () => {
  console.log(`[agent-x-core] Listening on port ${PORT}`);
  console.log(`  Health : http://localhost:${PORT}/health`);
  console.log(`  Registry: http://localhost:${PORT}/v1/registry/agents`);
  console.log(`  Upgrade : http://localhost:${PORT}/api/agents/:id/upgrade`);
  console.log(`  Audit   : http://localhost:${PORT}/api/agents/audit`);
});

module.exports = app;
