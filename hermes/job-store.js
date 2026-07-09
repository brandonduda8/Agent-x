/**
 * hermes/job-store.js
 * =============================================================================
 * Persistent job state store for Agent Hermes.
 *
 * Maintains an in-memory map of all discovered/queued jobs and flushes them
 * to disk (data/hermes-jobs.json) for recovery across restarts.
 *
 * Job schema:
 * {
 *   id          : string   — unique job ID (uuid-v4)
 *   title       : string   — human-readable job title
 *   source      : string   — "internal" | "board:<name>" | "queue"
 *   type        : string   — task type label (e.g. "content", "research", "build")
 *   requiredCaps: string[] — capability tags that an agent must possess
 *   payload     : object   — arbitrary task-specific data
 *   priority    : number   — 0 (lowest) – 10 (highest)
 *   status      : string   — "open" | "assigned" | "in-progress" | "done" | "failed"
 *   assignedTo  : string|null — agentId that claimed the job
 *   score       : number|null — match score at time of assignment
 *   createdAt   : ISO8601
 *   updatedAt   : ISO8601
 *   expiresAt   : ISO8601|null
 * }
 * =============================================================================
 */

"use strict";

const fs   = require("fs");
const path = require("path");
const { v4: uuidv4 } = require("uuid");

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------
const STORE_PATH = path.resolve(
  __dirname,
  "..",
  "data",
  "hermes-jobs.json"
);

const VALID_STATUSES = new Set([
  "open",
  "assigned",
  "in-progress",
  "done",
  "failed",
]);

// ---------------------------------------------------------------------------
// Internal state
// ---------------------------------------------------------------------------
/** @type {Map<string, object>} */
const _jobs = new Map();

let _dirty = false;          // flush-on-write debounce flag
let _flushTimer = null;

// ---------------------------------------------------------------------------
// Persistence helpers
// ---------------------------------------------------------------------------

/**
 * Load jobs from disk into memory.
 * Called once at module initialisation — errors are non-fatal.
 */
function _load() {
  try {
    if (!fs.existsSync(STORE_PATH)) return;
    const raw  = fs.readFileSync(STORE_PATH, "utf8");
    const list = JSON.parse(raw);
    if (!Array.isArray(list)) return;
    for (const job of list) {
      if (job && job.id) _jobs.set(job.id, job);
    }
    console.log(`[JobStore] Loaded ${_jobs.size} job(s) from disk.`);
  } catch (err) {
    console.warn("[JobStore] Could not load jobs from disk:", err.message);
  }
}

/**
 * Schedule a debounced flush to disk (10 ms after the last write).
 */
function _scheduledFlush() {
  if (_flushTimer) clearTimeout(_flushTimer);
  _flushTimer = setTimeout(_flush, 10);
}

/**
 * Write the in-memory map to disk synchronously.
 */
function _flush() {
  try {
    const dir = path.dirname(STORE_PATH);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(STORE_PATH, JSON.stringify([..._jobs.values()], null, 2));
    _dirty = false;
  } catch (err) {
    console.error("[JobStore] Flush failed:", err.message);
  }
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Add a new job to the store.
 *
 * @param {object} params
 * @param {string}   params.title
 * @param {string}   [params.source="internal"]
 * @param {string}   [params.type="generic"]
 * @param {string[]} [params.requiredCaps=[]]
 * @param {object}   [params.payload={}]
 * @param {number}   [params.priority=5]
 * @param {string|null} [params.expiresAt=null]
 * @returns {object} The created job record.
 */
function addJob({
  title,
  source      = "internal",
  type        = "generic",
  requiredCaps = [],
  payload      = {},
  priority     = 5,
  expiresAt    = null,
}) {
  if (!title || typeof title !== "string") {
    throw new TypeError("[JobStore] addJob: title is required and must be a string.");
  }

  const now = new Date().toISOString();
  const job = {
    id           : uuidv4(),
    title,
    source,
    type,
    requiredCaps : Array.isArray(requiredCaps) ? requiredCaps : [],
    payload      : payload || {},
    priority     : typeof priority === "number" ? Math.max(0, Math.min(10, priority)) : 5,
    status       : "open",
    assignedTo   : null,
    score        : null,
    createdAt    : now,
    updatedAt    : now,
    expiresAt    : expiresAt || null,
  };

  _jobs.set(job.id, job);
  _scheduledFlush();
  return job;
}

/**
 * Retrieve a single job by ID.
 *
 * @param {string} id
 * @returns {object|null}
 */
function getJob(id) {
  return _jobs.get(id) ?? null;
}

/**
 * Return all jobs, optionally filtered by status.
 *
 * @param {string|null} [status=null]  — if provided, only jobs with this status
 * @returns {object[]}
 */
function listJobs(status = null) {
  const all = [..._jobs.values()];
  if (status) return all.filter(j => j.status === status);
  return all;
}

/**
 * Update one or more fields of an existing job.
 *
 * @param {string} id
 * @param {object} updates  — partial job fields to merge
 * @returns {object|null}   — updated job or null if not found
 */
function updateJob(id, updates) {
  const job = _jobs.get(id);
  if (!job) return null;

  // Guard status transitions
  if (updates.status && !VALID_STATUSES.has(updates.status)) {
    throw new RangeError(`[JobStore] Invalid status: ${updates.status}`);
  }

  Object.assign(job, updates, { updatedAt: new Date().toISOString() });
  _jobs.set(id, job);
  _scheduledFlush();
  return job;
}

/**
 * Remove a job permanently.
 *
 * @param {string} id
 * @returns {boolean}
 */
function removeJob(id) {
  const existed = _jobs.delete(id);
  if (existed) _scheduledFlush();
  return existed;
}

/**
 * Purge all jobs whose expiresAt timestamp has passed.
 *
 * @returns {number} Number of jobs removed.
 */
function purgeExpired() {
  const now  = Date.now();
  let   count = 0;
  for (const [id, job] of _jobs) {
    if (job.expiresAt && new Date(job.expiresAt).getTime() < now) {
      _jobs.delete(id);
      count++;
    }
  }
  if (count > 0) _scheduledFlush();
  return count;
}

/**
 * Return basic aggregate statistics about the job store.
 *
 * @returns {object}
 */
function stats() {
  const all = [..._jobs.values()];
  const byStatus = {};
  for (const j of all) {
    byStatus[j.status] = (byStatus[j.status] || 0) + 1;
  }
  return { total: all.length, byStatus };
}

// ---------------------------------------------------------------------------
// Initialise on first require
// ---------------------------------------------------------------------------
_load();

module.exports = {
  addJob,
  getJob,
  listJobs,
  updateJob,
  removeJob,
  purgeExpired,
  stats,
  // exposed for testing
  _flush,
  _storePath: STORE_PATH,
};
