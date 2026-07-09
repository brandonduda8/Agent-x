/**
 * Agent X Core — Command Center
 * Port: 3000
 *
 * Express API server for task routing, agent orchestration,
 * registry management, upgrade management, and Zangi messaging.
 */

'use strict';

require('dotenv').config();

const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// ---------------------------------------------------------------------------
// Middleware
// ---------------------------------------------------------------------------

app.use(cors());

// Note: /api/zangi/webhook uses its own rawBodyCapture middleware and must NOT
// be pre-parsed by express.json(). We apply JSON parsing only to other routes.
app.use((req, res, next) => {
  // Skip JSON body parsing for the Zangi webhook path — it does its own.
  if (req.path === '/api/zangi/webhook' || req.path === '/v1/zangi/webhook') {
    return next();
  }
  express.json()(req, res, next);
});

app.use(express.urlencoded({ extended: true }));

// ---------------------------------------------------------------------------
// Health / root
// ---------------------------------------------------------------------------

app.get('/', (req, res) => {
  res.json({
    service: 'agent-x-core',
    status: 'running',
    port: PORT,
    version: process.env.npm_package_version || '1.0.0',
  });
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});

// ---------------------------------------------------------------------------
// Routes
// ---------------------------------------------------------------------------

// Agent registry REST API
try {
  const registryApi = require('./registry/registry-api');
  app.use('/v1/registry', registryApi);
  console.info('[Core] Mounted registry API at /v1/registry');
} catch (err) {
  console.warn('[Core] Registry API not loaded:', err.message);
}

// Upgrade & config versioning API
try {
  const upgradeApi = require('./routes/upgrade');
  app.use('/v1/upgrade', upgradeApi);
  console.info('[Core] Mounted upgrade API at /v1/upgrade');
} catch (err) {
  console.warn('[Core] Upgrade API not loaded:', err.message);
}

// Agent routes
try {
  const agentsRoute = require('./routes/agents');
  app.use('/v1/agents', agentsRoute);
  console.info('[Core] Mounted agents route at /v1/agents');
} catch (err) {
  console.warn('[Core] Agents route not loaded:', err.message);
}

// ────────────────────────────────────────────────────────────────────────────
// Zangi Communication Layer
// ────────────────────────────────────────────────────────────────────────────
try {
  const zangiRouter = require('./routes/zangi');
  app.use('/api/zangi', zangiRouter);
  // Also expose under versioned path for consistency
  app.use('/v1/zangi', zangiRouter);
  console.info('[Core] ✓ Mounted Zangi API at /api/zangi and /v1/zangi');
} catch (err) {
  console.error('[Core] ✗ Failed to mount Zangi API:', err.message);
}
// ────────────────────────────────────────────────────────────────────────────

// ---------------------------------------------------------------------------
// Task API (internal use — agents post results here)
// ---------------------------------------------------------------------------

// Simple in-memory task store (replace with lowdb / db.json in production)
const tasks = new Map();

app.get('/v1/tasks', (req, res) => {
  res.json({ tasks: [...tasks.values()] });
});

app.get('/v1/tasks/:id', (req, res) => {
  const task = tasks.get(req.params.id);
  if (!task) return res.status(404).json({ error: 'Task not found' });
  return res.json(task);
});

app.post('/v1/tasks', (req, res) => {
  const task = req.body;
  if (!task || !task.id) {
    return res.status(400).json({ error: 'Task must have an id' });
  }
  tasks.set(task.id, { ...task, receivedAt: new Date().toISOString() });
  console.info(`[Core] Received task ${task.id} (type: ${task.type})`);
  res.status(201).json({ ok: true, taskId: task.id });
});

// ---------------------------------------------------------------------------
// 404 handler
// ---------------------------------------------------------------------------

app.use((req, res) => {
  res.status(404).json({ error: 'Not found', path: req.path });
});

// ---------------------------------------------------------------------------
// Error handler
// ---------------------------------------------------------------------------

app.use((err, req, res, next) => {
  console.error('[Core] Unhandled error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------

app.listen(PORT, () => {
  console.info(`[Core] ✓ agent-x-core running on http://0.0.0.0:${PORT}`);
});

module.exports = app;
