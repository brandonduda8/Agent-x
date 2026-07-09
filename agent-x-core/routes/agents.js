/**
 * Agent Registry — Express Router
 * =============================================================================
 * Mounts under /api/agents (wired in agent-x-core/index.js).
 *
 * Endpoints
 * ─────────
 * GET    /api/agents                 List all agents (optional ?status= ?type= filters)
 * POST   /api/agents                 Register a new agent
 * GET    /api/agents/:id             Get a single agent
 * PATCH  /api/agents/:id             Partial update of an agent
 * DELETE /api/agents/:id             Remove an agent
 *
 * POST   /api/agents/:id/heartbeat   Agent liveness ping
 * GET    /api/agents/heartbeat/summary  Registry-wide status counts (no :id conflict)
 *
 * All responses follow the project envelope:
 *   Success: { ok: true,  data: <payload> }
 *   Error:   { ok: false, error: <message>, errors?: [...] }
 * =============================================================================
 */

'use strict';

const { Router } = require('express');
const registry   = require('../registry/agent-registry');
const monitor    = require('../registry/heartbeat-monitor');

const router = Router();

// --------------------------------------------------------------------------- #
// Helpers
// --------------------------------------------------------------------------- #

/**
 * Wrap an async route handler so unhandled rejections become 500 responses
 * rather than crashing the process (Express 5 handles this natively, but this
 * explicit wrapper also works correctly under Express 4).
 */
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

/** Send a 200 success envelope. */
const ok = (res, data, status = 200) => res.status(status).json({ ok: true, data });

/** Send an error envelope. */
const err = (res, message, status = 400, extra = {}) =>
  res.status(status).json({ ok: false, error: message, ...extra });

// --------------------------------------------------------------------------- #
// GET /api/agents/heartbeat/summary
// Must be declared BEFORE /:id routes to avoid Express matching "heartbeat"
// as an :id parameter.
// --------------------------------------------------------------------------- #

/**
 * @route GET /api/agents/heartbeat/summary
 * @desc  Returns aggregate status counts for all registered agents.
 *        Also includes monitor configuration (interval, stale threshold).
 */
router.get('/heartbeat/summary', asyncHandler(async (_req, res) => {
  const summary = monitor.summary();
  ok(res, {
    summary,
    monitor: {
      running    : monitor.isRunning,
      tickCount  : monitor.tickCount,
      intervalMs : monitor.intervalMs,
      staleMs    : monitor.staleMs,
    },
  });
}));

// --------------------------------------------------------------------------- #
// GET /api/agents
// --------------------------------------------------------------------------- #

/**
 * @route GET /api/agents
 * @query {string} [status] — filter by status
 * @query {string} [type]   — filter by type
 * @desc  Return a (optionally filtered) list of all registered agents.
 */
router.get('/', asyncHandler(async (req, res) => {
  const filters = {};
  if (req.query.status) filters.status = req.query.status;
  if (req.query.type)   filters.type   = req.query.type;

  const agents = registry.listAgents(filters);
  ok(res, { agents, count: agents.length });
}));

// --------------------------------------------------------------------------- #
// POST /api/agents
// --------------------------------------------------------------------------- #

/**
 * @route POST /api/agents
 * @body  { name, type, capabilities?, status?, current_task_id? }
 * @desc  Register a new agent. Returns the created agent with its assigned id.
 */
router.post('/', asyncHandler(async (req, res) => {
  const result = registry.createAgent(req.body || {});

  if (!result.ok) {
    return err(res, 'Validation failed', 422, { errors: result.errors });
  }

  ok(res, { agent: result.agent }, 201);
}));

// --------------------------------------------------------------------------- #
// GET /api/agents/:id
// --------------------------------------------------------------------------- #

/**
 * @route GET /api/agents/:id
 * @desc  Retrieve a single agent by its UUID.
 */
router.get('/:id', asyncHandler(async (req, res) => {
  const agent = registry.getAgent(req.params.id);

  if (!agent) {
    return err(res, `Agent not found: ${req.params.id}`, 404);
  }

  ok(res, { agent });
}));

// --------------------------------------------------------------------------- #
// PATCH /api/agents/:id
// --------------------------------------------------------------------------- #

/**
 * @route PATCH /api/agents/:id
 * @body  { name?, type?, capabilities?, status?, current_task_id? }
 * @desc  Partially update a registered agent. Immutable fields (id, created_at)
 *        are rejected with 422.
 */
router.patch('/:id', asyncHandler(async (req, res) => {
  const result = registry.updateAgent(req.params.id, req.body || {});

  if (result.notFound) {
    return err(res, `Agent not found: ${req.params.id}`, 404);
  }
  if (!result.ok) {
    return err(res, 'Validation failed', 422, { errors: result.errors });
  }

  ok(res, { agent: result.agent });
}));

// --------------------------------------------------------------------------- #
// DELETE /api/agents/:id
// --------------------------------------------------------------------------- #

/**
 * @route DELETE /api/agents/:id
 * @desc  Remove an agent from the registry permanently.
 */
router.delete('/:id', asyncHandler(async (req, res) => {
  const result = registry.deleteAgent(req.params.id);

  if (result.notFound) {
    return err(res, `Agent not found: ${req.params.id}`, 404);
  }

  ok(res, { deleted: true, id: req.params.id });
}));

// --------------------------------------------------------------------------- #
// POST /api/agents/:id/heartbeat
// --------------------------------------------------------------------------- #

/**
 * @route POST /api/agents/:id/heartbeat
 * @body  { status?, current_task_id? }  — all optional
 * @desc  Record a liveness ping from an agent.
 *
 *        The agent should call this endpoint every ~30 s.
 *        If the monitor hasn't seen a heartbeat within HEARTBEAT_STALE_MS (default 60 s),
 *        it will automatically demote the agent to "stale" on the next tick.
 *
 *        A 200 response carries the updated agent record plus the server's
 *        current timestamp so agents can detect clock skew.
 */
router.post('/:id/heartbeat', asyncHandler(async (req, res) => {
  const result = registry.recordHeartbeat(req.params.id, req.body || {});

  if (result.notFound) {
    return err(res, `Agent not found: ${req.params.id}`, 404);
  }
  if (!result.ok) {
    return err(res, 'Heartbeat validation failed', 422, { errors: result.errors });
  }

  ok(res, {
    agent        : result.agent,
    server_time  : new Date().toISOString(),
    next_expected: new Date(Date.now() + monitor.intervalMs).toISOString(),
  });
}));

// --------------------------------------------------------------------------- #
// 404 catch-all for unrecognised sub-paths under /api/agents
// --------------------------------------------------------------------------- #
router.use((req, res) => {
  err(res, `Unknown agent route: ${req.method} ${req.path}`, 404);
});

module.exports = router;
