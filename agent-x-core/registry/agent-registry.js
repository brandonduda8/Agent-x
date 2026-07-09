/**
 * agent-registry.js
 * =============================================================================
 * Central registry for all active agents.
 *
 * Responsibilities:
 *   • Store agent metadata (id, name, type, capabilities, status, heartbeat)
 *   • Expose CRUD helpers used by registry-api / upgrade-manager / watchdog
 *   • Persist state to memory/registry.json on every mutation
 *   • Fire optional restart callbacks registered by external consumers
 *     (watchdog, upgrade-manager) so the upgrade system can trigger
 *     graceful agent restarts without a direct PM2 dependency
 *
 * Agent lifecycle states:
 *   registered → active → stale → dead
 *                  ↑        │
 *                  └────────┘  (re-heartbeat recovers to active)
 * =============================================================================
 */

'use strict';

const fs   = require('fs');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

// ---------------------------------------------------------------------------
// Storage path
// ---------------------------------------------------------------------------

const REGISTRY_FILE = path.resolve(__dirname, '../../memory/registry.json');

// ---------------------------------------------------------------------------
// Ensure the memory/ directory exists
// ---------------------------------------------------------------------------
const _memDir = path.dirname(REGISTRY_FILE);
if (!fs.existsSync(_memDir)) fs.mkdirSync(_memDir, { recursive: true });

// ---------------------------------------------------------------------------
// In-memory agent map  { agentId → agentRecord }
// ---------------------------------------------------------------------------

/** @type {Map<string, object>} */
const _agents = new Map();

/**
 * External restart callbacks registered by watchdog / upgrade-manager.
 * @type {Map<string, Function>}
 */
const _restartCallbacks = new Map();

// ---------------------------------------------------------------------------
// Agent status constants
// ---------------------------------------------------------------------------

const STATUS = Object.freeze({
  REGISTERED: 'registered',
  ACTIVE:     'active',
  STALE:      'stale',
  DEAD:       'dead',
});

// ---------------------------------------------------------------------------
// Persistence helpers
// ---------------------------------------------------------------------------

/**
 * Load registry state from disk (called once at startup).
 */
function _load() {
  try {
    if (!fs.existsSync(REGISTRY_FILE)) return;
    const raw  = fs.readFileSync(REGISTRY_FILE, 'utf8').trim();
    if (!raw) return;
    const data = JSON.parse(raw);
    if (Array.isArray(data.agents)) {
      for (const agent of data.agents) {
        _agents.set(agent.id, agent);
      }
    }
  } catch (err) {
    console.warn('[agent-registry] Failed to load registry.json:', err.message);
  }
}

/**
 * Flush current state to disk.
 */
function _persist() {
  try {
    const payload = { agents: [..._agents.values()], savedAt: new Date().toISOString() };
    fs.writeFileSync(REGISTRY_FILE, JSON.stringify(payload, null, 2), 'utf8');
  } catch (err) {
    console.warn('[agent-registry] Failed to persist registry.json:', err.message);
  }
}

// Boot-time load
_load();

// ---------------------------------------------------------------------------
// Public API — Agent CRUD
// ---------------------------------------------------------------------------

/**
 * Register a new agent.
 *
 * @param {object} params
 * @param {string}   [params.id]           — pre-assigned ID (generated if omitted)
 * @param {string}   params.name
 * @param {string}   [params.type]         — e.g. 'worker', 'orchestrator'
 * @param {string[]} [params.capabilities] — array of capability strings
 * @param {object}   [params.meta]
 * @returns {object} The registered agent record
 */
function registerAgent({ id, name, type = 'worker', capabilities = [], meta = {} }) {
  if (!name) throw new Error('agent-registry: name is required');

  const agentId = id || uuidv4();

  if (_agents.has(agentId)) {
    throw new Error(`agent-registry: agent ${agentId} is already registered`);
  }

  const agent = {
    id:               agentId,
    name,
    type,
    capabilities,
    status:           STATUS.REGISTERED,
    registeredAt:     new Date().toISOString(),
    lastHeartbeat:    null,
    missedHeartbeats: 0,
    meta,
  };

  _agents.set(agentId, agent);
  _persist();
  return agent;
}

/**
 * Retrieve a single agent by ID.
 *
 * @param {string} agentId
 * @returns {object|null}
 */
function getAgent(agentId) {
  return _agents.get(agentId) || null;
}

/**
 * List all agents (optionally filtered by status).
 *
 * @param {string} [statusFilter]
 * @returns {Array<object>}
 */
function listAgents(statusFilter) {
  const all = [..._agents.values()];
  return statusFilter ? all.filter(a => a.status === statusFilter) : all;
}

/**
 * Record a heartbeat for an agent — sets status to `active`.
 *
 * @param {string} agentId
 * @returns {object} Updated agent record
 */
function heartbeat(agentId) {
  const agent = _agents.get(agentId);
  if (!agent) throw new Error(`agent-registry: agent ${agentId} not found`);

  agent.lastHeartbeat    = new Date().toISOString();
  agent.missedHeartbeats = 0;
  agent.status           = STATUS.ACTIVE;

  _persist();
  return agent;
}

/**
 * Mark an agent with a specific status.
 *
 * @param {string} agentId
 * @param {string} status — one of STATUS values
 * @returns {object}
 */
function setStatus(agentId, status) {
  const agent = _agents.get(agentId);
  if (!agent) throw new Error(`agent-registry: agent ${agentId} not found`);
  agent.status = status;
  _persist();
  return agent;
}

/**
 * Increment missed-heartbeat counter for an agent.
 *
 * @param {string} agentId
 * @returns {object}
 */
function incrementMissedHeartbeats(agentId) {
  const agent = _agents.get(agentId);
  if (!agent) throw new Error(`agent-registry: agent ${agentId} not found`);
  agent.missedHeartbeats = (agent.missedHeartbeats || 0) + 1;
  _persist();
  return agent;
}

/**
 * Deregister an agent and remove it from memory.
 *
 * @param {string} agentId
 * @returns {boolean} true if the agent existed and was removed
 */
function deregisterAgent(agentId) {
  if (!_agents.has(agentId)) return false;
  _agents.delete(agentId);
  _restartCallbacks.delete(agentId);
  _persist();
  return true;
}

/**
 * Update arbitrary metadata fields on an agent record.
 *
 * @param {string} agentId
 * @param {object} updates — plain object of fields to merge
 * @returns {object} Updated agent record
 */
function updateAgent(agentId, updates) {
  const agent = _agents.get(agentId);
  if (!agent) throw new Error(`agent-registry: agent ${agentId} not found`);

  // Prevent status/id from being clobbered accidentally
  const { id: _id, registeredAt: _reg, ...safe } = updates;
  Object.assign(agent, safe);

  _persist();
  return agent;
}

// ---------------------------------------------------------------------------
// Restart callback registration (used by upgrade-manager & watchdog)
// ---------------------------------------------------------------------------

/**
 * Register a restart callback for an agent.
 * When upgrade-manager needs to restart an agent it will invoke this callback.
 *
 * @param {string}   agentId
 * @param {Function} fn       — async (agentId) => void
 */
function registerRestartCallback(agentId, fn) {
  if (typeof fn !== 'function') throw new Error('restart callback must be a function');
  _restartCallbacks.set(agentId, fn);
}

/**
 * Trigger the registered restart callback for an agent.
 * Falls back gracefully if no callback is registered.
 *
 * @param {string} agentId
 * @returns {Promise<boolean>} true if a callback was invoked
 */
async function restartAgent(agentId) {
  const cb = _restartCallbacks.get(agentId);
  if (!cb) {
    console.warn(`[agent-registry] No restart callback for agent ${agentId} — restart must be done manually`);
    return false;
  }
  try {
    await Promise.resolve(cb(agentId));
    return true;
  } catch (err) {
    console.error(`[agent-registry] Restart callback failed for ${agentId}:`, err.message);
    return false;
  }
}

// ---------------------------------------------------------------------------
// Exports
// ---------------------------------------------------------------------------

module.exports = {
  STATUS,
  registerAgent,
  getAgent,
  listAgents,
  heartbeat,
  setStatus,
  incrementMissedHeartbeats,
  deregisterAgent,
  updateAgent,
  registerRestartCallback,
  restartAgent,
  // Expose for testing
  _agents,
};
