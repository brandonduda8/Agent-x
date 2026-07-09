/**
 * agent-x-core/pipeline/hermes-pipeline.js
 *
 * AgentHermes Autonomous Build Pipeline
 * ──────────────────────────────────────
 * Responsibilities:
 *  1. Poll for work (internal queue + optional external Hermes job source)
 *  2. Match tasks to capable, healthy agents from the registry
 *  3. Dispatch tasks to agent runners via the orchestrator bridge
 *  4. Monitor completion; surface results
 *  5. Requeue failures with exponential backoff (max 3 retries)
 *  6. Emit granular status events for the WebSocket bus
 *
 * Event surface (emitted on `bus`):
 *   pipeline:started          { at }
 *   pipeline:stopped          { at }
 *   pipeline:poll             { pendingCount, assignedCount }
 *   pipeline:task:dispatched  { task, agent }
 *   pipeline:task:completed   { task, result }
 *   pipeline:task:failed      { task, error, attempt }
 *   pipeline:task:dead        { task }
 *   pipeline:no-agents        { task }
 *   pipeline:error            { error }
 */

'use strict';

const { EventEmitter } = require('events');
const { TaskQueue }    = require('./task-queue');

// ── default config ────────────────────────────────────────────────────────────
const DEFAULT_POLL_MS       = 2_000;   // how often to check for new work
const DISPATCH_TIMEOUT_MS   = 30_000;  // max time to wait for agent ACK
const ASSIGN_TIMEOUT_MS     = 60_000;  // max time for an assigned task before stale-check

/**
 * @typedef {Object} PipelineOptions
 * @property {import('./task-queue').TaskQueue}  [queue]        - inject existing queue
 * @property {Object}                            registry       - agent-registry instance
 * @property {EventEmitter}                      bus            - shared event bus
 * @property {Function}                          dispatcher     - async fn(task, agent) → result
 * @property {number}                            [pollMs]       - polling interval ms
 * @property {Function}                          [jobSource]    - async fn() → raw job[] from Hermes
 */

class HermesPipeline extends EventEmitter {
  /**
   * @param {PipelineOptions} opts
   */
  constructor(opts = {}) {
    super();

    const {
      queue      = new TaskQueue(),
      registry,
      bus,
      dispatcher,
      pollMs     = DEFAULT_POLL_MS,
      jobSource  = null,
    } = opts;

    if (!registry)   throw new Error('HermesPipeline: registry is required');
    if (!bus)        throw new Error('HermesPipeline: bus is required');
    if (!dispatcher) throw new Error('HermesPipeline: dispatcher is required');

    this.queue      = queue;
    this.registry   = registry;
    this.bus        = bus;
    this.dispatcher = dispatcher;
    this.pollMs     = pollMs;
    this.jobSource  = jobSource;

    this._running     = false;
    this._pollTimer   = null;
    this._inFlight    = new Map(); // taskId → { timer, agentId }

    // Forward queue events onto the shared bus
    this._wireQueueEvents();
  }

  // ── lifecycle ───────────────────────────────────────────────────────────────

  start() {
    if (this._running) return this;
    this._running = true;
    this._emit('pipeline:started', { at: new Date().toISOString() });
    this._schedulePoll();
    return this;
  }

  stop() {
    if (!this._running) return this;
    this._running = false;
    if (this._pollTimer) {
      clearTimeout(this._pollTimer);
      this._pollTimer = null;
    }
    // Clear all in-flight dispatch timers
    for (const { timer } of this._inFlight.values()) {
      clearTimeout(timer);
    }
    this._inFlight.clear();
    this._emit('pipeline:stopped', { at: new Date().toISOString() });
    return this;
  }

  // ── public task submission ──────────────────────────────────────────────────

  /**
   * Submit a task directly (bypasses Hermes polling).
   * @param {Object} taskDef – passed to TaskQueue.enqueue
   * @returns {import('./task-queue').Task}
   */
  submit(taskDef) {
    return this.queue.enqueue(taskDef);
  }

  /**
   * Queue snapshot + stats for dashboard.
   */
  status() {
    return {
      running:   this._running,
      stats:     this.queue.stats(),
      inFlight:  this._inFlight.size,
      snapshot:  this.queue.snapshot(),
    };
  }

  // ── core loop ───────────────────────────────────────────────────────────────

  _schedulePoll() {
    if (!this._running) return;
    this._pollTimer = setTimeout(() => this._poll(), this.pollMs);
  }

  async _poll() {
    if (!this._running) return;

    try {
      // 1. Pull in any new jobs from external Hermes source
      if (typeof this.jobSource === 'function') {
        await this._ingestExternalJobs();
      }

      // 2. Dispatch all ready pending tasks
      let task;
      while ((task = this.queue.dequeue()) !== null) {
        // Don't dispatch the same task twice if already in-flight
        if (this._inFlight.has(task.id)) break;
        await this._dispatch(task);
      }

      const stats = this.queue.stats();
      this._emit('pipeline:poll', {
        pendingCount:  stats.pending,
        assignedCount: stats.assigned,
        deadCount:     stats.dead,
        inFlight:      this._inFlight.size,
      });

    } catch (err) {
      this._emit('pipeline:error', { error: err.message, stack: err.stack });
    }

    this._schedulePoll();
  }

  async _ingestExternalJobs() {
    try {
      const jobs = await this.jobSource();
      if (!Array.isArray(jobs)) return;
      for (const job of jobs) {
        this.queue.enqueue({
          type:     job.type    || 'hermes-job',
          payload:  job.payload || job,
          priority: job.priority || 0,
          meta:     { source: 'hermes', externalId: job.id },
        });
      }
    } catch (err) {
      this._emit('pipeline:error', {
        error: `jobSource ingestion failed: ${err.message}`,
      });
    }
  }

  async _dispatch(task) {
    // Select a capable, healthy agent
    const agent = this._selectAgent(task);

    if (!agent) {
      this._emit('pipeline:no-agents', { task });
      // Don't consume the task — leave it pending for next poll
      return;
    }

    // Mark assigned in queue
    try {
      this.queue.assign(task.id, agent.id);
    } catch (err) {
      // Race condition: task was already picked up
      return;
    }

    this._emit('pipeline:task:dispatched', { task, agent });

    // Set a stale-assignment guard timer
    const guardTimer = setTimeout(() => {
      // If still in-flight after ASSIGN_TIMEOUT, fail it
      if (this._inFlight.has(task.id)) {
        this._inFlight.delete(task.id);
        this._handleFailure(task, `assignment timeout after ${ASSIGN_TIMEOUT_MS}ms`);
      }
    }, ASSIGN_TIMEOUT_MS);

    if (guardTimer.unref) guardTimer.unref();
    this._inFlight.set(task.id, { timer: guardTimer, agentId: agent.id });

    // Dispatch — fire and forget (monitored via try/catch)
    try {
      const result = await Promise.race([
        this.dispatcher(task, agent),
        this._timeoutPromise(DISPATCH_TIMEOUT_MS, `dispatcher timeout`),
      ]);

      clearTimeout(guardTimer);
      this._inFlight.delete(task.id);
      this.queue.complete(task.id, result || {});
      this._emit('pipeline:task:completed', { task, result });

    } catch (err) {
      clearTimeout(guardTimer);
      this._inFlight.delete(task.id);
      this._handleFailure(task, err.message || String(err));
    }
  }

  _handleFailure(task, errorMsg) {
    const updatedTask = this.queue.fail(task.id, errorMsg);

    if (updatedTask.status === 'dead') {
      this._emit('pipeline:task:dead', { task: updatedTask });
    } else {
      this._emit('pipeline:task:failed', {
        task:    updatedTask,
        error:   errorMsg,
        attempt: updatedTask.retries,
      });
    }
  }

  // ── agent selection ─────────────────────────────────────────────────────────

  /**
   * Pick the best available agent for the task.
   * Prefers agents whose capabilities include the task type.
   * Falls back to any active agent if no specialist is found.
   */
  _selectAgent(task) {
    let agents;
    try {
      const all = this.registry.list ? this.registry.list() :
                  this.registry.getAll ? this.registry.getAll() : [];
      agents = Array.isArray(all) ? all : [];
    } catch {
      agents = [];
    }

    // Only healthy, active agents
    const healthy = agents.filter(a =>
      a.status === 'active' &&
      !this._agentBusy(a.id)
    );

    if (!healthy.length) return null;

    // Prefer agents with matching capability
    const specialist = healthy.find(a =>
      Array.isArray(a.capabilities) &&
      a.capabilities.some(c =>
        c === task.type ||
        c === task.payload?.action ||
        c === task.meta?.jobType
      )
    );

    return specialist || healthy[0];
  }

  /** True if the agent already has an in-flight task assigned to it. */
  _agentBusy(agentId) {
    for (const { agentId: aid } of this._inFlight.values()) {
      if (aid === agentId) return true;
    }
    return false;
  }

  // ── helpers ─────────────────────────────────────────────────────────────────

  _timeoutPromise(ms, msg) {
    return new Promise((_, reject) =>
      setTimeout(() => reject(new Error(msg)), ms).unref?.() ||
      setTimeout(() => reject(new Error(msg)), ms)
    );
  }

  _emit(event, data) {
    const payload = { event, ...data, ts: new Date().toISOString() };
    // Emit on self (for direct listeners)
    this.emit(event, payload);
    // Propagate to shared bus
    try { this.bus.emit(event, payload); } catch { /* bus may not be available */ }
  }

  _wireQueueEvents() {
    const forward = (queueEvent, busEvent) => {
      this.queue.on(queueEvent, data =>
        this._emit(busEvent || queueEvent, { task: data })
      );
    };

    forward('task:enqueued',        'queue:task:enqueued');
    forward('task:retry-scheduled', 'queue:task:retry-scheduled');
    forward('task:retry-ready',     'queue:task:retry-ready');
    forward('task:dead',            'queue:task:dead');
  }
}

module.exports = { HermesPipeline, DEFAULT_POLL_MS };
