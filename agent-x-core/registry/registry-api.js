/**
 * registry-api.js
 * =============================================================================
 * Express router that exposes the Agent Registry over HTTP.
 *
 * Mounted at:  /v1/registry  (see agent-x-core/index.js)
 *
 * ─── Endpoints ──────────────────────────────────────────────────────────────
 *
 *   GET    /agents              List all agents (optional ?status= filter)
 *   POST   /agents/register     Register a new agent
 *   POST   /agents/:id/heartbeat  Record a heartbeat
 *   PATCH  /agents/:id          Update agent metadata
 *   DELETE /agents/:id          Deregister an agent
 *   GET    /agents/:id          Get a single agent
 * =============================================================================
 */

'use strict';

const express  = require('express');
const router   = express.Router();
const registry = require('./agent-registry');

// ---------------------------------------------------------------------------
// Helper
// ---------------------------------------------------------------------------

function asyncHandler(fn) {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}

// ---------------------------------------------------------------------------
// GET /agents
// ---------------------------------------------------------------------------
router.get('/agents', asyncHandler(async (req, res) => {
  const { status } = req.query;
  const agents = registry.listAgents(status || undefined);
  res.json({ ok: true, count: agents.length, agents });
}));

// ---------------------------------------------------------------------------
// POST /agents/register
// ---------------------------------------------------------------------------
router.post('/agents/register', asyncHandler(async (req, res) => {
  const { name, type, capabilities, meta } = req.body || {};

  if (!name) {
    return res.status(400).json({ ok: false, error: '"name" is required' });
  }

  let agent;
  try {
    agent = registry.registerAgent({ name, type, capabilities, meta });
  } catch (err) {
    return res.status(409).json({ ok: false, error: err.message });
  }

  res.status(201).json({ ok: true, agent });
}));

// ---------------------------------------------------------------------------
// GET /agents/:id
// ---------------------------------------------------------------------------
router.get('/agents/:id', asyncHandler(async (req, res) => {
  const agent = registry.getAgent(req.params.id);
  if (!agent) return res.status(404).json({ ok: false, error: 'Agent not found' });
  res.json({ ok: true, agent });
}));

// ---------------------------------------------------------------------------
// POST /agents/:id/heartbeat
// ---------------------------------------------------------------------------
router.post('/agents/:id/heartbeat', asyncHandler(async (req, res) => {
  let agent;
  try {
    agent = registry.heartbeat(req.params.id);
  } catch (err) {
    return res.status(404).json({ ok: false, error: err.message });
  }
  res.json({ ok: true, agent });
}));

// ---------------------------------------------------------------------------
// PATCH /agents/:id
// ---------------------------------------------------------------------------
router.patch('/agents/:id', asyncHandler(async (req, res) => {
  const updates = req.body || {};
  let agent;
  try {
    agent = registry.updateAgent(req.params.id, updates);
  } catch (err) {
    return res.status(404).json({ ok: false, error: err.message });
  }
  res.json({ ok: true, agent });
}));

// ---------------------------------------------------------------------------
// DELETE /agents/:id
// ---------------------------------------------------------------------------
router.delete('/agents/:id', asyncHandler(async (req, res) => {
  const removed = registry.deregisterAgent(req.params.id);
  if (!removed) return res.status(404).json({ ok: false, error: 'Agent not found' });
  res.json({ ok: true, removed: true });
}));

// ---------------------------------------------------------------------------
// Error handler
// ---------------------------------------------------------------------------
// eslint-disable-next-line no-unused-vars
router.use((err, _req, res, _next) => {
  console.error('[registry-api]', err);
  res.status(500).json({ ok: false, error: err.message || 'Internal error' });
});

module.exports = router;
