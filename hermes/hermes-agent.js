/**
 * hermes/hermes-agent.js
 * =============================================================================
 * Agent Hermes — Job Discovery & Matching Orchestrator
 *
 * Hermes is the coordination core of the job pipeline. It:
 *
 *  1. Initialises the job store (persistent on-disk state).
 *  2. Starts the job-discovery scanner (internal queues + remote boards).
 *  3. Periodically runs the job-matcher against the live agent registry.
 *  4. Emits internal events so other subsystems can react to new assignments.
 *  5. Exposes a clean programmatic API consumed by hermes-api.js.
 *
 * ## Event bus integration
 *
 *  Hermes publishes the following events on the Node.js core EventEmitter
 *  exported as `hermesEvents`:
 *
 *   "job:discovered"   — { job }              — new job added to store
 *   "job:assigned"     — { job, agentId }      — job matched to an agent
 *   "job:unmatched"    — { job }              — open job with no eligible agent
 *   "match:cycle"      — { assigned, unmatched, elapsed } — end of each match cycle
 *
 * ## Environment variables
 *
 *  HERMES_DISCOVERY_INTERVAL_MS   default 60 000 (1 min)
 *  HERMES_MATCH_INTERVAL_MS       default 15 000 (15 s)
 *  HERMES_REGISTRY_URL            default http://localhost:3000/v1/registry/agents
 *  HERMES_MOCK_BOARD              default "true" — set "false" to disable mock jobs
 *  HERMES_JOB_BOARDS              comma-separated URLs of remote job board endpoints
 * =============================================================================
 */

"use strict";

const { EventEmitter } = require("events");
const http             = require("http");
const https            = require("https");

const jobStore    = require("./job-store");
const jobMatcher  = require("./job-matcher");
const jobDiscovery = require("./job-discovery");

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------
const DISCOVERY_INTERVAL_MS = parseInt(
  process.env.HERMES_DISCOVERY_INTERVAL_MS || "60000", 10
);
const MATCH_INTERVAL_MS = parseInt(
  process.env.HERMES_MATCH_INTERVAL_MS || "15000", 10
);
const REGISTRY_URL = process.env.HERMES_REGISTRY_URL ||
  "http://localhost:3000/v1/registry/agents";

// ---------------------------------------------------------------------------
// Internal event bus
// ---------------------------------------------------------------------------
const hermesEvents = new EventEmitter();
hermesEvents.setMaxListeners(50);

// ---------------------------------------------------------------------------
// Agent-list cache
// ---------------------------------------------------------------------------
/** @type {object[]} */
let _agentCache  = [];
let _cacheStale  = true;
let _fetchingAgents = false;

/**
 * Fetch the current agent list from the registry API.
 * Falls back to the last known cache on error.
 *
 * @returns {Promise<object[]>}
 */
async function _fetchAgents() {
  if (_fetchingAgents) return _agentCache;
  _fetchingAgents = true;

  return new Promise((resolve) => {
    const mod = REGISTRY_URL.startsWith("https") ? https : http;
    const timeout = setTimeout(() => {
      console.warn("[Hermes] Registry fetch timed out — using cached agent list.");
      _fetchingAgents = false;
      resolve(_agentCache);
    }, 6000);

    try {
      mod.get(REGISTRY_URL, { headers: { Accept: "application/json" } }, (res) => {
        let body = "";
        res.on("data", c => { body += c; });
        res.on("end", () => {
          clearTimeout(timeout);
          _fetchingAgents = false;
          try {
            const data = JSON.parse(body);
            // Support both raw array and { agents: [] } envelope
            const list = Array.isArray(data)
              ? data
              : (data.agents || data.data || []);
            _agentCache = Array.isArray(list) ? list : [];
            _cacheStale = false;
            resolve(_agentCache);
          } catch (e) {
            console.warn("[Hermes] Agent list parse error:", e.message);
            resolve(_agentCache);
          }
        });
        res.on("error", e => {
          clearTimeout(timeout);
          _fetchingAgents = false;
          console.warn("[Hermes] Registry response error:", e.message);
          resolve(_agentCache);
        });
      }).on("error", e => {
        clearTimeout(timeout);
        _fetchingAgents = false;
        console.warn("[Hermes] Registry request error:", e.message);
        resolve(_agentCache);
      });
    } catch (e) {
      clearTimeout(timeout);
      _fetchingAgents = false;
      console.warn("[Hermes] Could not reach registry:", e.message);
      resolve(_agentCache);
    }
  });
}

// ---------------------------------------------------------------------------
// Discovery callback
// ---------------------------------------------------------------------------

/**
 * Callback handed to job-discovery.scanAll / startPolling.
 * Adds job to store and emits "job:discovered".
 *
 * @param {object} params
 * @returns {object} created job
 */
function _onJobDiscovered(params) {
  const job = jobStore.addJob(params);
  hermesEvents.emit("job:discovered", { job });
  return job;
}

// ---------------------------------------------------------------------------
// Match cycle
// ---------------------------------------------------------------------------

/**
 * Run one complete match cycle:
 *  1. Refresh agent list from registry.
 *  2. Call assignAllOpen — scores and assigns every open job.
 *  3. Emit events for assigned and unmatched jobs.
 *
 * @returns {Promise<{ assigned: number, unmatched: number, elapsed: number }>}
 */
async function runMatchCycle() {
  const t0 = Date.now();

  const agents = await _fetchAgents();
  if (agents.length === 0) {
    console.warn("[Hermes] No agents available — skipping match cycle.");
    return { assigned: 0, unmatched: 0, elapsed: Date.now() - t0 };
  }

  // Snapshot open jobs before assignment (for event emission)
  const openBefore = jobStore.listJobs("open");

  const { assigned, unmatched } = jobMatcher.assignAllOpen(jobStore, agents);

  // Emit per-job events for newly assigned jobs
  for (const job of openBefore) {
    const updated = jobStore.getJob(job.id);
    if (updated && updated.status === "assigned") {
      hermesEvents.emit("job:assigned", { job: updated, agentId: updated.assignedTo });
    } else if (updated && updated.status === "open") {
      hermesEvents.emit("job:unmatched", { job: updated });
    }
  }

  const elapsed = Date.now() - t0;
  hermesEvents.emit("match:cycle", { assigned, unmatched, elapsed });

  console.log(
    `[Hermes] Match cycle complete — assigned: ${assigned}, unmatched: ${unmatched}, elapsed: ${elapsed}ms`
  );

  return { assigned, unmatched, elapsed };
}

// ---------------------------------------------------------------------------
// Lifecycle
// ---------------------------------------------------------------------------

let _stopDiscovery = null;
let _matchInterval  = null;
let _running        = false;

/**
 * Initialise and start Agent Hermes.
 *
 * Safe to call multiple times — subsequent calls are no-ops.
 */
function start() {
  if (_running) {
    console.log("[Hermes] Already running.");
    return;
  }
  _running = true;

  console.log("[Hermes] Starting up…");
  console.log(`  Discovery interval : ${DISCOVERY_INTERVAL_MS}ms`);
  console.log(`  Match interval     : ${MATCH_INTERVAL_MS}ms`);
  console.log(`  Registry URL       : ${REGISTRY_URL}`);

  // 1. Expire any stale jobs from the previous run
  const purged = jobStore.purgeExpired();
  if (purged > 0) console.log(`[Hermes] Purged ${purged} expired job(s).`);

  // 2. Start periodic job discovery
  _stopDiscovery = jobDiscovery.startPolling(
    _onJobDiscovered,
    jobStore.listJobs,
    DISCOVERY_INTERVAL_MS
  );

  // 3. Start periodic match cycles
  _matchInterval = setInterval(() => {
    runMatchCycle().catch(err =>
      console.error("[Hermes] Match cycle error:", err.message)
    );
  }, MATCH_INTERVAL_MS);

  console.log("[Hermes] Online.");
}

/**
 * Gracefully stop Agent Hermes.
 */
function stop() {
  if (!_running) return;
  _running = false;

  if (_stopDiscovery) { _stopDiscovery(); _stopDiscovery = null; }
  if (_matchInterval) { clearInterval(_matchInterval); _matchInterval = null; }

  console.log("[Hermes] Stopped.");
}

// ---------------------------------------------------------------------------
// Public programmatic API (used by hermes-api.js)
// ---------------------------------------------------------------------------

/**
 * Trigger a manual discovery scan and return newly added jobs.
 *
 * @returns {Promise<object[]>}
 */
async function triggerScan() {
  return jobDiscovery.scanAll(_onJobDiscovered, jobStore.listJobs);
}

/**
 * Trigger a manual match cycle and return the result.
 *
 * @returns {Promise<object>}
 */
async function triggerMatch() {
  return runMatchCycle();
}

/**
 * Submit a job directly (bypassing discovery, e.g. from an HTTP request).
 *
 * @param {object} params — job params (see jobStore.addJob schema)
 * @returns {object}      — created job record
 */
function submitJob(params) {
  const job = jobStore.addJob(params);
  hermesEvents.emit("job:discovered", { job });
  return job;
}

/**
 * Return all jobs, optionally filtered by status.
 *
 * @param {string|null} [status]
 * @returns {object[]}
 */
function getJobs(status = null) {
  return jobStore.listJobs(status);
}

/**
 * Return a single job by ID.
 *
 * @param {string} id
 * @returns {object|null}
 */
function getJob(id) {
  return jobStore.getJob(id);
}

/**
 * Update a job (e.g. mark in-progress or done from an external agent).
 *
 * @param {string} id
 * @param {object} updates
 * @returns {object|null}
 */
function updateJob(id, updates) {
  return jobStore.updateJob(id, updates);
}

/**
 * Remove a job.
 *
 * @param {string} id
 * @returns {boolean}
 */
function removeJob(id) {
  return jobStore.removeJob(id);
}

/**
 * Rank available agents for a given job without assigning it.
 *
 * @param {string} jobId
 * @returns {Promise<Array>}
 */
async function rankForJob(jobId) {
  const job = jobStore.getJob(jobId);
  if (!job) return [];
  const agents = await _fetchAgents();
  return jobMatcher.rankAgents(job, agents);
}

/**
 * Return store statistics.
 *
 * @returns {object}
 */
function getStats() {
  return {
    ...jobStore.stats(),
    agentsCached : _agentCache.length,
    running      : _running,
  };
}

// ---------------------------------------------------------------------------
// Module exports
// ---------------------------------------------------------------------------
module.exports = {
  // Lifecycle
  start,
  stop,

  // API surface
  submitJob,
  getJobs,
  getJob,
  updateJob,
  removeJob,
  triggerScan,
  triggerMatch,
  rankForJob,
  getStats,

  // Event bus — consumers can subscribe to Hermes events
  events: hermesEvents,

  // Internals exposed for testing
  _fetchAgents,
  _onJobDiscovered,
};
