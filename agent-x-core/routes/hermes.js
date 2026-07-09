/**
 * agent-x-core/routes/hermes.js
 * =============================================================================
 * Express router — Agent Hermes Job Discovery & Matching API
 *
 * Mount point (in agent-x-core/index.js):
 *   app.use("/api/hermes", require("./routes/hermes"));
 *
 * ## Endpoints
 *
 *  Method  Path                        Description
 *  ──────  ──────────────────────────  ─────────────────────────────────────
 *  GET     /api/hermes/jobs            List all jobs (filter by ?status=)
 *  POST    /api/hermes/jobs            Submit a new job
 *  GET     /api/hermes/jobs/:id        Get a single job by ID
 *  PATCH   /api/hermes/jobs/:id        Update job fields (status, assignedTo…)
 *  DELETE  /api/hermes/jobs/:id        Remove a job
 *
 *  POST    /api/hermes/scan            Trigger a one-shot discovery scan
 *  POST    /api/hermes/match           Trigger a one-shot match cycle
 *  GET     /api/hermes/jobs/:id/rank   Rank available agents for a specific job
 *
 *  GET     /api/hermes/stats           Store + runtime statistics
 *  GET     /api/hermes/health          Liveness probe (always 200 when mounted)
 *
 * =============================================================================
 */

"use strict";

const { Router } = require("express");
const hermes     = require("../../hermes/hermes-agent");

const router = Router();

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Wrap an async route handler and forward errors to Express error middleware.
 *
 * @param {Function} fn
 * @returns {Function}
 */
const asyncHandler = fn => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);

/**
 * Send a normalised JSON success response.
 *
 * @param {object} res
 * @param {*}      data
 * @param {number} [status=200]
 */
function ok(res, data, status = 200) {
  res.status(status).json({
    ok     : true,
    ts     : new Date().toISOString(),
    data,
  });
}

/**
 * Send a normalised JSON error response.
 *
 * @param {object} res
 * @param {string} message
 * @param {number} [status=400]
 * @param {*}      [detail]
 */
function fail(res, message, status = 400, detail = undefined) {
  const body = { ok: false, ts: new Date().toISOString(), error: message };
  if (detail !== undefined) body.detail = detail;
  res.status(status).json(body);
}

// ---------------------------------------------------------------------------
// ── /api/hermes/health ──────────────────────────────────────────────────────
// ---------------------------------------------------------------------------

/**
 * GET /api/hermes/health
 * Liveness probe — always returns 200 when the router is mounted.
 */
router.get("/health", (_req, res) => {
  ok(res, { service: "hermes", status: "ok" });
});

// ---------------------------------------------------------------------------
// ── /api/hermes/stats ───────────────────────────────────────────────────────
// ---------------------------------------------------------------------------

/**
 * GET /api/hermes/stats
 * Returns aggregate statistics about the job store and runtime state.
 */
router.get("/stats", (_req, res) => {
  ok(res, hermes.getStats());
});

// ---------------------------------------------------------------------------
// ── /api/hermes/jobs ────────────────────────────────────────────────────────
// ---------------------------------------------------------------------------

/**
 * GET /api/hermes/jobs
 *
 * Query parameters:
 *   ?status=open|assigned|in-progress|done|failed
 *   ?type=<type>           — filter by job type
 *   ?source=<source>       — filter by source label
 *   ?limit=<n>             — max results (default 100)
 *   ?offset=<n>            — pagination offset (default 0)
 *   ?sort=priority|createdAt|score   — sort field (default createdAt)
 *   ?order=asc|desc        — sort order (default desc)
 */
router.get("/jobs", (req, res) => {
  const {
    status,
    type,
    source,
    limit  = "100",
    offset = "0",
    sort   = "createdAt",
    order  = "desc",
  } = req.query;

  let jobs = hermes.getJobs(status || null);

  // Optional filters
  if (type)   jobs = jobs.filter(j => j.type   === type);
  if (source) jobs = jobs.filter(j => j.source === source);

  // Sorting
  const SORTABLE = new Set(["priority", "createdAt", "updatedAt", "score"]);
  const sortKey  = SORTABLE.has(sort) ? sort : "createdAt";
  const dir      = order === "asc" ? 1 : -1;

  jobs = [...jobs].sort((a, b) => {
    const av = a[sortKey] ?? "";
    const bv = b[sortKey] ?? "";
    if (av < bv) return -1 * dir;
    if (av > bv) return  1 * dir;
    return 0;
  });

  // Pagination
  const lim  = Math.max(1, Math.min(500, parseInt(limit,  10) || 100));
  const off  = Math.max(0,              parseInt(offset, 10) || 0);
  const page = jobs.slice(off, off + lim);

  ok(res, {
    total  : jobs.length,
    limit  : lim,
    offset : off,
    jobs   : page,
  });
});

/**
 * POST /api/hermes/jobs
 *
 * Submit a new job directly into the Hermes pipeline.
 *
 * Body (JSON):
 * {
 *   "title"       : "string (required)",
 *   "type"        : "string",
 *   "source"      : "string",
 *   "requiredCaps": ["string", …],
 *   "payload"     : { … },
 *   "priority"    : 0–10,
 *   "expiresAt"   : "ISO8601 | null"
 * }
 */
router.post("/jobs", asyncHandler(async (req, res) => {
  const body = req.body || {};

  if (!body.title || typeof body.title !== "string" || !body.title.trim()) {
    return fail(res, "Field 'title' is required and must be a non-empty string.");
  }

  const params = {
    title        : body.title.trim(),
    source       : typeof body.source       === "string"  ? body.source       : "api",
    type         : typeof body.type         === "string"  ? body.type         : "generic",
    requiredCaps : Array.isArray(body.requiredCaps)        ? body.requiredCaps : [],
    payload      : typeof body.payload      === "object"  ? body.payload      : {},
    priority     : typeof body.priority     === "number"  ? body.priority     : 5,
    expiresAt    : body.expiresAt || null,
  };

  const job = hermes.submitJob(params);
  ok(res, { job }, 201);
}));

// ---------------------------------------------------------------------------
// ── /api/hermes/jobs/:id ────────────────────────────────────────────────────
// ---------------------------------------------------------------------------

/**
 * GET /api/hermes/jobs/:id
 * Retrieve a single job record.
 */
router.get("/jobs/:id", (req, res) => {
  const job = hermes.getJob(req.params.id);
  if (!job) return fail(res, `Job not found: ${req.params.id}`, 404);
  ok(res, { job });
});

/**
 * PATCH /api/hermes/jobs/:id
 *
 * Update mutable fields of an existing job.
 * Immutable fields (id, createdAt) are silently ignored.
 *
 * Body (JSON) — any subset of:
 * {
 *   "status"     : "open|assigned|in-progress|done|failed",
 *   "assignedTo" : "agentId | null",
 *   "priority"   : 0–10,
 *   "payload"    : { … },
 *   "expiresAt"  : "ISO8601 | null"
 * }
 */
router.patch("/jobs/:id", asyncHandler(async (req, res) => {
  const job = hermes.getJob(req.params.id);
  if (!job) return fail(res, `Job not found: ${req.params.id}`, 404);

  const body    = req.body || {};
  const allowed = new Set(["status", "assignedTo", "priority", "payload", "expiresAt", "title", "requiredCaps"]);
  const updates = {};

  for (const [k, v] of Object.entries(body)) {
    if (allowed.has(k)) updates[k] = v;
  }

  if (Object.keys(updates).length === 0) {
    return fail(res, "No updatable fields provided.");
  }

  try {
    const updated = hermes.updateJob(req.params.id, updates);
    ok(res, { job: updated });
  } catch (err) {
    fail(res, err.message, 422);
  }
}));

/**
 * DELETE /api/hermes/jobs/:id
 * Permanently remove a job from the store.
 */
router.delete("/jobs/:id", (req, res) => {
  const existed = hermes.removeJob(req.params.id);
  if (!existed) return fail(res, `Job not found: ${req.params.id}`, 404);
  ok(res, { removed: req.params.id });
});

// ---------------------------------------------------------------------------
// ── /api/hermes/jobs/:id/rank ───────────────────────────────────────────────
// ---------------------------------------------------------------------------

/**
 * GET /api/hermes/jobs/:id/rank
 *
 * Rank all currently available agents against the specified job.
 * Does NOT assign the job — purely advisory.
 *
 * Response:
 * {
 *   "job"     : { … job record … },
 *   "ranking" : [{ agentId, agentName, score, breakdown }, …]
 * }
 */
router.get("/jobs/:id/rank", asyncHandler(async (req, res) => {
  const job = hermes.getJob(req.params.id);
  if (!job) return fail(res, `Job not found: ${req.params.id}`, 404);

  const ranking = await hermes.rankForJob(req.params.id);
  ok(res, { job, ranking });
}));

// ---------------------------------------------------------------------------
// ── /api/hermes/scan ────────────────────────────────────────────────────────
// ---------------------------------------------------------------------------

/**
 * POST /api/hermes/scan
 *
 * Trigger an immediate discovery scan across all configured sources.
 * Returns the list of newly discovered jobs.
 *
 * No request body required.
 */
router.post("/scan", asyncHandler(async (req, res) => {
  const created = await hermes.triggerScan();
  ok(res, {
    scanned  : created.length,
    jobs     : created,
  });
}));

// ---------------------------------------------------------------------------
// ── /api/hermes/match ───────────────────────────────────────────────────────
// ---------------------------------------------------------------------------

/**
 * POST /api/hermes/match
 *
 * Trigger an immediate match cycle — assigns all open jobs to available agents.
 *
 * No request body required.
 *
 * Response:
 * {
 *   "assigned"  : number,
 *   "unmatched" : number,
 *   "elapsed"   : number   — milliseconds
 * }
 */
router.post("/match", asyncHandler(async (req, res) => {
  const result = await hermes.triggerMatch();
  ok(res, result);
}));

// ---------------------------------------------------------------------------
// ── Error handler (scoped to this router) ───────────────────────────────────
// ---------------------------------------------------------------------------

// eslint-disable-next-line no-unused-vars
router.use((err, req, res, _next) => {
  console.error("[HermesAPI] Unhandled error:", err);
  fail(res, err.message || "Internal server error", 500);
});

module.exports = router;
