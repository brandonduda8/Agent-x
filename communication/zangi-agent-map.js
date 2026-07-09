/**
 * Zangi Agent Map
 *
 * Maps Agent X agent IDs (and agent names) to their Zangi user / channel IDs.
 *
 * The authoritative source of truth is the JSON file at:
 *   data/zangi-agent-map.json
 *
 * This module loads that file at startup, keeps an in-memory copy for fast
 * lookups, and exposes helpers to add / remove / update mappings at runtime.
 * Changes are persisted back to disk immediately so they survive restarts.
 *
 * Schema for each map entry (stored in the JSON array `agents`):
 * {
 *   "agentId"    : "uuid-v4 | stable-name-slug",  // internal Agent X ID
 *   "agentName"  : "content-generator",            // human-readable name
 *   "zangiUserId": "zangi-uid-xxxx",               // Zangi DM target
 *   "zangiChannelId": "zangi-chan-xxxx",            // per-agent private channel
 *   "capabilities": ["draft","email"],              // mirrors registry capabilities
 *   "active"     : true                            // false = skip in broadcasts
 * }
 *
 * A special entry with agentId === "__broadcast__" holds the shared group
 * channel used for system-wide broadcasts.
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ---------------------------------------------------------------------------
// File path
// ---------------------------------------------------------------------------

const MAP_FILE = path.resolve(
  process.env.ZANGI_MAP_FILE ||
  path.join(__dirname, '..', 'data', 'zangi-agent-map.json')
);

// ---------------------------------------------------------------------------
// In-memory store (populated by load())
// ---------------------------------------------------------------------------

/** @type {Map<string, object>} agentId → entry */
const byAgentId = new Map();

/** @type {Map<string, object>} agentName → entry */
const byAgentName = new Map();

/** @type {Map<string, object>} zangiUserId → entry */
const byZangiUserId = new Map();

/** @type {Map<string, object>} zangiChannelId → entry */
const byZangiChannelId = new Map();

/** The broadcast (shared group) entry, if present */
let broadcastEntry = null;

// ---------------------------------------------------------------------------
// Disk helpers
// ---------------------------------------------------------------------------

/**
 * Read the map file from disk and re-populate the in-memory indices.
 * Safe to call multiple times (clears existing state).
 */
function load() {
  byAgentId.clear();
  byAgentName.clear();
  byZangiUserId.clear();
  byZangiChannelId.clear();
  broadcastEntry = null;

  let raw;
  try {
    raw = fs.readFileSync(MAP_FILE, 'utf8');
  } catch (err) {
    if (err.code === 'ENOENT') {
      // File doesn't exist yet — start with empty map
      console.info('[ZangiAgentMap] No map file found at', MAP_FILE, '— starting with defaults.');
      _seedDefaults();
      return;
    }
    throw err;
  }

  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch (err) {
    throw new Error(`[ZangiAgentMap] Failed to parse ${MAP_FILE}: ${err.message}`);
  }

  const agents = Array.isArray(parsed.agents) ? parsed.agents : [];
  for (const entry of agents) {
    _index(entry);
  }

  console.info(`[ZangiAgentMap] Loaded ${byAgentId.size} agent mapping(s) from ${MAP_FILE}`);
}

/**
 * Persist current in-memory state to disk atomically (write-then-rename).
 */
function save() {
  const agents = [...byAgentId.values()];
  const data = JSON.stringify({ agents }, null, 2);

  // Ensure the directory exists
  const dir = path.dirname(MAP_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  const tmp = MAP_FILE + '.tmp';
  fs.writeFileSync(tmp, data, 'utf8');
  fs.renameSync(tmp, MAP_FILE);
}

/**
 * Index a single entry into all lookup maps.
 * @param {object} entry
 */
function _index(entry) {
  if (!entry || !entry.agentId) return;

  byAgentId.set(entry.agentId, entry);

  if (entry.agentName) {
    byAgentName.set(entry.agentName, entry);
  }
  if (entry.zangiUserId) {
    byZangiUserId.set(entry.zangiUserId, entry);
  }
  if (entry.zangiChannelId) {
    byZangiChannelId.set(entry.zangiChannelId, entry);
  }
  if (entry.agentId === '__broadcast__') {
    broadcastEntry = entry;
  }
}

/**
 * Remove an entry from all indices.
 * @param {object} entry
 */
function _deindex(entry) {
  if (!entry) return;
  byAgentId.delete(entry.agentId);
  if (entry.agentName) byAgentName.delete(entry.agentName);
  if (entry.zangiUserId) byZangiUserId.delete(entry.zangiUserId);
  if (entry.zangiChannelId) byZangiChannelId.delete(entry.zangiChannelId);
  if (entry.agentId === '__broadcast__') broadcastEntry = null;
}

/**
 * Seed a default map with all known Agent X worker agents.
 * Zangi IDs are populated from environment variables so the file can be
 * committed without secrets; fill them in via env or update via API.
 */
function _seedDefaults() {
  const defaults = [
    // -----------------------------------------------------------------------
    // Shared broadcast channel
    // -----------------------------------------------------------------------
    {
      agentId: '__broadcast__',
      agentName: 'broadcast',
      zangiUserId: null,
      zangiChannelId: process.env.ZANGI_BROADCAST_CHANNEL_ID || null,
      capabilities: [],
      active: true,
    },
    // -----------------------------------------------------------------------
    // Core worker agents
    // -----------------------------------------------------------------------
    {
      agentId: 'orchestrator',
      agentName: 'orchestrator',
      zangiUserId: process.env.ZANGI_USER_ORCHESTRATOR || null,
      zangiChannelId: process.env.ZANGI_CHANNEL_ORCHESTRATOR || null,
      capabilities: ['route', 'coordinate'],
      active: true,
    },
    {
      agentId: 'content-generator',
      agentName: 'content-generator',
      zangiUserId: process.env.ZANGI_USER_CONTENT_GENERATOR || null,
      zangiChannelId: process.env.ZANGI_CHANNEL_CONTENT_GENERATOR || null,
      capabilities: ['draft', 'email', 'post'],
      active: true,
    },
    {
      agentId: 'data-aggregator',
      agentName: 'data-aggregator',
      zangiUserId: process.env.ZANGI_USER_DATA_AGGREGATOR || null,
      zangiChannelId: process.env.ZANGI_CHANNEL_DATA_AGGREGATOR || null,
      capabilities: ['fetch', 'summarise', 'aggregate'],
      active: true,
    },
    {
      agentId: 'publisher',
      agentName: 'publisher',
      zangiUserId: process.env.ZANGI_USER_PUBLISHER || null,
      zangiChannelId: process.env.ZANGI_CHANNEL_PUBLISHER || null,
      capabilities: ['publish', 'distribute'],
      active: true,
    },
    {
      agentId: 'infrastructure',
      agentName: 'infrastructure',
      zangiUserId: process.env.ZANGI_USER_INFRASTRUCTURE || null,
      zangiChannelId: process.env.ZANGI_CHANNEL_INFRASTRUCTURE || null,
      capabilities: ['env-check', 'network-probe', 'lifecycle'],
      active: true,
    },
    {
      agentId: 'api-socket',
      agentName: 'api-socket',
      zangiUserId: process.env.ZANGI_USER_API_SOCKET || null,
      zangiChannelId: process.env.ZANGI_CHANNEL_API_SOCKET || null,
      capabilities: ['http-get', 'http-post'],
      active: true,
    },
    {
      agentId: 'watchdog',
      agentName: 'watchdog',
      zangiUserId: process.env.ZANGI_USER_WATCHDOG || null,
      zangiChannelId: process.env.ZANGI_CHANNEL_WATCHDOG || null,
      capabilities: ['health-monitor', 'restart'],
      active: true,
    },
  ];

  for (const entry of defaults) {
    _index(entry);
  }
  save();
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Look up a mapping by Agent X agent ID.
 * @param {string} agentId
 * @returns {object|null}
 */
function getByAgentId(agentId) {
  return byAgentId.get(agentId) || null;
}

/**
 * Look up a mapping by agent name (e.g. "content-generator").
 * @param {string} name
 * @returns {object|null}
 */
function getByAgentName(name) {
  return byAgentName.get(name) || null;
}

/**
 * Look up a mapping by Zangi user ID (for routing inbound DMs).
 * @param {string} zangiUserId
 * @returns {object|null}
 */
function getByZangiUserId(zangiUserId) {
  return byZangiUserId.get(zangiUserId) || null;
}

/**
 * Look up a mapping by Zangi channel ID (for routing inbound channel messages).
 * @param {string} zangiChannelId
 * @returns {object|null}
 */
function getByZangiChannelId(zangiChannelId) {
  return byZangiChannelId.get(zangiChannelId) || null;
}

/**
 * Convenience: resolve an agent by ID **or** name.
 *
 * @param {string} idOrName  Agent X UUID or name slug
 * @returns {object|null}
 */
function resolve(idOrName) {
  return getByAgentId(idOrName) || getByAgentName(idOrName) || null;
}

/**
 * Return the broadcast channel entry (agentId === '__broadcast__').
 * @returns {object|null}
 */
function getBroadcastEntry() {
  return broadcastEntry;
}

/**
 * List all entries (excluding the broadcast meta-entry).
 * Pass `{ includeInactive: true }` to include entries with `active: false`.
 *
 * @param {object} [opts]
 * @param {boolean} [opts.includeInactive]
 * @returns {object[]}
 */
function listAll({ includeInactive = false } = {}) {
  return [...byAgentId.values()].filter((e) => {
    if (e.agentId === '__broadcast__') return false;
    if (!includeInactive && !e.active) return false;
    return true;
  });
}

/**
 * Add or update a mapping entry.
 * Existing entry with the same agentId is replaced.
 *
 * @param {object} entry
 * @param {string} entry.agentId
 * @param {string} [entry.agentName]
 * @param {string} [entry.zangiUserId]
 * @param {string} [entry.zangiChannelId]
 * @param {string[]} [entry.capabilities]
 * @param {boolean} [entry.active]
 * @param {boolean} [opts.persist]  Write to disk immediately (default: true)
 */
function upsert(entry, { persist = true } = {}) {
  if (!entry || !entry.agentId) throw new Error('upsert: entry.agentId is required');

  // Remove old indices if entry already exists
  const existing = byAgentId.get(entry.agentId);
  if (existing) _deindex(existing);

  const normalised = {
    agentId: entry.agentId,
    agentName: entry.agentName || entry.agentId,
    zangiUserId: entry.zangiUserId || null,
    zangiChannelId: entry.zangiChannelId || null,
    capabilities: Array.isArray(entry.capabilities) ? entry.capabilities : [],
    active: entry.active !== undefined ? Boolean(entry.active) : true,
  };

  _index(normalised);

  if (persist) save();
  return normalised;
}

/**
 * Remove a mapping by Agent X agent ID.
 *
 * @param {string} agentId
 * @param {boolean} [opts.persist]  Write to disk immediately (default: true)
 * @returns {boolean}  true if removed, false if not found
 */
function remove(agentId, { persist = true } = {}) {
  const entry = byAgentId.get(agentId);
  if (!entry) return false;
  _deindex(entry);
  if (persist) save();
  return true;
}

/**
 * Reload the map from disk (useful after external edits).
 */
function reload() {
  load();
}

// ---------------------------------------------------------------------------
// Initialise on module load
// ---------------------------------------------------------------------------

load();

// ---------------------------------------------------------------------------
// Exports
// ---------------------------------------------------------------------------

module.exports = {
  getByAgentId,
  getByAgentName,
  getByZangiUserId,
  getByZangiChannelId,
  resolve,
  getBroadcastEntry,
  listAll,
  upsert,
  remove,
  reload,
  save,
  MAP_FILE,
};
