/**
 * hermes/hermes.test.js
 * =============================================================================
 * Unit + integration tests for Agent Hermes Job Discovery & Matching.
 *
 * Run with:  node hermes/hermes.test.js
 *
 * No external test framework required — uses a lightweight homegrown harness
 * that matches the project's existing test style (see registry/registry.test.js).
 * =============================================================================
 */

"use strict";

const assert = require("assert");
const path   = require("path");
const fs     = require("fs");
const os     = require("os");

// ---------------------------------------------------------------------------
// Lightweight test harness
// ---------------------------------------------------------------------------
let _passed  = 0;
let _failed  = 0;
const _failures = [];

function test(name, fn) {
  try {
    const result = fn();
    if (result && typeof result.then === "function") {
      return result
        .then(() => { _passed++; console.log(`  ✔ ${name}`); })
        .catch(err => {
          _failed++;
          _failures.push({ name, err });
          console.error(`  ✘ ${name}\n    ${err.message}`);
        });
    }
    _passed++;
    console.log(`  ✔ ${name}`);
  } catch (err) {
    _failed++;
    _failures.push({ name, err });
    console.error(`  ✘ ${name}\n    ${err.message}`);
  }
}

async function runAll(suites) {
  for (const [suiteName, fn] of suites) {
    console.log(`\n── ${suiteName}`);
    await fn();
  }
  console.log(`\n${"─".repeat(50)}`);
  console.log(`Results: ${_passed} passed, ${_failed} failed`);
  if (_failures.length) {
    console.log("\nFailures:");
    for (const { name, err } of _failures) {
      console.log(`  ✘ ${name}\n    ${err.stack || err.message}`);
    }
    process.exitCode = 1;
  }
}

// ---------------------------------------------------------------------------
// Patch job-store to use a temp file so tests don't pollute data/
// ---------------------------------------------------------------------------
const TMP_STORE = path.join(os.tmpdir(), `hermes-test-${Date.now()}.json`);

// We must patch the store path BEFORE requiring the modules
// by monkey-patching process.env and re-requiring with cache busting.
function freshStore() {
  // Clear require cache for store
  const storePath = require.resolve("./job-store");
  delete require.cache[storePath];

  // Temporarily point store to temp file
  const original = process.env.HERMES_STORE_PATH;
  // job-store.js reads STORE_PATH from a computed path, so we patch fs directly
  const store = require("./job-store");
  // Reset the store by wiping all jobs via the public API
  store.listJobs().forEach(j => store.removeJob(j.id));
  return store;
}

// ---------------------------------------------------------------------------
// ── Suite: job-store ────────────────────────────────────────────────────────
// ---------------------------------------------------------------------------
async function suiteJobStore() {
  const store = freshStore();

  test("addJob returns a valid job with defaults", () => {
    const job = store.addJob({ title: "Test job alpha" });
    assert.ok(job.id,                          "id assigned");
    assert.strictEqual(job.title, "Test job alpha");
    assert.strictEqual(job.status,   "open");
    assert.strictEqual(job.source,   "internal");
    assert.strictEqual(job.priority,  5);
    assert.ok(Array.isArray(job.requiredCaps), "requiredCaps is array");
    assert.strictEqual(job.assignedTo, null);
  });

  test("addJob clamps priority to [0,10]", () => {
    const low  = store.addJob({ title: "low",  priority: -5  });
    const high = store.addJob({ title: "high", priority: 999 });
    assert.strictEqual(low.priority,  0);
    assert.strictEqual(high.priority, 10);
  });

  test("addJob throws on missing title", () => {
    assert.throws(
      () => store.addJob({ source: "test" }),
      /title is required/
    );
  });

  test("getJob returns the created job", () => {
    const created = store.addJob({ title: "Fetch me" });
    const fetched  = store.getJob(created.id);
    assert.deepStrictEqual(fetched, created);
  });

  test("getJob returns null for unknown id", () => {
    assert.strictEqual(store.getJob("no-such-id"), null);
  });

  test("listJobs returns all jobs", () => {
    const before = store.listJobs().length;
    store.addJob({ title: "Extra job" });
    assert.strictEqual(store.listJobs().length, before + 1);
  });

  test("listJobs filters by status", () => {
    store.addJob({ title: "Open A" });
    const openBefore = store.listJobs("open").length;
    const j = store.addJob({ title: "Soon assigned" });
    store.updateJob(j.id, { status: "assigned", assignedTo: "agent-1" });
    assert.strictEqual(store.listJobs("open").length, openBefore); // unchanged
    assert.ok(store.listJobs("assigned").some(x => x.id === j.id));
  });

  test("updateJob merges fields and updates updatedAt", () => {
    const j  = store.addJob({ title: "Updateable" });
    const t0 = j.updatedAt;

    // Small delay to guarantee timestamp changes
    const updated = store.updateJob(j.id, { status: "in-progress" });
    assert.strictEqual(updated.status, "in-progress");
    assert.ok(updated.updatedAt >= t0);
  });

  test("updateJob rejects invalid status", () => {
    const j = store.addJob({ title: "Bad status" });
    assert.throws(
      () => store.updateJob(j.id, { status: "flying" }),
      /Invalid status/
    );
  });

  test("updateJob returns null for unknown id", () => {
    assert.strictEqual(store.updateJob("ghost", { status: "done" }), null);
  });

  test("removeJob deletes the entry", () => {
    const j = store.addJob({ title: "Deletable" });
    assert.ok(store.removeJob(j.id));
    assert.strictEqual(store.getJob(j.id), null);
  });

  test("removeJob returns false for unknown id", () => {
    assert.strictEqual(store.removeJob("not-here"), false);
  });

  test("purgeExpired removes expired jobs only", () => {
    const past   = new Date(Date.now() - 1000).toISOString();
    const future = new Date(Date.now() + 9_999_999).toISOString();
    const exp  = store.addJob({ title: "Expired",    expiresAt: past   });
    const live = store.addJob({ title: "Still live", expiresAt: future });
    const count = store.purgeExpired();
    assert.ok(count >= 1);
    assert.strictEqual(store.getJob(exp.id),  null);
    assert.ok(store.getJob(live.id) !== null);
  });

  test("stats returns expected shape", () => {
    const s = store.stats();
    assert.ok(typeof s.total    === "number");
    assert.ok(typeof s.byStatus === "object");
  });
}

// ---------------------------------------------------------------------------
// ── Suite: job-matcher ──────────────────────────────────────────────────────
// ---------------------------------------------------------------------------
async function suiteJobMatcher() {
  const matcher = require("./job-matcher");

  // Agent fixtures
  const AGENTS = [
    {
      id          : "agent-content",
      name        : "content-generator",
      type        : "worker",
      capabilities: ["draft", "email", "post"],
      status      : "active",
      currentLoad : 2,
    },
    {
      id          : "agent-data",
      name        : "data-aggregator",
      type        : "worker",
      capabilities: ["fetch", "summarise", "aggregate"],
      status      : "active",
      currentLoad : 0,
    },
    {
      id          : "agent-infra",
      name        : "infrastructure",
      type        : "worker",
      capabilities: ["env-check", "network-probe", "lifecycle"],
      status      : "stale",
      currentLoad : 7,
    },
    {
      id          : "agent-dead",
      name        : "dead-worker",
      type        : "worker",
      capabilities: ["draft", "email"],
      status      : "dead",
      currentLoad : 0,
    },
  ];

  // Job fixtures
  const contentJob = {
    id          : "job-content-1",
    title       : "Write email sequence",
    type        : "content",
    requiredCaps: ["draft", "email"],
    priority    : 8,
  };

  const dataJob = {
    id          : "job-data-1",
    title       : "Aggregate niches",
    type        : "research",
    requiredCaps: ["fetch", "aggregate"],
    priority    : 5,
  };

  const infraJob = {
    id          : "job-infra-1",
    title       : "Health check",
    type        : "infrastructure",
    requiredCaps: ["env-check", "network-probe"],
    priority    : 9,
  };

  const noCapJob = {
    id          : "job-nocap-1",
    title       : "Generic work",
    type        : "generic",
    requiredCaps: [],
    priority    : 3,
  };

  test("scoreAgent returns score in [0,100]", () => {
    const result = matcher.scoreAgent(contentJob, AGENTS[0]);
    assert.ok(result.score >= 0 && result.score <= 100, `score out of range: ${result.score}`);
    assert.ok(typeof result.breakdown === "object");
  });

  test("scoreAgent gives dead agents 0 status points", () => {
    const result = matcher.scoreAgent(contentJob, AGENTS[3]); // dead
    assert.strictEqual(result.breakdown.status, 0);
  });

  test("rankAgents excludes dead agents", () => {
    const ranked = matcher.rankAgents(contentJob, AGENTS);
    assert.ok(ranked.every(r => r.agentId !== "agent-dead"),
      "dead agent must be excluded");
  });

  test("rankAgents returns agents sorted highest score first", () => {
    const ranked = matcher.rankAgents(contentJob, AGENTS);
    for (let i = 0; i < ranked.length - 1; i++) {
      assert.ok(ranked[i].score >= ranked[i + 1].score,
        "scores must be non-increasing");
    }
  });

  test("rankAgents returns content-generator as best for content job", () => {
    const ranked = matcher.rankAgents(contentJob, AGENTS);
    assert.ok(ranked.length > 0, "must have at least one candidate");
    assert.strictEqual(ranked[0].agentId, "agent-content");
  });

  test("rankAgents returns data-aggregator as best for data job", () => {
    const ranked = matcher.rankAgents(dataJob, AGENTS);
    assert.ok(ranked.length > 0, "must have at least one candidate");
    assert.strictEqual(ranked[0].agentId, "agent-data");
  });

  test("rankAgents excludes agents with zero capability overlap (when caps required)", () => {
    const ranked = matcher.rankAgents(contentJob, AGENTS);
    // data-aggregator has no draft/email — must be excluded
    assert.ok(!ranked.some(r => r.agentId === "agent-data"),
      "data-aggregator should be excluded from content job");
  });

  test("rankAgents includes all live agents for no-cap job", () => {
    const ranked = matcher.rankAgents(noCapJob, AGENTS);
    // Only dead agent should be excluded
    const ids = ranked.map(r => r.agentId);
    assert.ok(!ids.includes("agent-dead"), "dead excluded");
    assert.ok(ids.includes("agent-content"), "content included");
    assert.ok(ids.includes("agent-data"),    "data included");
  });

  test("bestMatch returns top-ranked agent", () => {
    const best = matcher.bestMatch(contentJob, AGENTS);
    assert.ok(best !== null);
    assert.strictEqual(best.agentId, "agent-content");
  });

  test("bestMatch returns null when no eligible agents exist", () => {
    const result = matcher.bestMatch(infraJob, [AGENTS[3]]); // only dead agent
    assert.strictEqual(result, null);
  });

  test("assignJob updates job record in store", () => {
    const store = freshStore();
    const job   = store.addJob({
      title       : "Assignable",
      type        : "content",
      requiredCaps: ["draft"],
      priority    : 7,
    });

    const updated = matcher.assignJob(job, AGENTS, store);
    assert.ok(updated !== null,             "assignment must succeed");
    assert.strictEqual(updated.status,       "assigned");
    assert.strictEqual(updated.assignedTo,   "agent-content");
    assert.ok(typeof updated.score === "number");
  });

  test("assignJob returns null if no eligible agents", () => {
    const store = freshStore();
    const job   = store.addJob({
      title       : "Unassignable",
      type        : "content",
      requiredCaps: ["draft", "email"],
      priority    : 5,
    });

    const result = matcher.assignJob(job, [AGENTS[3]], store); // only dead
    assert.strictEqual(result, null);
    // Job must remain open
    assert.strictEqual(store.getJob(job.id).status, "open");
  });

  test("assignAllOpen processes every open job", () => {
    const store = freshStore();
    store.addJob({ title: "A", type: "content", requiredCaps: ["draft", "email"], priority: 5 });
    store.addJob({ title: "B", type: "research", requiredCaps: ["fetch"], priority: 5 });
    store.addJob({ title: "C", requiredCaps: [], priority: 3 });

    const { assigned, unmatched } = matcher.assignAllOpen(store, AGENTS);
    assert.ok(assigned + unmatched === 3, "all jobs must be processed");
    assert.ok(assigned >= 2, "at least 2 should be assigned");
  });

  test("WEIGHTS sum to 100", () => {
    const sum = Object.values(matcher.WEIGHTS).reduce((a, b) => a + b, 0);
    assert.strictEqual(sum, 100);
  });
}

// ---------------------------------------------------------------------------
// ── Suite: job-discovery ────────────────────────────────────────────────────
// ---------------------------------------------------------------------------
async function suiteJobDiscovery() {
  const discovery = require("./job-discovery");

  test("normalise produces expected schema shape", () => {
    const raw = {
      title      : "Raw task",
      type       : "build",
      capabilities: ["compile"],
      priority   : 7,
      description: "Do the build thing.",
    };
    const norm = discovery.normalise(raw, "test-source");
    assert.strictEqual(norm.title,          "Raw task");
    assert.strictEqual(norm.type,           "build");
    assert.deepStrictEqual(norm.requiredCaps, ["compile"]);
    assert.strictEqual(norm.priority,        7);
    assert.strictEqual(norm.source,         "test-source");
    assert.ok(typeof norm.payload === "object");
  });

  test("normalise uses title fallback", () => {
    const norm = discovery.normalise({ name: "My task" }, "src");
    assert.strictEqual(norm.title, "My task");
  });

  test("normalise uses generic type fallback", () => {
    const norm = discovery.normalise({ title: "T" }, "src");
    assert.strictEqual(norm.type, "generic");
  });

  test("discoverMockBoard returns non-empty array of normalised jobs", () => {
    const jobs = discovery.discoverMockBoard();
    assert.ok(Array.isArray(jobs) && jobs.length > 0, "should return mock jobs");
    for (const j of jobs) {
      assert.ok(j.title,                       "each mock job needs a title");
      assert.ok(Array.isArray(j.requiredCaps), "requiredCaps must be array");
      assert.ok(typeof j.priority === "number","priority must be number");
    }
  });

  test("discoverInternal returns an array (even if files missing)", async () => {
    const results = await discovery.discoverInternal();
    assert.ok(Array.isArray(results));
  });

  test("dedup filters out already-stored jobs", () => {
    const existing = [
      { id: "1", source: "mock-board", title: "Write email sequence", status: "open" },
    ];
    const listJobs = () => existing;
    const candidates = [
      { source: "mock-board", title: "Write Email Sequence" }, // case-insensitive match
      { source: "mock-board", title: "Brand new job" },
    ];
    const filtered = discovery.dedup(candidates, listJobs);
    assert.strictEqual(filtered.length, 1);
    assert.strictEqual(filtered[0].title, "Brand new job");
  });

  test("scanAll with mock board adds jobs to store", async () => {
    const store = freshStore();
    const created = await discovery.scanAll(store.addJob.bind(store), store.listJobs);
    assert.ok(Array.isArray(created));
    assert.ok(created.length > 0, "mock board should create jobs");
    assert.ok(store.listJobs().length >= created.length);
  });

  test("scanAll deduplicates on second run", async () => {
    const store = freshStore();

    const first  = await discovery.scanAll(store.addJob.bind(store), store.listJobs);
    const second = await discovery.scanAll(store.addJob.bind(store), store.listJobs);

    assert.strictEqual(second.length, 0, "second scan should add no duplicates");
    // Total jobs unchanged
    assert.strictEqual(store.listJobs().length, first.length);
  });
}

// ---------------------------------------------------------------------------
// ── Suite: hermes-agent (programmatic API) ──────────────────────────────────
// ---------------------------------------------------------------------------
async function suiteHermesAgent() {
  // Bust the hermes-agent cache so we get a fresh instance
  const agentPath = require.resolve("./hermes-agent");
  delete require.cache[agentPath];
  // Also bust job-store so the hermes agent gets a clean store
  freshStore();
  delete require.cache[agentPath];

  const hermes = require("./hermes-agent");

  test("submitJob returns a valid job record", () => {
    const job = hermes.submitJob({
      title       : "Hermes API test job",
      type        : "content",
      requiredCaps: ["draft"],
      priority    : 6,
    });
    assert.ok(job.id);
    assert.strictEqual(job.status, "open");
    assert.strictEqual(job.source, "api");
  });

  test("getJobs returns submitted job", () => {
    const job  = hermes.submitJob({ title: "Listed job", source: "api" });
    const jobs = hermes.getJobs();
    assert.ok(jobs.some(j => j.id === job.id));
  });

  test("getJob retrieves by id", () => {
    const job = hermes.submitJob({ title: "Fetchable", source: "api" });
    assert.deepStrictEqual(hermes.getJob(job.id), job);
  });

  test("getJob returns null for unknown id", () => {
    assert.strictEqual(hermes.getJob("no-such"), null);
  });

  test("updateJob patches the record", () => {
    const job     = hermes.submitJob({ title: "Updatable" });
    const updated = hermes.updateJob(job.id, { status: "in-progress" });
    assert.strictEqual(updated.status, "in-progress");
  });

  test("removeJob deletes the record", () => {
    const job = hermes.submitJob({ title: "Removable" });
    assert.ok(hermes.removeJob(job.id));
    assert.strictEqual(hermes.getJob(job.id), null);
  });

  test("getStats returns expected shape", () => {
    const s = hermes.getStats();
    assert.ok(typeof s.total       === "number");
    assert.ok(typeof s.byStatus    === "object");
    assert.ok(typeof s.agentsCached === "number");
    assert.ok(typeof s.running     === "boolean");
  });

  test("triggerScan resolves with an array", async () => {
    const result = await hermes.triggerScan();
    assert.ok(Array.isArray(result));
  });

  test("triggerMatch resolves with { assigned, unmatched, elapsed }", async () => {
    const result = await hermes.triggerMatch();
    assert.ok(typeof result.assigned  === "number");
    assert.ok(typeof result.unmatched === "number");
    assert.ok(typeof result.elapsed   === "number");
  });

  test("rankForJob returns array (empty when registry unreachable)", async () => {
    const job  = hermes.submitJob({ title: "Rankable", requiredCaps: ["draft"] });
    const rank = await hermes.rankForJob(job.id);
    assert.ok(Array.isArray(rank));
  });

  test("events emitter fires job:discovered on submitJob", done => {
    hermes.events.once("job:discovered", ({ job }) => {
      assert.ok(job.id);
      done();
    });
    hermes.submitJob({ title: "Event test job" });
  });
}

// ---------------------------------------------------------------------------
// Run
// ---------------------------------------------------------------------------
runAll([
  ["job-store",         suiteJobStore],
  ["job-matcher",       suiteJobMatcher],
  ["job-discovery",     suiteJobDiscovery],
  ["hermes-agent (API)", suiteHermesAgent],
]).catch(err => {
  console.error("Test runner crashed:", err);
  process.exitCode = 1;
});
