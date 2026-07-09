/**
 * hermes/job-discovery.js
 * =============================================================================
 * Job-board scanner and internal task-queue reader for Agent Hermes.
 *
 * ## Discovery sources
 *
 *  Source              | Driver key        | Description
 *  ─────────────────── | ───────────────── | ──────────────────────────────
 *  Internal task file  | "internal-queue"  | Reads data/tasks.json + agent-x-core/tasks.json
 *  HTTP job board      | "board:<url>"     | Polls a remote JSON endpoint
 *  Inline mock board   | "mock-board"      | Built-in demo jobs (dev / testing)
 *
 * Each discovered item is normalised into the job-store schema before being
 * passed to the provided callback (usually addJob from job-store.js).
 *
 * ## Usage
 *
 *   const discovery = require("./job-discovery");
 *
 *   // One-shot scan of all enabled sources
 *   const jobs = await discovery.scanAll(addJobFn);
 *
 *   // Start periodic polling (returns a stopper function)
 *   const stop = discovery.startPolling(addJobFn, 60_000);
 *   // …later:
 *   stop();
 * =============================================================================
 */

"use strict";

const fs    = require("fs");
const path  = require("path");
const https = require("https");
const http  = require("http");

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------
const REPO_ROOT = path.resolve(__dirname, "..");

/** Paths to internal task JSON files */
const INTERNAL_TASK_FILES = [
  path.join(REPO_ROOT, "data",          "tasks.json"),
  path.join(REPO_ROOT, "agent-x-core", "tasks.json"),
  path.join(REPO_ROOT, "memory",       "tasks.json"),
];

/**
 * Remote job board endpoints to poll.
 * Populated from HERMES_JOB_BOARDS env var (comma-separated URLs)
 * or left empty for local-only operation.
 */
const REMOTE_BOARDS = (process.env.HERMES_JOB_BOARDS || "")
  .split(",")
  .map(u => u.trim())
  .filter(Boolean);

/** Whether to include the built-in mock board (useful for dev/CI) */
const INCLUDE_MOCK = process.env.HERMES_MOCK_BOARD !== "false";

/** HTTP fetch timeout in ms */
const FETCH_TIMEOUT_MS = parseInt(process.env.HERMES_FETCH_TIMEOUT_MS || "8000", 10);

// ---------------------------------------------------------------------------
// Normalisation helpers
// ---------------------------------------------------------------------------

/**
 * Normalise an arbitrary task object into the Hermes job-store schema.
 * Unknown fields are folded into `payload`.
 *
 * @param {object} raw   — raw task/job object from any source
 * @param {string} source — source identifier string
 * @returns {object}      — normalised job params (ready for addJob)
 */
function normalise(raw, source) {
  const type = (
    raw.type   ||
    raw.kind   ||
    raw.category ||
    "generic"
  ).toLowerCase();

  // Merge known capability hints
  const requiredCaps = Array.isArray(raw.requiredCaps)
    ? raw.requiredCaps
    : Array.isArray(raw.capabilities)
      ? raw.capabilities
      : Array.isArray(raw.tags)
        ? raw.tags
        : [];

  // Derive priority
  const priority = typeof raw.priority === "number"
    ? raw.priority
    : raw.urgent || raw.high_priority
      ? 8
      : 5;

  // Carry everything else into payload for agent use
  const payload = {
    ...(raw.payload || {}),
    ...(raw.data    || {}),
    description : raw.description || raw.body || raw.content || "",
    externalId  : raw.id          || raw._id  || null,
  };

  return {
    title       : raw.title || raw.name || raw.task || `Untitled job from ${source}`,
    source,
    type,
    requiredCaps,
    payload,
    priority,
    expiresAt   : raw.expiresAt || raw.deadline || raw.expires_at || null,
  };
}

// ---------------------------------------------------------------------------
// Source drivers
// ---------------------------------------------------------------------------

/**
 * Read tasks from internal JSON files on disk.
 *
 * Accepts arrays at the top level or under keys:
 *   "tasks", "jobs", "items", "queue"
 *
 * @returns {Promise<object[]>} normalised job param objects
 */
async function discoverInternal() {
  const results = [];

  for (const filePath of INTERNAL_TASK_FILES) {
    if (!fs.existsSync(filePath)) continue;

    try {
      const raw  = fs.readFileSync(filePath, "utf8");
      const data = JSON.parse(raw);

      // Support multiple container shapes
      const list = Array.isArray(data)
        ? data
        : (data.tasks || data.jobs || data.items || data.queue || []);

      if (!Array.isArray(list)) continue;

      const label = `internal-queue:${path.basename(path.dirname(filePath))}`;
      for (const item of list) {
        if (item && typeof item === "object") {
          // Skip items already marked done / completed
          const s = (item.status || item.state || "").toLowerCase();
          if (s === "done" || s === "completed" || s === "cancelled") continue;

          results.push(normalise(item, label));
        }
      }
    } catch (err) {
      console.warn(`[JobDiscovery] Could not read ${filePath}:`, err.message);
    }
  }

  return results;
}

/**
 * Fetch tasks from a remote HTTP(S) JSON endpoint.
 *
 * The endpoint must return either:
 *   - a JSON array of job objects, or
 *   - a JSON object with one of the keys: jobs, tasks, items, data
 *
 * @param {string} url
 * @returns {Promise<object[]>} normalised job param objects
 */
async function discoverRemoteBoard(url) {
  return new Promise((resolve) => {
    const mod     = url.startsWith("https") ? https : http;
    const label   = `board:${url}`;
    const timeout = setTimeout(() => {
      console.warn(`[JobDiscovery] Timeout fetching ${url}`);
      resolve([]);
    }, FETCH_TIMEOUT_MS);

    try {
      const req = mod.get(url, { headers: { Accept: "application/json" } }, (res) => {
        let body = "";
        res.on("data", chunk => { body += chunk; });
        res.on("end", () => {
          clearTimeout(timeout);
          try {
            const data = JSON.parse(body);
            const list = Array.isArray(data)
              ? data
              : (data.jobs || data.tasks || data.items || data.data || []);

            if (!Array.isArray(list)) {
              console.warn(`[JobDiscovery] Unexpected shape from ${url}`);
              resolve([]);
              return;
            }

            resolve(list.map(item => normalise(item, label)));
          } catch (parseErr) {
            console.warn(`[JobDiscovery] JSON parse error from ${url}:`, parseErr.message);
            resolve([]);
          }
        });
        res.on("error", err => {
          clearTimeout(timeout);
          console.warn(`[JobDiscovery] Response error from ${url}:`, err.message);
          resolve([]);
        });
      });

      req.on("error", err => {
        clearTimeout(timeout);
        console.warn(`[JobDiscovery] Request error for ${url}:`, err.message);
        resolve([]);
      });
    } catch (err) {
      clearTimeout(timeout);
      console.warn(`[JobDiscovery] Could not initiate request to ${url}:`, err.message);
      resolve([]);
    }
  });
}

/**
 * Return a static set of mock jobs useful for development and CI.
 *
 * @returns {object[]} normalised job param objects
 */
function discoverMockBoard() {
  const mocks = [
    {
      title       : "Write 3 monetisation email sequences",
      type        : "content",
      requiredCaps: ["draft", "email"],
      priority    : 8,
      description : "Generate welcome, nurture, and sales sequences for SaaS product.",
    },
    {
      title       : "Aggregate trending SaaS niches from HN & Reddit",
      type        : "research",
      requiredCaps: ["fetch", "summarise", "aggregate"],
      priority    : 6,
      description : "Pull top posts, extract startup ideas, return JSON summary.",
    },
    {
      title       : "Publish product listing to Gumroad",
      type        : "publish",
      requiredCaps: ["publish", "distribute"],
      priority    : 7,
      description : "Take the generated ebook artifact and push it to Gumroad via API.",
    },
    {
      title       : "Sanity-check all running microservices",
      type        : "infrastructure",
      requiredCaps: ["env-check", "network-probe"],
      priority    : 9,
      description : "HTTP probe each service endpoint; return health report.",
    },
    {
      title       : "Route next batch of tasks to available workers",
      type        : "orchestration",
      requiredCaps: ["route", "coordinate"],
      priority    : 5,
      description : "Orchestrator pass: dequeue, score, dispatch pending tasks.",
    },
    {
      title       : "Fetch Stripe revenue report for last 7 days",
      type        : "data",
      requiredCaps: ["http-get", "http-post"],
      priority    : 4,
      description : "Call Stripe API, aggregate charges, return summary object.",
    },
  ];

  return mocks.map(m => normalise(m, "mock-board"));
}

// ---------------------------------------------------------------------------
// Deduplication
// ---------------------------------------------------------------------------

/**
 * Filter out jobs whose title + source already exist in the store.
 *
 * @param {object[]}        candidates — normalised job param arrays
 * @param {Function}        listJobs   — jobStore.listJobs
 * @returns {object[]}
 */
function dedup(candidates, listJobs) {
  const existing = new Set(
    listJobs().map(j => `${j.source}|${j.title.toLowerCase()}`)
  );
  return candidates.filter(c => {
    const key = `${c.source}|${c.title.toLowerCase()}`;
    return !existing.has(key);
  });
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Run a one-shot discovery pass across all configured sources.
 *
 * @param {Function} addJob    — jobStore.addJob callback
 * @param {Function} [listJobs] — jobStore.listJobs for dedup (optional)
 * @returns {Promise<object[]>} array of newly created job records
 */
async function scanAll(addJob, listJobs = null) {
  console.log("[JobDiscovery] Starting discovery scan…");

  const buckets = await Promise.all([
    discoverInternal(),
    ...REMOTE_BOARDS.map(url => discoverRemoteBoard(url)),
    INCLUDE_MOCK ? Promise.resolve(discoverMockBoard()) : Promise.resolve([]),
  ]);

  let candidates = buckets.flat();
  console.log(`[JobDiscovery] Raw candidates: ${candidates.length}`);

  // Dedup against existing store entries if listJobs is available
  if (typeof listJobs === "function") {
    candidates = dedup(candidates, listJobs);
    console.log(`[JobDiscovery] After dedup: ${candidates.length} new job(s)`);
  }

  const created = [];
  for (const params of candidates) {
    try {
      const job = addJob(params);
      created.push(job);
    } catch (err) {
      console.warn("[JobDiscovery] addJob failed:", err.message, params);
    }
  }

  console.log(`[JobDiscovery] Scan complete — ${created.length} job(s) added.`);
  return created;
}

/**
 * Start periodic polling of all configured sources.
 *
 * @param {Function} addJob      — jobStore.addJob
 * @param {Function} listJobs    — jobStore.listJobs (for dedup)
 * @param {number}   [intervalMs=60000] — poll interval in milliseconds
 * @returns {Function} stop()    — call to cancel the polling interval
 */
function startPolling(addJob, listJobs, intervalMs = 60_000) {
  console.log(`[JobDiscovery] Polling started (interval: ${intervalMs}ms).`);

  // Run immediately, then on each interval
  scanAll(addJob, listJobs).catch(err =>
    console.error("[JobDiscovery] Initial scan error:", err.message)
  );

  const handle = setInterval(() => {
    scanAll(addJob, listJobs).catch(err =>
      console.error("[JobDiscovery] Poll scan error:", err.message)
    );
  }, intervalMs);

  return function stop() {
    clearInterval(handle);
    console.log("[JobDiscovery] Polling stopped.");
  };
}

module.exports = {
  scanAll,
  startPolling,
  // Exposed for targeted testing
  discoverInternal,
  discoverRemoteBoard,
  discoverMockBoard,
  normalise,
  dedup,
};
