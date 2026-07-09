/**
 * hermes/job-matcher.js
 * =============================================================================
 * Job-to-agent scoring and routing algorithm for Agent Hermes.
 *
 * ## Scoring model
 *
 * Each (job, agent) pair receives a composite score in the range [0, 100]:
 *
 *  Component                         Weight
 *  ──────────────────────────────────────────
 *  Capability coverage               50 pts   — how many requiredCaps the agent satisfies
 *  Type affinity                     20 pts   — does the agent declare this job type?
 *  Agent load (inverse)              15 pts   — prefer less-loaded agents
 *  Priority boost                    10 pts   — high-priority jobs get a small bias
 *  Status health bonus                5 pts   — prefer "active" over "stale" agents
 *
 * Agents with a score of 0 (zero capability overlap when caps are required)
 * are excluded from routing.
 *
 * ## Usage
 *
 *   const { rankAgents, bestMatch, assignJob } = require("./job-matcher");
 *
 *   // Score all eligible agents for a job
 *   const ranked = rankAgents(job, agentList);
 *
 *   // Return only the top candidate
 *   const winner = bestMatch(job, agentList);
 *
 *   // Score + update job record in the store
 *   const updated = assignJob(job, agentList, jobStore);
 * =============================================================================
 */

"use strict";

// ---------------------------------------------------------------------------
// Weights (sum = 100)
// ---------------------------------------------------------------------------
const W = {
  CAPABILITY : 50,
  TYPE       : 20,
  LOAD       : 15,
  PRIORITY   : 10,
  STATUS     :  5,
};

// ---------------------------------------------------------------------------
// Internal scoring helpers
// ---------------------------------------------------------------------------

/**
 * Compute capability-coverage score.
 *
 * If the job has no requiredCaps, any agent qualifies and gets full marks.
 * Otherwise score = (matched caps / required caps) * W.CAPABILITY.
 *
 * @param {string[]} requiredCaps
 * @param {string[]} agentCaps
 * @returns {number}
 */
function _capabilityScore(requiredCaps, agentCaps) {
  if (!requiredCaps || requiredCaps.length === 0) return W.CAPABILITY;

  const agentSet = new Set((agentCaps || []).map(c => c.toLowerCase()));
  let matched = 0;
  for (const cap of requiredCaps) {
    if (agentSet.has(cap.toLowerCase())) matched++;
  }

  return (matched / requiredCaps.length) * W.CAPABILITY;
}

/**
 * Compute type-affinity score.
 *
 * Checks whether the agent's `types` array (or `capabilities`) includes
 * the job type (case-insensitive partial match allowed).
 *
 * @param {string}   jobType
 * @param {object}   agent
 * @returns {number}
 */
function _typeScore(jobType, agent) {
  if (!jobType || jobType === "generic") return W.TYPE * 0.5; // neutral

  const type  = jobType.toLowerCase();
  const pool  = [
    ...(agent.types        || []),
    ...(agent.capabilities || []),
    agent.type || "",
    agent.name || "",
  ].map(s => s.toLowerCase());

  // Exact match gets full marks; substring match gets half marks
  if (pool.some(p => p === type))         return W.TYPE;
  if (pool.some(p => p.includes(type)))   return W.TYPE * 0.6;
  return 0;
}

/**
 * Compute inverse-load score.
 *
 * agent.currentLoad is expected to be an integer in [0, N].
 * We normalise against a ceiling of 10 active jobs.
 *
 * @param {object} agent
 * @returns {number}
 */
function _loadScore(agent) {
  const CEILING = 10;
  const load    = typeof agent.currentLoad === "number"
    ? Math.max(0, agent.currentLoad)
    : 0;
  // Invert: 0 load → full score, CEILING load → 0 score
  return Math.max(0, (1 - load / CEILING)) * W.LOAD;
}

/**
 * Compute priority-alignment score.
 *
 * High-priority jobs prefer agents with a low existing load — this small
 * boost nudges the matcher toward less-busy agents when stakes are high.
 *
 * @param {number} priority  — job priority 0–10
 * @param {object} agent
 * @returns {number}
 */
function _priorityScore(priority, agent) {
  // Scale: priority 10 → W.PRIORITY pts, priority 0 → 0 pts
  const norm = (typeof priority === "number" ? Math.max(0, Math.min(10, priority)) : 5) / 10;
  // Give the bonus only if agent is not heavily loaded
  const load = typeof agent.currentLoad === "number" ? agent.currentLoad : 0;
  const available = load < 5 ? 1 : 0.3;
  return norm * available * W.PRIORITY;
}

/**
 * Compute status-health score.
 *
 * @param {object} agent
 * @returns {number}
 */
function _statusScore(agent) {
  const status = (agent.status || "").toLowerCase();
  switch (status) {
    case "active"     : return W.STATUS;
    case "registered" : return W.STATUS * 0.6;
    case "stale"      : return W.STATUS * 0.2;
    case "dead"       : return 0;
    default           : return W.STATUS * 0.4;
  }
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Score a single agent against a job.
 *
 * @param {object} job   — job record (from job-store)
 * @param {object} agent — agent record (from registry)
 * @returns {{agentId: string, agentName: string, score: number, breakdown: object}}
 */
function scoreAgent(job, agent) {
  const caps      = _capabilityScore(job.requiredCaps, agent.capabilities);
  const type      = _typeScore(job.type, agent);
  const load      = _loadScore(agent);
  const priority  = _priorityScore(job.priority, agent);
  const status    = _statusScore(agent);

  const total = Math.round(caps + type + load + priority + status);

  return {
    agentId  : agent.id,
    agentName: agent.name || agent.id,
    score    : total,
    breakdown: { caps, type, load, priority, status },
  };
}

/**
 * Rank all eligible agents for a given job, highest score first.
 *
 * Agents scoring 0 (e.g. zero cap overlap when caps are required) are
 * excluded entirely.
 *
 * @param {object}   job
 * @param {object[]} agents  — array of agent records from the registry
 * @returns {Array<{agentId, agentName, score, breakdown}>}
 */
function rankAgents(job, agents) {
  if (!Array.isArray(agents) || agents.length === 0) return [];

  const hasCapReq = Array.isArray(job.requiredCaps) && job.requiredCaps.length > 0;

  return agents
    .filter(a => {
      // Exclude dead or non-existent agents
      if ((a.status || "").toLowerCase() === "dead") return false;
      return true;
    })
    .map(a => scoreAgent(job, a))
    .filter(r => {
      // If job has required caps, discard agents with zero cap coverage
      if (hasCapReq && r.breakdown.caps === 0) return false;
      return r.score > 0;
    })
    .sort((a, b) => b.score - a.score);
}

/**
 * Return the single best-matching agent (or null if no eligible agents).
 *
 * @param {object}   job
 * @param {object[]} agents
 * @returns {{agentId, agentName, score, breakdown}|null}
 */
function bestMatch(job, agents) {
  const ranked = rankAgents(job, agents);
  return ranked.length > 0 ? ranked[0] : null;
}

/**
 * Score, select the best agent, and update the job record in the store.
 *
 * If no eligible agent is found the job remains open and the function
 * returns null.
 *
 * @param {object}   job        — job record
 * @param {object[]} agents     — agent list from registry
 * @param {object}   jobStore   — the job-store module (for updateJob)
 * @returns {object|null}       — updated job record or null
 */
function assignJob(job, agents, jobStore) {
  if (!job || !jobStore) {
    throw new TypeError("[JobMatcher] assignJob: job and jobStore are required.");
  }

  const winner = bestMatch(job, agents);
  if (!winner) {
    console.warn(`[JobMatcher] No eligible agent found for job ${job.id} ("${job.title}").`);
    return null;
  }

  const updated = jobStore.updateJob(job.id, {
    status    : "assigned",
    assignedTo: winner.agentId,
    score     : winner.score,
  });

  console.log(
    `[JobMatcher] Job "${job.title}" (${job.id}) → agent "${winner.agentName}" (score: ${winner.score})`
  );

  return updated;
}

/**
 * Attempt to (re-)assign all open jobs in the store to available agents.
 *
 * @param {object}   jobStore — the job-store module
 * @param {object[]} agents   — current agent list from the registry
 * @returns {{ assigned: number, unmatched: number }}
 */
function assignAllOpen(jobStore, agents) {
  const open      = jobStore.listJobs("open");
  let assigned    = 0;
  let unmatched   = 0;

  for (const job of open) {
    const result = assignJob(job, agents, jobStore);
    if (result) assigned++;
    else        unmatched++;
  }

  return { assigned, unmatched };
}

module.exports = {
  scoreAgent,
  rankAgents,
  bestMatch,
  assignJob,
  assignAllOpen,
  // expose weights for external inspection / testing
  WEIGHTS: { ...W },
};
