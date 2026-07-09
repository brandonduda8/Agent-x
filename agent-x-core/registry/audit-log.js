/**
 * audit-log.js
 * =============================================================================
 * Persistent audit log for all agent upgrade and configuration change events.
 *
 * Storage: data/upgrade_audit.json (append-only, JSON flat-file).
 *
 * Each entry is an AuditRecord:
 * {
 *   id:          string   — uuid v4
 *   timestamp:   string   — ISO 8601
 *   agentId:     string   — registry agent ID
 *   agentName:   string   — human-readable name
 *   action:      string   — one of AUDIT_ACTIONS
 *   actor:       string   — who triggered (system | user:<name> | api)
 *   fromVersion: number|null
 *   toVersion:   number|null
 *   configSnapshot: object|null  — full config at time of action
 *   outcome:     'success' | 'failure'
 *   reason:      string   — short description / error message
 *   meta:        object   — arbitrary extra context
 * }
 * =============================================================================
 */

'use strict';

const fs   = require('fs');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const AUDIT_ACTIONS = Object.freeze({
  CONFIG_CREATED:  'CONFIG_CREATED',
  CONFIG_UPGRADED: 'CONFIG_UPGRADED',
  CONFIG_ROLLED_BACK: 'CONFIG_ROLLED_BACK',
  AGENT_RESTARTED: 'AGENT_RESTARTED',
  RESTART_FAILED:  'RESTART_FAILED',
  UPGRADE_STARTED: 'UPGRADE_STARTED',
  UPGRADE_ABORTED: 'UPGRADE_ABORTED',
});

const AUDIT_FILE = path.resolve(
  __dirname, '../../data/upgrade_audit.json'
);

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Read the full audit log array from disk.
 * Returns [] if the file is missing or corrupt.
 *
 * @returns {Array<object>}
 */
function _readAll() {
  try {
    if (!fs.existsSync(AUDIT_FILE)) return [];
    const raw = fs.readFileSync(AUDIT_FILE, 'utf8').trim();
    if (!raw) return [];
    return JSON.parse(raw);
  } catch {
    return [];
  }
}

/**
 * Atomically write the full log array back to disk.
 *
 * @param {Array<object>} entries
 */
function _writeAll(entries) {
  const dir = path.dirname(AUDIT_FILE);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(AUDIT_FILE, JSON.stringify(entries, null, 2), 'utf8');
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Append a new audit record.
 *
 * @param {object} params
 * @param {string}        params.agentId
 * @param {string}        params.agentName
 * @param {string}        params.action       — one of AUDIT_ACTIONS values
 * @param {string}        [params.actor]      — defaults to 'system'
 * @param {number|null}   [params.fromVersion]
 * @param {number|null}   [params.toVersion]
 * @param {object|null}   [params.configSnapshot]
 * @param {'success'|'failure'} [params.outcome] — defaults to 'success'
 * @param {string}        [params.reason]
 * @param {object}        [params.meta]
 * @returns {object} The written audit record
 */
function append({
  agentId,
  agentName    = 'unknown',
  action,
  actor        = 'system',
  fromVersion  = null,
  toVersion    = null,
  configSnapshot = null,
  outcome      = 'success',
  reason       = '',
  meta         = {},
}) {
  if (!agentId) throw new Error('audit-log: agentId is required');
  if (!action)  throw new Error('audit-log: action is required');

  const record = {
    id:             uuidv4(),
    timestamp:      new Date().toISOString(),
    agentId,
    agentName,
    action,
    actor,
    fromVersion,
    toVersion,
    configSnapshot,
    outcome,
    reason,
    meta,
  };

  const all = _readAll();
  all.push(record);
  _writeAll(all);

  return record;
}

/**
 * Retrieve all audit entries, most-recent first.
 *
 * @param {object} [filters]
 * @param {string} [filters.agentId]  — filter by agent
 * @param {string} [filters.action]   — filter by action type
 * @param {number} [filters.limit]    — cap result count (default 200)
 * @returns {Array<object>}
 */
function query({ agentId, action, limit = 200 } = {}) {
  let entries = _readAll();

  if (agentId) entries = entries.filter(e => e.agentId === agentId);
  if (action)  entries = entries.filter(e => e.action  === action);

  // Most-recent first
  entries.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

  return entries.slice(0, limit);
}

/**
 * Return a single audit record by id.
 *
 * @param {string} id
 * @returns {object|null}
 */
function getById(id) {
  return _readAll().find(e => e.id === id) || null;
}

/**
 * Purge records older than `maxAgeDays` for a specific agent (or all agents).
 * Useful for housekeeping in long-running deployments.
 *
 * @param {object} [opts]
 * @param {number} [opts.maxAgeDays]  — default 90
 * @param {string} [opts.agentId]     — if omitted, purges across all agents
 * @returns {number} Count of purged entries
 */
function purgeOld({ maxAgeDays = 90, agentId } = {}) {
  const cutoff = Date.now() - maxAgeDays * 86_400_000;
  const all    = _readAll();
  const kept   = all.filter(e => {
    const tooOld = new Date(e.timestamp).getTime() < cutoff;
    const matches = agentId ? e.agentId === agentId : true;
    return !(tooOld && matches);
  });
  _writeAll(kept);
  return all.length - kept.length;
}

// ---------------------------------------------------------------------------
// Exports
// ---------------------------------------------------------------------------

module.exports = {
  AUDIT_ACTIONS,
  append,
  query,
  getById,
  purgeOld,
};
