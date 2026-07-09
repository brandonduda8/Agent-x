/**
 * agent-x-core/index.js
 * ──────────────────────
 * Agent X — Command Center
 * Express HTTP server on PORT (default 3000)
 *
 * Subsystems mounted here:
 *  • Agent Registry + Heartbeat  → /api/agents
 *  • Upgrade & Config Versioning → /api/upgrade  (via routes/upgrade.js)
 *  • Hermes Job Discovery        → /api/hermes   (via routes/hermes.js)
 *  • Zangi Communication         → /api/zangi    (via routes/zangi.js)
 *  • Autonomous Build Pipeline   → /pipeline     (NEW)
 *  • WebSocket status stream     → /ws/agent-status (NEW)
 */

'use strict';

require('dotenv').config();

const express    = require('express');
const cors       = require('cors');
const http       = require('http');
const path       = require('path');
const { EventEmitter } = require('events');

// ── shared event bus ──────────────────────────────────────────────────────────
const bus = new EventEmitter();
bus.setMaxListeners(50);

// ── app setup ─────────────────────────────────────────────────────────────────
const app    = express();
const server = http.createServer(app);

app.use(cors());
app.use(express.json({ limit: '2mb' }));
app.use(express.urlencoded({ extended: true }));

// ── registry ──────────────────────────────────────────────────────────────────
let registry;
try {
  registry = require('./registry/agent-registry');
  // propagate registry events onto the shared bus
  if (typeof registry.on === 'function') {
    const REG_EVENTS = ['agent:registered', 'agent:deregistered',
                        'agent:heartbeat',  'agent:stale', 'agent:dead'];
    for (const ev of REG_EVENTS) {
      registry.on(ev, data => bus.emit(ev, data));
    }
  }
} catch (err) {
  console.warn('[core] registry not available:', err.message);
  // Minimal stub so the pipeline can still function in isolation
  registry = {
    list:    () => [],
    getAll:  () => [],
    on:      () => {},
  };
}

// ── existing routes ───────────────────────────────────────────────────────────
try {
  const registryApi = require('./registry/registry-api');
  app.use('/api/agents', registryApi);
} catch (e) { console.warn('[core] registry-api unavailable:', e.message); }

try {
  const upgradeApi = require('./routes/upgrade');
  app.use('/api/upgrade', upgradeApi);
} catch (e) { console.warn('[core] upgrade route unavailable:', e.message); }

try {
  const hermesApi = require('./routes/hermes');
  app.use('/api/hermes', hermesApi);
} catch (e) { console.warn('[core] hermes route unavailable:', e.message); }

try {
  const zangiApi = require('./routes/zangi');
  app.use('/api/zangi', zangiApi);
} catch (e) { console.warn('[core] zangi route unavailable:', e.message); }

// ── pipeline subsystem ────────────────────────────────────────────────────────
const { mountPipeline } = require('./pipeline');

const { pipeline, wsServer, router: pipelineRouter } = mountPipeline({
  app,
  httpServer: server,
  registry,
  bus,
  pollMs:    Number(process.env.PIPELINE_POLL_MS) || 2_000,
  autoStart: process.env.PIPELINE_AUTO_START !== 'false',
});

app.use('/pipeline', pipelineRouter);

// Expose pipeline & bus for use by other modules
app.locals.pipeline  = pipeline;
app.locals.bus       = bus;
app.locals.wsServer  = wsServer;

// ── health / root ─────────────────────────────────────────────────────────────
app.get('/', (req, res) => {
  res.json({
    service:  'agent-x-core',
    status:   'running',
    version:  process.env.npm_package_version || '1.0.0',
    endpoints: {
      agents:   '/api/agents',
      upgrade:  '/api/upgrade',
      hermes:   '/api/hermes',
      zangi:    '/api/zangi',
      pipeline: '/pipeline',
      ws:       wsServer?.path ?? '/ws/agent-status',
    },
  });
});

app.get('/health', (req, res) => {
  res.json({
    ok:       true,
    uptime:   process.uptime(),
    pipeline: pipeline.status().stats,
    ws: {
      available: wsServer?.available ?? false,
      clients:   wsServer?.clientCount ?? 0,
    },
  });
});

// ── 404 handler ───────────────────────────────────────────────────────────────
app.use((req, res) => {
  res.status(404).json({ ok: false, error: 'Not Found', path: req.path });
});

// ── global error handler ──────────────────────────────────────────────────────
// eslint-disable-next-line no-unused-vars
app.use((err, req, res, next) => {
  console.error('[core] unhandled error:', err);
  res.status(500).json({ ok: false, error: err.message });
});

// ── start ─────────────────────────────────────────────────────────────────────
const PORT = Number(process.env.PORT) || 3000;

server.listen(PORT, () => {
  console.log(`[agent-x-core] running on port ${PORT}`);
  console.log(`[agent-x-core] WebSocket: ws://localhost:${PORT}${wsServer?.path ?? '/ws/agent-status'}`);
  console.log(`[agent-x-core] Pipeline:  http://localhost:${PORT}/pipeline/status`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('[agent-x-core] SIGTERM — shutting down');
  pipeline.stop();
  wsServer?.close();
  server.close(() => process.exit(0));
});

process.on('SIGINT', () => {
  console.log('[agent-x-core] SIGINT — shutting down');
  pipeline.stop();
  wsServer?.close();
  server.close(() => process.exit(0));
});

module.exports = { app, server, pipeline, bus, wsServer };
