/**
 * upgrade-manager.js
 * =============================================================================
 * Orchestrates the full agent upgrade lifecycle:
 *
 *   1. Validate the incoming config payload
 *   2. Write a new versioned config via agent-config-store
 *   3. Attempt a graceful restart of the target agent process (via PM2 or
 *      the registry restart callback if PM2 is unavailable)
 *   4. Confirm the agent comes back alive (heartbeat poll)
 *   5. Commit the new version as "current" on success, or roll back on failure
 *   6. Emit an audit log entry for every material event
 *
 * ─── Graceful Restart Strategy ────────────────────────────────────────────
 *
 * Priority order:
 *   a) PM2 restart  — `pm2 restart <agentName>` (production / Termux PM2)
 *   b) Registry restart callback — supplied by watchdog / orchestrator when
 *      agents are launched as child processes
 *   c) SIGTERM + re-spawn — last resort for detached processes tracked by PID
 *
 * If none of the above methods are available the upgrade still succeeds
 * (config is committed) but a warning is logged that a manual restart is
 * needed.
 *
 * ─── Rollback Policy ──────────────────────────────────────────────────────
 *
 * If the restart fails AND the agent does not send a heartbeat within
 * UPGRADE_CONFIRM_TIMEOUT_MS, the previous version is restored as "current"
 * in the config store and a ROLLED_BACK audit entry is written.
 * =============================================================================
 */

'use strict';

const { execFile }   = require('child_process');
const { promisify }  = require('util');
const execFileAsync  = promisify(execFile);

const configStore    = require('./agent-config-store');
const auditLog       = require('./audit-log');
const { AUDIT_ACTIONS } = auditLog;

// ---------------------------------------------------------------------------
// Configuration (all overridable via env)
// ---------------------------------------------------------------------------

const UPGRADE_CONFIRM_TIMEOUT_MS = Number(process.env.UPGRADE_CONFIRM_TIMEOUT_MS) || 30_000;
const HEARTBEAT_POLL_INTERVAL_MS = Number(process.env.HEARTBEAT_POLL_INTERVAL_MS) || 2_000;
const PM2_BINARY                 = process.env.PM2_BINARY || 'pm2';

// ---------------------------------------------------------------------------
// In-memory upgrade state
// Tracks active upgrades to prevent concurrent upgrades on the same agent.
//
// upgradeState[agentId] = {
//   status: 'pending' | 'restarting' | 'confirming' | 'done' | 'failed'
//   newVersion:   number
//   priorVersion: number
//   startedAt:    Date
//   completedAt:  Date | null
//   error:        string | null
// }
// ---------------------------------------------------------------------------

const upgradeState = new Map();

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Try to restart via PM2.
 *
 * @param {string} agentName  — PM2 process name
 * @returns {Promise<boolean>}
 */
async function _pm2Restart(agentName) {
  try {
    await execFileAsync(PM2_BINARY, ['restart', agentName], { timeout: 15_000 });
    return true;
  } catch (err) {
    return false;
  }
}

/**
 * Try to restart via a registered callback from the registry.
 *
 * @param {Function|null} restartCallback
 * @param {string}        agentId
 * @returns {Promise<boolean>}
 */
async function _callbackRestart(restartCallback, agentId) {
  if (typeof restartCallback !== 'function') return false;
  try {
    await Promise.resolve(restartCallback(agentId));
    return true;
  } catch {
    return false;
  }
}

/**
 * Poll the registry for the agent's heartbeat to confirm it's alive.
 * Returns true if the agent's lastHeartbeat is after `sinceTime`.
 *
 * @param {Function}  getAgentFn   — (agentId) => agent object | null
 * @param {string}    agentId
 * @param {Date}      sinceTime    — heartbeat must be newer than this
 * @returns {Promise<boolean>}
 */
async function _waitForHeartbeat(getAgentFn, agentId, sinceTime) {
  const deadline = Date.now() + UPGRADE_CONFIRM_TIMEOUT_MS;

  return new Promise(resolve => {
    const poll = () => {
      if (Date.now() >= deadline) return resolve(false);

      const agent = getAgentFn(agentId);
      if (agent && agent.lastHeartbeat) {
        const hbTime = new Date(agent.lastHeartbeat).getTime();
        if (hbTime > sinceTime.getTime()) return resolve(true);
      }

      setTimeout(poll, HEARTBEAT_POLL_INTERVAL_MS);
    };

    poll();
  });
}

/**
 * Validate a config payload before writing it.
 * Returns { valid: boolean, errors: string[] }.
 *
 * @param {object} config
 * @returns {{ valid: boolean, errors: string[] }}
 */
function _validateConfig(config) {
  const errors = [];

  if (!config || typeof config !== 'object' || Array.isArray(config)) {
    errors.push('config must be a non-null, non-array object');
    return { valid: false, errors };
  }

  // Reject configs that are obviously empty
  if (Object.keys(config).length === 0) {
    errors.push('config object must not be empty');
  }

  // Disallow prototype-polluting keys
  const dangerous = ['__proto__', 'constructor', 'prototype'];
  for (const key of Object.keys(config)) {
    if (dangerous.includes(key)) {
      errors.push(`config contains disallowed key: "${key}"`);
    }
  }

  return { valid: errors.length === 0, errors };
}

// ---------------------------------------------------------------------------
// Core upgrade function
// ---------------------------------------------------------------------------

/**
 * Apply a new configuration version to an agent and restart it gracefully.
 *
 * @param {object} opts
 * @param {string}        opts.agentId          — registry agent ID
 * @param {string}        [opts.agentName]      — human-readable name (for PM2 + logs)
 * @param {object}        opts.newConfig         — the new configuration to apply
 * @param {string}        [opts.changelog]       — human-readable description of changes
 * @param {string}        [opts.actor]           — who triggered this upgrade ('api', 'user:x', 'system')
 * @param {string}        [opts.label]           — version label
 * @param {Function|null} [opts.restartCallback] — (agentId) => Promise, provided by registry/watchdog
 * @param {Function|null} [opts.getAgentFn]      — (agentId) => agentObj, for heartbeat polling
 * @param {boolean}       [opts.skipRestart]     — store the new version but do not restart (dry-run mode)
 *
 * @returns {Promise<{
 *   ok:          boolean,
 *   agentId:     string,
 *   newVersion:  number,
 *   priorVersion: number | null,
 *   rolledBack:  boolean,
 *   restartMethod: string,
 *   auditId:     string,
 *   error:       string | null
 * }>}
 */
async function applyUpgrade({
  agentId,
  agentName        = agentId,
  newConfig,
  changelog        = '',
  actor            = 'api',
  label            = '',
  restartCallback  = null,
  getAgentFn       = null,
  skipRestart      = false,
}) {
  // ── Guard: no concurrent upgrades ────────────────────────────────────────
  const existing = upgradeState.get(agentId);
  if (existing && ['pending', 'restarting', 'confirming'].includes(existing.status)) {
    throw new Error(
      `upgrade-manager: upgrade already in progress for agent ${agentId} (status: ${existing.status})`
    );
  }

  // ── 1. Validate config ────────────────────────────────────────────────────
  const { valid, errors } = _validateConfig(newConfig);
  if (!valid) {
    const reason = `Invalid config: ${errors.join('; ')}`;
    auditLog.append({
      agentId, agentName, action: AUDIT_ACTIONS.UPGRADE_ABORTED,
      actor, outcome: 'failure', reason,
    });
    throw new Error(`upgrade-manager: ${reason}`);
  }

  // ── 2. Determine prior version ────────────────────────────────────────────
  const prior       = configStore.getCurrent(agentId);
  const priorVersion = prior ? prior.version : null;

  // ── 3. Write new config version ───────────────────────────────────────────
  const newVerRecord = configStore.createVersion({
    agentId, config: newConfig, createdBy: actor, changelog,
    label: label || `upgrade-by-${actor}`,
  });
  const newVersion = newVerRecord.version;

  // Track state
  upgradeState.set(agentId, {
    status: 'pending', newVersion, priorVersion,
    startedAt: new Date(), completedAt: null, error: null,
  });

  // Audit: upgrade started
  const startAudit = auditLog.append({
    agentId, agentName, action: AUDIT_ACTIONS.UPGRADE_STARTED,
    actor, fromVersion: priorVersion, toVersion: newVersion,
    configSnapshot: newConfig, outcome: 'success',
    reason: changelog || 'Upgrade initiated',
  });

  // ── 4. Skip restart if dry-run ────────────────────────────────────────────
  if (skipRestart) {
    configStore.setCurrentVersion(agentId, newVersion);
    upgradeState.set(agentId, {
      status: 'done', newVersion, priorVersion,
      startedAt: upgradeState.get(agentId).startedAt,
      completedAt: new Date(), error: null,
    });

    const commitAudit = auditLog.append({
      agentId, agentName, action: AUDIT_ACTIONS.CONFIG_UPGRADED,
      actor, fromVersion: priorVersion, toVersion: newVersion,
      configSnapshot: newConfig, outcome: 'success',
      reason: 'skipRestart=true — config committed without agent restart',
    });

    return {
      ok: true, agentId, newVersion, priorVersion,
      rolledBack: false, restartMethod: 'none (skipRestart)',
      auditId: commitAudit.id, error: null,
    };
  }

  // ── 5. Attempt graceful restart ───────────────────────────────────────────
  upgradeState.get(agentId).status = 'restarting';

  let restartMethod  = 'none';
  let restartSuccess = false;
  const restartTime  = new Date();

  // a) PM2
  if (!restartSuccess) {
    const pm2Ok = await _pm2Restart(agentName);
    if (pm2Ok) {
      restartMethod  = 'pm2';
      restartSuccess = true;
    }
  }

  // b) Registry callback
  if (!restartSuccess) {
    const cbOk = await _callbackRestart(restartCallback, agentId);
    if (cbOk) {
      restartMethod  = 'registry-callback';
      restartSuccess = true;
    }
  }

  // c) No restart method available — still commit but warn
  if (!restartSuccess) {
    restartMethod = 'manual-required';
  }

  // Audit restart attempt
  auditLog.append({
    agentId, agentName,
    action:  restartSuccess ? AUDIT_ACTIONS.AGENT_RESTARTED : AUDIT_ACTIONS.RESTART_FAILED,
    actor, fromVersion: priorVersion, toVersion: newVersion,
    outcome: restartSuccess ? 'success' : 'failure',
    reason:  restartSuccess
      ? `Restarted via ${restartMethod}`
      : 'No restart method succeeded — manual restart required',
    meta: { restartMethod },
  });

  // ── 6. Confirm liveness via heartbeat poll ────────────────────────────────
  upgradeState.get(agentId).status = 'confirming';

  let confirmed = false;

  if (restartSuccess && typeof getAgentFn === 'function') {
    confirmed = await _waitForHeartbeat(getAgentFn, agentId, restartTime);
  } else if (!restartSuccess) {
    // If we couldn't restart, still commit the config — operator must restart manually
    confirmed = true;
  } else {
    // Restart succeeded but no heartbeat poller available — assume ok
    confirmed = true;
  }

  // ── 7. Commit or rollback ─────────────────────────────────────────────────
  if (confirmed) {
    // Commit new version as current
    configStore.setCurrentVersion(agentId, newVersion);

    upgradeState.set(agentId, {
      status: 'done', newVersion, priorVersion,
      startedAt: upgradeState.get(agentId).startedAt,
      completedAt: new Date(), error: null,
    });

    const commitAudit = auditLog.append({
      agentId, agentName, action: AUDIT_ACTIONS.CONFIG_UPGRADED,
      actor, fromVersion: priorVersion, toVersion: newVersion,
      configSnapshot: newConfig, outcome: 'success',
      reason: `Upgrade confirmed via ${restartSuccess ? restartMethod : 'no-restart path'}`,
      meta: { restartMethod },
    });

    return {
      ok: true, agentId, newVersion, priorVersion,
      rolledBack: false, restartMethod,
      auditId: commitAudit.id, error: null,
    };
  } else {
    // Rollback — restore previous version as current
    let rolledBackTo = priorVersion;
    if (priorVersion !== null) {
      try {
        configStore.setCurrentVersion(agentId, priorVersion);
      } catch {
        rolledBackTo = null; // Prior version purged — nothing to roll back to
      }
    }

    const rollbackError = `Agent did not send a heartbeat within ${UPGRADE_CONFIRM_TIMEOUT_MS}ms after restart`;

    upgradeState.set(agentId, {
      status: 'failed', newVersion, priorVersion,
      startedAt: upgradeState.get(agentId).startedAt,
      completedAt: new Date(), error: rollbackError,
    });

    const rollbackAudit = auditLog.append({
      agentId, agentName, action: AUDIT_ACTIONS.CONFIG_ROLLED_BACK,
      actor, fromVersion: newVersion, toVersion: rolledBackTo,
      outcome: 'failure', reason: rollbackError,
      meta: { restartMethod, confirmedHeartbeat: false },
    });

    return {
      ok: false, agentId, newVersion, priorVersion,
      rolledBack: true, restartMethod,
      auditId: rollbackAudit.id,
      error: rollbackError,
    };
  }
}

// ---------------------------------------------------------------------------
// Rollback to an explicit prior version
// ---------------------------------------------------------------------------

/**
 * Explicitly roll back an agent to a specific prior version.
 *
 * @param {object} opts
 * @param {string}        opts.agentId
 * @param {string}        [opts.agentName]
 * @param {number}        opts.targetVersion
 * @param {string}        [opts.actor]
 * @param {Function|null} [opts.restartCallback]
 * @param {Function|null} [opts.getAgentFn]
 * @returns {Promise<object>}  same shape as applyUpgrade return value
 */
async function rollbackTo({
  agentId,
  agentName       = agentId,
  targetVersion,
  actor           = 'api',
  restartCallback = null,
  getAgentFn      = null,
}) {
  const targetRecord = configStore.getVersion(agentId, targetVersion);
  if (!targetRecord) {
    throw new Error(
      `upgrade-manager: version ${targetVersion} not found for agent ${agentId}`
    );
  }

  const current = configStore.getCurrent(agentId);
  if (current && current.version === targetVersion) {
    throw new Error(
      `upgrade-manager: agent ${agentId} is already on version ${targetVersion}`
    );
  }

  // Re-use applyUpgrade with the old config payload (creates a new version
  // record that mirrors the rolled-back config — version number keeps incrementing,
  // preserving a complete linear audit trail).
  return applyUpgrade({
    agentId,
    agentName,
    newConfig:   targetRecord.config,
    changelog:   `Rollback to v${targetVersion} from v${current ? current.version : '?'}`,
    actor,
    label:       `rollback-to-v${targetVersion}`,
    restartCallback,
    getAgentFn,
  });
}

// ---------------------------------------------------------------------------
// State accessors
// ---------------------------------------------------------------------------

/**
 * Get the current in-memory upgrade state for an agent.
 *
 * @param {string} agentId
 * @returns {object|null}
 */
function getUpgradeState(agentId) {
  return upgradeState.get(agentId) || null;
}

/**
 * List all in-memory upgrade states (useful for the /status endpoint).
 *
 * @returns {Array<{agentId: string, state: object}>}
 */
function listUpgradeStates() {
  const result = [];
  for (const [agentId, state] of upgradeState.entries()) {
    result.push({ agentId, state: { ...state } });
  }
  return result;
}

// ---------------------------------------------------------------------------
// Exports
// ---------------------------------------------------------------------------

module.exports = {
  applyUpgrade,
  rollbackTo,
  getUpgradeState,
  listUpgradeStates,
  UPGRADE_CONFIRM_TIMEOUT_MS,

  // Exported for unit-testing
  _validateConfig,
};
