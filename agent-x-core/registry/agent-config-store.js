/**
 * agent-config-store.js
 * =============================================================================
 * Versioned configuration store for all registered agents.
 *
 * Storage layout  →  data/agent_configs.json
 * ─────────────────────────────────────────
 * {
 *   "<agentId>": {
 *     "currentVersion": 3,
 *     "versions": [
 *       {
 *         "version":    1,
 *         "createdAt":  "ISO8601",
 *         "createdBy":  "system",
 *         "label":      "initial",
 *         "config":     { ... agent config object ... },
 *         "changelog":  "First config"
 *       },
 *       ...
 *     ]
 *   }
 * }
 *
 * Version numbers are monotonically increasing integers starting at 1.
 * The "current" version is the one actively deployed for that agent.
 * All prior versions are retained for rollback and audit purposes.
 * =============================================================================
 */

'use strict';

const fs   = require('fs');
const path = require('path');

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const CONFIG_FILE = path.resolve(
  __dirname, '../../data/agent_configs.json'
);

const MAX_VERSIONS_PER_AGENT = Number(process.env.MAX_CONFIG_VERSIONS) || 50;

// ---------------------------------------------------------------------------
// Internal I/O
// ---------------------------------------------------------------------------

/**
 * Read the entire config store from disk.
 *
 * @returns {Record<string, {currentVersion: number, versions: Array}>}
 */
function _read() {
  try {
    if (!fs.existsSync(CONFIG_FILE)) return {};
    const raw = fs.readFileSync(CONFIG_FILE, 'utf8').trim();
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

/**
 * Persist the entire config store to disk atomically (write-then-rename).
 *
 * @param {object} data
 */
function _write(data) {
  const dir = path.dirname(CONFIG_FILE);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  const tmp = CONFIG_FILE + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2), 'utf8');
  fs.renameSync(tmp, CONFIG_FILE);
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Create the initial (version 1) config record for an agent.
 * Idempotent — if versions already exist, throws to prevent accidental clobber.
 *
 * @param {object} params
 * @param {string} params.agentId
 * @param {string} [params.agentName]
 * @param {object} params.config      — the initial configuration object
 * @param {string} [params.createdBy] — defaults to 'system'
 * @param {string} [params.changelog]
 * @returns {object} The newly created version record
 */
function createInitial({ agentId, agentName = '', config, createdBy = 'system', changelog = 'Initial configuration' }) {
  if (!agentId) throw new Error('agent-config-store: agentId is required');
  if (!config || typeof config !== 'object') throw new Error('agent-config-store: config must be an object');

  const store = _read();

  if (store[agentId] && store[agentId].versions.length > 0) {
    throw new Error(`agent-config-store: configs already exist for agent ${agentId} — use createVersion() to add new versions`);
  }

  const versionRecord = {
    version:   1,
    createdAt: new Date().toISOString(),
    createdBy,
    label:     agentName || agentId,
    config:    structuredClone(config),
    changelog,
  };

  store[agentId] = {
    currentVersion: 1,
    versions: [versionRecord],
  };

  _write(store);
  return versionRecord;
}

/**
 * Add a new config version for an existing agent.
 * The new version number is automatically assigned as max(existing) + 1.
 * Does NOT automatically activate the new version — call `setCurrentVersion`
 * after validation / restart confirmation.
 *
 * @param {object} params
 * @param {string} params.agentId
 * @param {object} params.config      — full config object for this version
 * @param {string} [params.createdBy]
 * @param {string} [params.changelog]
 * @param {string} [params.label]
 * @returns {object} The newly created version record
 */
function createVersion({ agentId, config, createdBy = 'system', changelog = '', label = '' }) {
  if (!agentId) throw new Error('agent-config-store: agentId is required');
  if (!config || typeof config !== 'object') throw new Error('agent-config-store: config must be an object');

  const store = _read();

  // Auto-bootstrap if no record exists yet
  if (!store[agentId]) {
    return createInitial({ agentId, config, createdBy, changelog });
  }

  const existing  = store[agentId].versions;
  const nextVer   = Math.max(...existing.map(v => v.version), 0) + 1;

  const versionRecord = {
    version:   nextVer,
    createdAt: new Date().toISOString(),
    createdBy,
    label:     label || `v${nextVer}`,
    config:    structuredClone(config),
    changelog,
  };

  existing.push(versionRecord);

  // Prune oldest versions if we've exceeded the cap (keep currentVersion safe)
  if (existing.length > MAX_VERSIONS_PER_AGENT) {
    const current = store[agentId].currentVersion;
    // Sort oldest first, remove from front — never remove the active version
    const sorted  = [...existing].sort((a, b) => a.version - b.version);
    const pruned  = sorted.filter(v => v.version !== current);
    const toRemove = pruned.slice(0, existing.length - MAX_VERSIONS_PER_AGENT);
    store[agentId].versions = existing.filter(
      v => !toRemove.some(r => r.version === v.version)
    );
  }

  _write(store);
  return versionRecord;
}

/**
 * Mark a specific version as the "current" active config.
 *
 * @param {string} agentId
 * @param {number} version
 * @returns {object} The activated version record
 */
function setCurrentVersion(agentId, version) {
  const store = _read();
  const entry = store[agentId];
  if (!entry) throw new Error(`agent-config-store: no configs found for agent ${agentId}`);

  const target = entry.versions.find(v => v.version === version);
  if (!target) throw new Error(`agent-config-store: version ${version} not found for agent ${agentId}`);

  entry.currentVersion = version;
  _write(store);
  return target;
}

/**
 * Get the currently-active config for an agent.
 *
 * @param {string} agentId
 * @returns {{ version: number, config: object, createdAt: string } | null}
 */
function getCurrent(agentId) {
  const store = _read();
  const entry = store[agentId];
  if (!entry) return null;
  return entry.versions.find(v => v.version === entry.currentVersion) || null;
}

/**
 * Get a specific version record.
 *
 * @param {string} agentId
 * @param {number} version
 * @returns {object|null}
 */
function getVersion(agentId, version) {
  const store = _read();
  const entry = store[agentId];
  if (!entry) return null;
  return entry.versions.find(v => v.version === version) || null;
}

/**
 * List all version records for an agent, newest first.
 *
 * @param {string} agentId
 * @returns {Array<object>}
 */
function listVersions(agentId) {
  const store = _read();
  const entry = store[agentId];
  if (!entry) return [];
  return [...entry.versions].sort((a, b) => b.version - a.version);
}

/**
 * Return summary metadata for all agents that have config records.
 *
 * @returns {Array<{ agentId: string, currentVersion: number, totalVersions: number, lastUpdated: string }>}
 */
function listAll() {
  const store = _read();
  return Object.entries(store).map(([agentId, entry]) => {
    const sorted = [...entry.versions].sort((a, b) => b.version - a.version);
    return {
      agentId,
      currentVersion: entry.currentVersion,
      totalVersions:  entry.versions.length,
      lastUpdated:    sorted[0]?.createdAt || null,
    };
  });
}

/**
 * Delete all config versions for an agent (called on agent deregistration).
 *
 * @param {string} agentId
 * @returns {boolean} true if records existed and were deleted
 */
function deleteAgent(agentId) {
  const store = _read();
  if (!store[agentId]) return false;
  delete store[agentId];
  _write(store);
  return true;
}

/**
 * Compute a shallow diff between two version configs.
 * Returns an object with keys that changed, showing [oldVal, newVal].
 *
 * @param {string} agentId
 * @param {number} fromVersion
 * @param {number} toVersion
 * @returns {Record<string, [any, any]>}
 */
function diffVersions(agentId, fromVersion, toVersion) {
  const fromRec = getVersion(agentId, fromVersion);
  const toRec   = getVersion(agentId, toVersion);

  if (!fromRec) throw new Error(`version ${fromVersion} not found`);
  if (!toRec)   throw new Error(`version ${toVersion} not found`);

  const diff   = {};
  const allKeys = new Set([
    ...Object.keys(fromRec.config),
    ...Object.keys(toRec.config),
  ]);

  for (const key of allKeys) {
    const oldVal = fromRec.config[key];
    const newVal = toRec.config[key];
    if (JSON.stringify(oldVal) !== JSON.stringify(newVal)) {
      diff[key] = [oldVal, newVal];
    }
  }

  return diff;
}

// ---------------------------------------------------------------------------
// Exports
// ---------------------------------------------------------------------------

module.exports = {
  createInitial,
  createVersion,
  setCurrentVersion,
  getCurrent,
  getVersion,
  listVersions,
  listAll,
  deleteAgent,
  diffVersions,
  CONFIG_FILE,
};
