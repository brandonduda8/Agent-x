/**
 * heartbeat-monitor.js
 * =============================================================================
 * Periodic liveness checker for all registered agents.
 *
 * Polls the agent registry on a configurable interval and transitions agents
 * through the stale → dead lifecycle when heartbeats are missed.
 *
 * Configuration (environment variables):
 *   HEARTBEAT_INTERVAL_MS  — how often the monitor ticks (default: 15 000 ms)
 *   STALE_THRESHOLD_MS     — time without heartbeat before → stale (default: 30 000 ms)
 *   DEAD_THRESHOLD_MS      — time without heartbeat before → dead  (default: 60 000 ms)
 *
 * Dead-agent callbacks:
 *   External consumers (watchdog, upgrade-manager) subscribe via
 *   `monitor.onDead(callback)` to receive notifications when an agent crosses
 *   the DEAD threshold.
 *
 * Usage:
 *   const HeartbeatMonitor = require('./heartbeat-monitor');
 *   const monitor = new HeartbeatMonitor();
 *   monitor.onDead((agent) => console.log('Dead:', agent.id));
 *   monitor.start();
 *   // later…
 *   monitor.stop();
 * =============================================================================
 */

'use strict';

const registry = require('./agent-registry');

const HEARTBEAT_INTERVAL_MS = Number(process.env.HEARTBEAT_INTERVAL_MS) || 15_000;
const STALE_THRESHOLD_MS    = Number(process.env.STALE_THRESHOLD_MS)    || 30_000;
const DEAD_THRESHOLD_MS     = Number(process.env.DEAD_THRESHOLD_MS)     || 60_000;

class HeartbeatMonitor {
  constructor() {
    this._timer      = null;
    this._deadCbs    = [];
    this._staleCbs   = [];
    this._running    = false;
  }

  /**
   * Register a callback invoked when an agent transitions to `dead`.
   * @param {Function} cb  — (agentRecord) => void
   */
  onDead(cb) {
    if (typeof cb === 'function') this._deadCbs.push(cb);
    return this;
  }

  /**
   * Register a callback invoked when an agent transitions to `stale`.
   * @param {Function} cb  — (agentRecord) => void
   */
  onStale(cb) {
    if (typeof cb === 'function') this._staleCbs.push(cb);
    return this;
  }

  /**
   * Start the heartbeat polling loop.
   */
  start() {
    if (this._running) return;
    this._running = true;
    console.log(
      `[heartbeat-monitor] Started — interval: ${HEARTBEAT_INTERVAL_MS}ms, ` +
      `stale: ${STALE_THRESHOLD_MS}ms, dead: ${DEAD_THRESHOLD_MS}ms`
    );
    this._timer = setInterval(() => this._tick(), HEARTBEAT_INTERVAL_MS);
    // Unref so the timer doesn't prevent process exit in tests
    if (this._timer.unref) this._timer.unref();
  }

  /**
   * Stop the polling loop.
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
   * Perform one liveness check pass across all agents.
   * Exported for direct invocation in tests.
   */
  _tick() {
    const now    = Date.now();
    const agents = registry.listAgents();

    for (const agent of agents) {
      // Only monitor agents that have registered and sent at least one heartbeat
      if (!agent.lastHeartbeat) continue;

      const elapsed = now - new Date(agent.lastHeartbeat).getTime();

      if (elapsed >= DEAD_THRESHOLD_MS && agent.status !== registry.STATUS.DEAD) {
        registry.setStatus(agent.id, registry.STATUS.DEAD);
        registry.incrementMissedHeartbeats(agent.id);
        const updated = registry.getAgent(agent.id);
        console.warn(`[heartbeat-monitor] Agent ${agent.id} (${agent.name}) marked DEAD`);
        this._deadCbs.forEach(cb => { try { cb(updated); } catch {} });

      } else if (
        elapsed >= STALE_THRESHOLD_MS &&
        elapsed <  DEAD_THRESHOLD_MS  &&
        agent.status === registry.STATUS.ACTIVE
      ) {
        registry.setStatus(agent.id, registry.STATUS.STALE);
        registry.incrementMissedHeartbeats(agent.id);
        const updated = registry.getAgent(agent.id);
        console.warn(`[heartbeat-monitor] Agent ${agent.id} (${agent.name}) marked STALE`);
        this._staleCbs.forEach(cb => { try { cb(updated); } catch {} });
      }
    }
  }

  get isRunning() { return this._running; }
}

module.exports = HeartbeatMonitor;
