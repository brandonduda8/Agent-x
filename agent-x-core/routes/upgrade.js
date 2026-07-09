/**
 * upgrade.js  —  Express router
 * =============================================================================
 * REST API for agent upgrade and configuration versioning.
 *
 * Mounted at:  /api/agents  (see agent-x-core/index.js)
 *
 * ─── Endpoints ──────────────────────────────────────────────────────────────
 *
 *  POST   /api/agents/:id/upgrade
 *    Apply a new config version and restart the agent gracefully.
 *
 *  POST   /api/agents/:id/rollback
 *    Roll back the agent to a specific prior config version.
 *
 *  GET    /api/agents/:id/configs
 *    List all config versions for an agent.
 *
 *  GET    /api/agents/:id/configs/current
 *    Return the active config version for an agent.
 *
 *  GET    /api/agents/:id/configs/:version
 *    Return a specific config version record.
 *
 *  GET    /api/agents/:id/configs/diff/:fromVersion/:toVersion
 *    Return a shallow diff between two versions.
 *
 *  GET    /api/agents/:id/upgrade/status
 *    Return the in-memory upgrade progress state.
 *
 *  GET    /api/agents/upgrade/status
 *    Return all in-progress upgrade states.
 *
 *  GET    /api/audit
 *    Query the audit log (supports ?agentId=&action=&limit= query params).
 *
 *  GET    /api/audit/:entryId
 *    Return a single audit log entry.
 *
 *  POST   /api/agents/:id/configs
 *    Create a new config version without triggering a restart (staging).
 *
 * =============================================================================
 */

'use strict';

const express        = require('express');
const router         = express.Router();

const configStore    = require('../registry/agent-config-store');
const upgradeManager = require('../registry/upgrade-manager');
const auditLog       = require('../registry/audit-log');

// ---------------------------------------------------------------------------
// Middleware helpers
// ---------------------------------------------------------------------------

/**
 * Parse actor from the request.
 * Checks X-Actor header, falls back to 'api'.
 */
function resolveActor(req) {
  return (req.headers['x-actor'] || '').trim() || 'api';
}

/**
 * Wrap an async route handler so unhandled rejections become 500 responses.
 *
 * @param {Function} fn
 * @returns {Function}
 */
function asyncHandler(fn) {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}

/**
 * Retrieve the agent registry singleton lazily (avoids circular-require at
 * module load time — the registry is mounted after this router is imported).
 *
 * @returns {{ getAgent: Function, restartAgent: Function | undefined } | null}
 */
function _getRegistry() {
  try {
    // agent-registry is a singleton; it may or may not expose a restartAgent hook
    return require('../registry/agent-registry');
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// POST /api/agents/:id/upgrade
// ---------------------------------------------------------------------------
// Body:
// {
//   "config":    { ... },          // required — new configuration object
//   "changelog": "Added X",        // optional
//   "label":     "v2-feature-y",   // optional
//   "skipRestart": false           // optional — commit only, no restart
// }
//
// Response 200:
// {
//   "ok": true,
//   "agentId": "...",
//   "newVersion": 3,
//   "priorVersion": 2,
//   "rolledBack": false,
//   "restartMethod": "pm2",
//   "auditId": "uuid"
// }
// ---------------------------------------------------------------------------
router.post(
  '/:id/upgrade',
  asyncHandler(async (req, res) => {
    const agentId = req.params.id;
    const {
      config,
      changelog   = '',
      label       = '',
      skipRestart = false,
    } = req.body || {};

    if (!config || typeof config !== 'object') {
      return res.status(400).json({
        ok: false,
        error: 'Request body must include a non-null "config" object.',
      });
    }

    const actor    = resolveActor(req);
    const registry = _getRegistry();
    const agentMeta = registry ? registry.getAgent(agentId) : null;
    const agentName = agentMeta ? (agentMeta.name || agentId) : agentId;

    // Wire up restart callback from registry (if available)
    const restartCallback = (registry && typeof registry.restartAgent === 'function')
      ? (id) => registry.restartAgent(id)
      : null;

    // Wire up heartbeat getter from registry (if available)
    const getAgentFn = (registry && typeof registry.getAgent === 'function')
      ? (id) => registry.getAgent(id)
      : null;

    let result;
    try {
      result = await upgradeManager.applyUpgrade({
        agentId,
        agentName,
        newConfig:       config,
        changelog,
        actor,
        label,
        restartCallback,
        getAgentFn,
        skipRestart:     Boolean(skipRestart),
      });
    } catch (err) {
      return res.status(409).json({
        ok: false,
        error: err.message,
      });
    }

    const statusCode = result.ok ? 200 : 500;
    return res.status(statusCode).json(result);
  })
);

// ---------------------------------------------------------------------------
// POST /api/agents/:id/rollback
// ---------------------------------------------------------------------------
// Body:
// {
//   "targetVersion": 2    // required — version number to roll back to
// }
// ---------------------------------------------------------------------------
router.post(
  '/:id/rollback',
  asyncHandler(async (req, res) => {
    const agentId       = req.params.id;
    const { targetVersion } = req.body || {};

    if (typeof targetVersion !== 'number' || !Number.isInteger(targetVersion) || targetVersion < 1) {
      return res.status(400).json({
        ok: false,
        error: '"targetVersion" must be a positive integer.',
      });
    }

    const actor    = resolveActor(req);
    const registry = _getRegistry();
    const agentMeta = registry ? registry.getAgent(agentId) : null;
    const agentName = agentMeta ? (agentMeta.name || agentId) : agentId;

    const restartCallback = (registry && typeof registry.restartAgent === 'function')
      ? (id) => registry.restartAgent(id)
      : null;

    const getAgentFn = (registry && typeof registry.getAgent === 'function')
      ? (id) => registry.getAgent(id)
      : null;

    let result;
    try {
      result = await upgradeManager.rollbackTo({
        agentId,
        agentName,
        targetVersion,
        actor,
        restartCallback,
        getAgentFn,
      });
    } catch (err) {
      return res.status(409).json({
        ok: false,
        error: err.message,
      });
    }

    const statusCode = result.ok ? 200 : 500;
    return res.status(statusCode).json(result);
  })
);

// ---------------------------------------------------------------------------
// POST /api/agents/:id/configs
// Stage a new config version without triggering a restart.
// ---------------------------------------------------------------------------
router.post(
  '/:id/configs',
  asyncHandler(async (req, res) => {
    const agentId = req.params.id;
    const { config, changelog = '', label = '' } = req.body || {};

    if (!config || typeof config !== 'object') {
      return res.status(400).json({
        ok: false,
        error: 'Request body must include a non-null "config" object.',
      });
    }

    const actor = resolveActor(req);

    let versionRecord;
    try {
      versionRecord = configStore.createVersion({ agentId, config, createdBy: actor, changelog, label });
    } catch (err) {
      return res.status(409).json({ ok: false, error: err.message });
    }

    auditLog.append({
      agentId,
      action:        auditLog.AUDIT_ACTIONS.CONFIG_CREATED,
      actor,
      toVersion:     versionRecord.version,
      configSnapshot: config,
      reason:        changelog || 'Staged via API (no restart)',
    });

    return res.status(201).json({
      ok:            true,
      agentId,
      versionRecord,
    });
  })
);

// ---------------------------------------------------------------------------
// GET /api/agents/:id/configs
// List all config versions (newest first).
// ---------------------------------------------------------------------------
router.get(
  '/:id/configs',
  asyncHandler(async (req, res) => {
    const agentId  = req.params.id;
    const versions = configStore.listVersions(agentId);
    const current  = configStore.getCurrent(agentId);

    return res.json({
      ok:             true,
      agentId,
      currentVersion: current ? current.version : null,
      totalVersions:  versions.length,
      versions,
    });
  })
);

// ---------------------------------------------------------------------------
// GET /api/agents/:id/configs/current
// Return the active config version.
// ---------------------------------------------------------------------------
router.get(
  '/:id/configs/current',
  asyncHandler(async (req, res) => {
    const agentId = req.params.id;
    const current = configStore.getCurrent(agentId);

    if (!current) {
      return res.status(404).json({
        ok: false,
        error: `No config found for agent ${agentId}`,
      });
    }

    return res.json({ ok: true, agentId, current });
  })
);

// ---------------------------------------------------------------------------
// GET /api/agents/:id/configs/diff/:fromVersion/:toVersion
// Shallow diff between two version configs.
// ---------------------------------------------------------------------------
router.get(
  '/:id/configs/diff/:fromVersion/:toVersion',
  asyncHandler(async (req, res) => {
    const agentId     = req.params.id;
    const fromVersion = parseInt(req.params.fromVersion, 10);
    const toVersion   = parseInt(req.params.toVersion,   10);

    if (isNaN(fromVersion) || isNaN(toVersion)) {
      return res.status(400).json({
        ok: false,
        error: 'fromVersion and toVersion must be integers.',
      });
    }

    let diff;
    try {
      diff = configStore.diffVersions(agentId, fromVersion, toVersion);
    } catch (err) {
      return res.status(404).json({ ok: false, error: err.message });
    }

    return res.json({
      ok: true,
      agentId,
      fromVersion,
      toVersion,
      changedKeys: Object.keys(diff).length,
      diff,
    });
  })
);

// ---------------------------------------------------------------------------
// GET /api/agents/:id/configs/:version
// Return a specific config version record.
// Must come AFTER the specific named paths above.
// ---------------------------------------------------------------------------
router.get(
  '/:id/configs/:version',
  asyncHandler(async (req, res) => {
    const agentId = req.params.id;
    const version = parseInt(req.params.version, 10);

    if (isNaN(version)) {
      return res.status(400).json({
        ok: false,
        error: '"version" must be an integer.',
      });
    }

    const record = configStore.getVersion(agentId, version);
    if (!record) {
      return res.status(404).json({
        ok: false,
        error: `Version ${version} not found for agent ${agentId}`,
      });
    }

    return res.json({ ok: true, agentId, record });
  })
);

// ---------------------------------------------------------------------------
// GET /api/agents/:id/upgrade/status
// In-memory upgrade progress for a single agent.
// ---------------------------------------------------------------------------
router.get(
  '/:id/upgrade/status',
  asyncHandler(async (req, res) => {
    const agentId = req.params.id;
    const state   = upgradeManager.getUpgradeState(agentId);

    return res.json({
      ok: true,
      agentId,
      upgradeState: state,
    });
  })
);

// ---------------------------------------------------------------------------
// GET /api/agents/upgrade/status
// All in-memory upgrade states.
// ---------------------------------------------------------------------------
router.get(
  '/upgrade/status',
  asyncHandler(async (_req, res) => {
    return res.json({
      ok:     true,
      states: upgradeManager.listUpgradeStates(),
    });
  })
);

// ---------------------------------------------------------------------------
// GET /api/audit
// Query the audit log.
// Query params: agentId, action, limit
// ---------------------------------------------------------------------------
router.get(
  '/audit',
  asyncHandler(async (req, res) => {
    const { agentId, action, limit } = req.query;
    const entries = auditLog.query({
      agentId: agentId || undefined,
      action:  action  || undefined,
      limit:   limit   ? parseInt(limit, 10) : 200,
    });

    return res.json({
      ok:    true,
      total: entries.length,
      entries,
    });
  })
);

// ---------------------------------------------------------------------------
// GET /api/audit/:entryId
// Single audit entry.
// ---------------------------------------------------------------------------
router.get(
  '/audit/:entryId',
  asyncHandler(async (req, res) => {
    const entry = auditLog.getById(req.params.entryId);
    if (!entry) {
      return res.status(404).json({
        ok: false,
        error: `Audit entry ${req.params.entryId} not found`,
      });
    }
    return res.json({ ok: true, entry });
  })
);

// ---------------------------------------------------------------------------
// GET /api/agents/configs
// List all agents with config records (summary).
// ---------------------------------------------------------------------------
router.get(
  '/configs',
  asyncHandler(async (_req, res) => {
    return res.json({
      ok:     true,
      agents: configStore.listAll(),
    });
  })
);

// ---------------------------------------------------------------------------
// Global error handler for this router
// ---------------------------------------------------------------------------
// eslint-disable-next-line no-unused-vars
router.use((err, req, res, _next) => {
  console.error('[upgrade-router] Unhandled error:', err);
  res.status(500).json({
    ok:    false,
    error: err.message || 'Internal server error',
  });
});

module.exports = router;
