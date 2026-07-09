/**
 * Agent Registry
 * =============================================================================
 * Flat-file backed CRUD store for registered agents.
 *
 * Schema per agent record:
 * {
 *   id            : string  (uuid v4)           — immutable after creation
 *   name          : string                       — human-readable display name
 *   type          : string                       — category label (e.g. "worker", "orchestrator")
 *   capabilities  : string[]                     — list of action tokens the agent can handle
 *   status        : "active"|"idle"|"stale"|"offline"
 *   current_task_id : string | null              — task the agent is presently executing
 *   last_heartbeat  : ISO-8601 string | null     — wall-clock time of most-recent ping
 *   created_at      : ISO-8601 string            — immutable creation timestamp
 *   updated_at      : ISO-8601 string            — updated on every write
 * }
 *
 * Persistence: data/agents.json  (read on require, flushed after every mutation)
 * =============================================================================
 */

'use strict';

const fs   = require('fs');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

// --------------------------------------------------------------------------- #
// Storage path
// --------------------------------------------------------------------------- #
const STORE_PATH = path.resolve(__dirname, '../../data/agents.json');

// Allowed status values — used for validation throughout
const VALID_STATUSES = new Set(['active', 'idle', 'stale', 'offline']);

// --------------------------------------------------------------------------- #
// Low-level helpers
// --------------------------------------------------------------------------- #

/**
 * Read the full agents array from disk.
 * Returns [] if the file is missing or malformed (fail-safe).
 * @returns {Object[]}
 */
function _read() {
  try {
    const raw = fs.readFileSync(STORE_PATH, 'utf8');
    const parsed = JSON.parse(raw);
    // Support both { agents: [] } wrapper and bare [] shapes
    if (Array.isArray(parsed)) return parsed;
    if (parsed && Array.isArray(parsed.agents)) return parsed.agents;
    return [];
  } catch (_) {
    return [];
  }
}

/**
 * Flush the agents array to disk atomically (write-then-rename).
 * The { agents: [] } wrapper is preserved for consistency with other data files.
 * @param {Object[]} agents
 */
function _write(agents) {
  const dir   = path.dirname(STORE_PATH);
  const tmp   = path.join(dir, `.agents-${process.pid}.tmp`);
  const payload = JSON.stringify({ agents }, null, 2);

  try {
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(tmp, payload, 'utf8');
    fs.renameSync(tmp, STORE_PATH);
  } catch (err) {
    // Clean up temp file if rename failed
    try { fs.unlinkSync(tmp); } catch (_) {}
    throw err;
  }
}

/** Return a compact ISO-8601 UTC timestamp string. */
function _now() {
  return new Date().toISOString();
}

// --------------------------------------------------------------------------- #
// Validation helpers
// --------------------------------------------------------------------------- #

/**
 * Validate fields supplied when creating a new agent.
 * @param {Object} data
 * @returns {{ valid: boolean, errors: string[] }}
 */
function validateCreatePayload(data) {
  const errors = [];

  if (!data.name || typeof data.name !== 'string' || !data.name.trim()) {
    errors.push('"name" is required and must be a non-empty string');
  }

  if (!data.type || typeof data.type !== 'string' || !data.type.trim()) {
    errors.push('"type" is required and must be a non-empty string');
  }

  if (data.capabilities !== undefined) {
    if (!Array.isArray(data.capabilities)) {
      errors.push('"capabilities" must be an array of strings');
    } else if (data.capabilities.some((c) => typeof c !== 'string')) {
      errors.push('every item in "capabilities" must be a string');
    }
  }

  if (data.status !== undefined && !VALID_STATUSES.has(data.status)) {
    errors.push(`"status" must be one of: ${[...VALID_STATUSES].join(', ')}`);
  }

  return { valid: errors.length === 0, errors };
}

/**
 * Validate fields supplied when updating an existing agent.
 * All fields are optional; only provided fields are validated.
 * @param {Object} data
 * @returns {{ valid: boolean, errors: string[] }}
 */
function validateUpdatePayload(data) {
  const errors = [];

  if (data.name !== undefined) {
    if (typeof data.name !== 'string' || !data.name.trim()) {
      errors.push('"name" must be a non-empty string');
    }
  }

  if (data.type !== undefined) {
    if (typeof data.type !== 'string' || !data.type.trim()) {
      errors.push('"type" must be a non-empty string');
    }
  }

  if (data.capabilities !== undefined) {
    if (!Array.isArray(data.capabilities)) {
      errors.push('"capabilities" must be an array of strings');
    } else if (data.capabilities.some((c) => typeof c !== 'string')) {
      errors.push('every item in "capabilities" must be a string');
    }
  }

  if (data.status !== undefined && !VALID_STATUSES.has(data.status)) {
    errors.push(`"status" must be one of: ${[...VALID_STATUSES].join(', ')}`);
  }

  // Immutable fields — reject attempts to change them
  for (const immutable of ['id', 'created_at']) {
    if (data[immutable] !== undefined) {
      errors.push(`"${immutable}" is immutable and cannot be updated`);
    }
  }

  return { valid: errors.length === 0, errors };
}

// --------------------------------------------------------------------------- #
// Public CRUD API
// --------------------------------------------------------------------------- #

/**
 * Return all registered agents, optionally filtered.
 *
 * @param {Object} [filters={}]
 * @param {string} [filters.status]  — filter by status value
 * @param {string} [filters.type]    — filter by agent type
 * @returns {Object[]}
 */
function listAgents(filters = {}) {
  let agents = _read();

  if (filters.status) {
    agents = agents.filter((a) => a.status === filters.status);
  }
  if (filters.type) {
    agents = agents.filter((a) => a.type === filters.type);
  }

  return agents;
}

/**
 * Look up a single agent by ID.
 * @param {string} id
 * @returns {Object|null}
 */
function getAgent(id) {
  return _read().find((a) => a.id === id) || null;
}

/**
 * Register a new agent.
 *
 * @param {Object} data
 * @param {string}   data.name
 * @param {string}   data.type
 * @param {string[]} [data.capabilities=[]]
 * @param {string}   [data.status="idle"]
 * @param {string|null} [data.current_task_id=null]
 * @returns {{ ok: boolean, agent?: Object, errors?: string[] }}
 */
function createAgent(data) {
  const { valid, errors } = validateCreatePayload(data);
  if (!valid) return { ok: false, errors };

  const now   = _now();
  const agent = {
    id             : uuidv4(),
    name           : data.name.trim(),
    type           : data.type.trim(),
    capabilities   : Array.isArray(data.capabilities)
      ? data.capabilities.map((c) => String(c).trim()).filter(Boolean)
      : [],
    status          : VALID_STATUSES.has(data.status) ? data.status : 'idle',
    current_task_id : data.current_task_id || null,
    last_heartbeat  : null,
    created_at      : now,
    updated_at      : now,
  };

  const agents = _read();
  agents.push(agent);
  _write(agents);

  return { ok: true, agent };
}

/**
 * Partially update an existing agent by ID.
 * Immutable fields (id, created_at) are rejected.
 *
 * @param {string} id
 * @param {Object} data  — fields to update (all optional)
 * @returns {{ ok: boolean, agent?: Object, errors?: string[], notFound?: boolean }}
 */
function updateAgent(id, data) {
  const { valid, errors } = validateUpdatePayload(data);
  if (!valid) return { ok: false, errors };

  const agents = _read();
  const idx    = agents.findIndex((a) => a.id === id);

  if (idx === -1) return { ok: false, notFound: true };

  const existing = agents[idx];
  const mutable  = ['name', 'type', 'capabilities', 'status', 'current_task_id'];

  for (const field of mutable) {
    if (data[field] !== undefined) {
      existing[field] = field === 'capabilities'
        ? data[field].map((c) => String(c).trim()).filter(Boolean)
        : data[field];
    }
  }

  existing.updated_at = _now();
  agents[idx] = existing;
  _write(agents);

  return { ok: true, agent: existing };
}

/**
 * Delete an agent by ID.
 * @param {string} id
 * @returns {{ ok: boolean, notFound?: boolean }}
 */
function deleteAgent(id) {
  const agents  = _read();
  const filtered = agents.filter((a) => a.id !== id);

  if (filtered.length === agents.length) return { ok: false, notFound: true };

  _write(filtered);
  return { ok: true };
}

// --------------------------------------------------------------------------- #
// Heartbeat
// --------------------------------------------------------------------------- #

/**
 * Record a heartbeat for an agent, updating its status and optional task.
 *
 * @param {string} id
 * @param {Object} [payload={}]
 * @param {string} [payload.status]          — new status (optional)
 * @param {string|null} [payload.current_task_id] — current task (optional)
 * @returns {{ ok: boolean, agent?: Object, notFound?: boolean, errors?: string[] }}
 */
function recordHeartbeat(id, payload = {}) {
  const agents = _read();
  const idx    = agents.findIndex((a) => a.id === id);

  if (idx === -1) return { ok: false, notFound: true };

  const agent = agents[idx];
  const now   = _now();

  // Status from heartbeat payload — must be a valid non-stale status
  // (an agent that is heartbeating cannot be 'stale' or 'offline')
  const incomingStatus = payload.status;
  if (incomingStatus !== undefined) {
    if (!VALID_STATUSES.has(incomingStatus)) {
      return {
        ok: false,
        errors: [`"status" must be one of: ${[...VALID_STATUSES].join(', ')}`],
      };
    }
    agent.status = incomingStatus;
  } else {
    // Default: a heartbeating agent is at least 'idle' (not stale/offline)
    if (agent.status === 'stale' || agent.status === 'offline') {
      agent.status = 'idle';
    }
  }

  if (payload.current_task_id !== undefined) {
    agent.current_task_id = payload.current_task_id || null;
  }

  agent.last_heartbeat = now;
  agent.updated_at     = now;
  agents[idx]          = agent;
  _write(agents);

  return { ok: true, agent };
}

/**
 * Mark agents whose last_heartbeat is older than `thresholdMs` as "stale".
 * Agents already "offline" are not touched.
 *
 * @param {number} [thresholdMs=60000]  — age in ms before an agent is stale (default 60 s)
 * @returns {Object[]}  list of agents that were just marked stale
 */
function markStaleAgents(thresholdMs = 60_000) {
  const agents   = _read();
  const cutoff   = Date.now() - thresholdMs;
  const nowStr   = _now();
  const staled   = [];

  for (const agent of agents) {
    if (agent.status === 'offline') continue; // already dead — skip

    const hbTime = agent.last_heartbeat
      ? new Date(agent.last_heartbeat).getTime()
      : null;

    const isStale = hbTime === null        // never sent a heartbeat
      ? agent.status !== 'idle'            //   newly registered idle agents are OK without HB
      : hbTime < cutoff;                   //   otherwise compare against cutoff

    if (isStale && agent.status !== 'stale') {
      agent.status     = 'stale';
      agent.updated_at = nowStr;
      staled.push(agent);
    }
  }

  if (staled.length > 0) _write(agents);

  return staled;
}

// --------------------------------------------------------------------------- #
// Exports
// --------------------------------------------------------------------------- #
module.exports = {
  // CRUD
  listAgents,
  getAgent,
  createAgent,
  updateAgent,
  deleteAgent,
  // Heartbeat
  recordHeartbeat,
  markStaleAgents,
  // Validation (exported so tests and routes can reuse)
  validateCreatePayload,
  validateUpdatePayload,
  VALID_STATUSES,
};
