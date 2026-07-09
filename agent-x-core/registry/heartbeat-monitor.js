/**
 * Heartbeat Monitor
 * =============================================================================
 * Runs a periodic check (every HEARTBEAT_INTERVAL_MS) that:
 *   1. Calls markStaleAgents() to demote agents that have missed heartbeats.
 *   2. Logs a summary of active / idle / stale / offline counts.
 *   3. Emits structured events so other parts of the system can react.
 *
 * Configuration (via .env / process.env):
 *   HEARTBEAT_INTERVAL_MS  — how often to run the check (default: 30 000 ms)
 *   HEARTBEAT_STALE_MS     — age at which an agent is considered stale (default: 60 000 ms)
 *
 * Lifecycle:
 *   const monitor = require('./heartbeat-monitor');
 *   monitor.start();   // begin periodic checks
 *   monitor.stop();    // clear the timer (e.g. during graceful shutdown)
 *   monitor.tick();    // run one check synchronously (useful in tests)
 *   monitor.summary(); // return current counts without running stale check
 * =============================================================================
 */

'use strict';

const { EventEmitter } = require('events');
const registry = require('./agent-registry');

// --------------------------------------------------------------------------- #
// Configuration
// --------------------------------------------------------------------------- #

/** How frequently (ms) the monitor fires. Default: 30 s */
const HEARTBEAT_INTERVAL_MS = parseInt(
  process.env.HEARTBEAT_INTERVAL_MS || '30000',
  10,
);

/** Age (ms) after which a non-heartbeating agent is marked stale. Default: 60 s */
const HEARTBEAT_STALE_MS = parseInt(
  process.env.HEARTBEAT_STALE_MS || '60000',
  10,
);

// --------------------------------------------------------------------------- #
// Monitor class
// --------------------------------------------------------------------------- #

class HeartbeatMonitor extends EventEmitter {
  constructor() {
    super();
    this._timer     = null;
    this._running   = false;
    this._tickCount = 0;
  }

  // ------------------------------------------------------------------ //
  // Public API
  // ------------------------------------------------------------------ //

  /**
   * Start the periodic heartbeat check.
   * Calling start() when already running is a no-op.
   */
  start() {
    if (this._running) return;
    this._running = true;

    console.log(
      `[heartbeat-monitor] Started — interval: ${HEARTBEAT_INTERVAL_MS}ms, ` +
      `stale threshold: ${HEARTBEAT_STALE_MS}ms`,
    );

    this._timer = setInterval(() => this.tick(), HEARTBEAT_INTERVAL_MS);

    // setInterval does not prevent the process from exiting in test
    // environments — unref() ensures it's not the last thing keeping Node up.
    if (this._timer.unref) this._timer.unref();
  }

  /**
   * Stop the periodic check. Safe to call multiple times.
   */
  stop() {
    if (this._timer) {
      clearInterval(this._timer);
      this._timer = null;
    }
    this._running = false;
    console.log('[heartbeat-monitor] Stopped.');
  }

  /**
   * Execute one heartbeat scan immediately (also called by the interval).
   * Emits:
   *   "tick"   { tickCount, summary }
   *   "stale"  { agents: [...] }   — only when agents become stale
   */
  tick() {
    this._tickCount += 1;

    let staled = [];
    try {
      staled = registry.markStaleAgents(HEARTBEAT_STALE_MS);
    } catch (err) {
      console.error('[heartbeat-monitor] Error running markStaleAgents:', err.message);
      this.emit('error', err);
      return;
    }

    if (staled.length > 0) {
      const names = staled.map((a) => `${a.name} (${a.id})`).join(', ');
      console.warn(
        `[heartbeat-monitor] Tick #${this._tickCount} — ` +
        `${staled.length} agent(s) marked stale: ${names}`,
      );
      this.emit('stale', { agents: staled });
    } else {
      console.log(
        `[heartbeat-monitor] Tick #${this._tickCount} — ` +
        `no new stale agents`,
      );
    }

    const sum = this.summary();
    this.emit('tick', { tickCount: this._tickCount, summary: sum });
    return sum;
  }

  /**
   * Return current agent counts by status without mutating anything.
   * @returns {{ total: number, active: number, idle: number, stale: number, offline: number }}
   */
  summary() {
    let all;
    try {
      all = registry.listAgents();
    } catch (_) {
      all = [];
    }

    const counts = { total: all.length, active: 0, idle: 0, stale: 0, offline: 0 };
    for (const a of all) {
      if (counts[a.status] !== undefined) counts[a.status] += 1;
    }
    return counts;
  }

  /** Whether the monitor is currently running. */
  get isRunning() {
    return this._running;
  }

  /** Number of ticks fired since start(). */
  get tickCount() {
    return this._tickCount;
  }

  /** Configured interval in milliseconds. */
  get intervalMs() {
    return HEARTBEAT_INTERVAL_MS;
  }

  /** Configured stale threshold in milliseconds. */
  get staleMs() {
    return HEARTBEAT_STALE_MS;
  }
}

// --------------------------------------------------------------------------- #
// Singleton export
// --------------------------------------------------------------------------- #
const monitor = new HeartbeatMonitor();

module.exports = monitor;
