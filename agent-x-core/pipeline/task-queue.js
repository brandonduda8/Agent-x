/**
 * agent-x-core/pipeline/task-queue.js
 *
 * In-memory task queue with:
 *  - Priority ordering (higher priority dequeued first)
 *  - Per-task retry tracking (max 3 retries)
 *  - Exponential backoff scheduling (1s, 2s, 4s … capped at 60 s)
 *  - Dead-letter store for permanently failed tasks
 *  - EventEmitter interface so pipeline can react to state changes
 *
 * States:
 *   pending  → assigned → completed
 *                       ↘ failed  → (retry → pending) | dead
 */

'use strict';

const { EventEmitter } = require('events');
const { v4: uuidv4 }   = require('uuid');

// ─── constants ────────────────────────────────────────────────────────────────
const MAX_RETRIES      = 3;
const BASE_BACKOFF_MS  = 1_000;  // 1 s
const MAX_BACKOFF_MS   = 60_000; // 60 s cap

// ─── helpers ──────────────────────────────────────────────────────────────────
function backoffMs(attempt) {
  const raw = BASE_BACKOFF_MS * (2 ** attempt);
  return Math.min(raw, MAX_BACKOFF_MS);
}

/**
 * @typedef {Object} Task
 * @property {string}   id
 * @property {string}   type
 * @property {Object}   payload
 * @property {number}   priority      – higher = dequeued first
 * @property {string}   status        – pending | assigned | completed | failed | dead
 * @property {number}   retries
 * @property {number}   maxRetries
 * @property {string|null} assignedTo – agent id
 * @property {string}   createdAt
 * @property {string|null} assignedAt
 * @property {string|null} completedAt
 * @property {string|null} failedAt
 * @property {string|null} nextRetryAt
 * @property {string|null} errorMsg
 * @property {Object}   meta
 */

class TaskQueue extends EventEmitter {
  constructor() {
    super();

    /** @type {Map<string, Task>} */
    this._tasks = new Map();

    /** @type {Task[]} dead-letter store */
    this._deadLetter = [];

    // Periodic sweep: move back-off tasks back to pending when their timer fires
    this._sweepInterval = setInterval(() => this._sweepBackoff(), 500);
    this._sweepInterval.unref?.(); // don't block process exit
  }

  // ── public API ─────────────────────────────────────────────────────────────

  /**
   * Enqueue a new task.
   * @param {Object} opts
   * @param {string}  opts.type
   * @param {Object}  [opts.payload={}]
   * @param {number}  [opts.priority=0]
   * @param {number}  [opts.maxRetries=MAX_RETRIES]
   * @param {Object}  [opts.meta={}]
   * @returns {Task}
   */
  enqueue({ type, payload = {}, priority = 0, maxRetries = MAX_RETRIES, meta = {} }) {
    if (!type) throw new Error('Task type is required');

    const task = {
      id:          uuidv4(),
      type,
      payload,
      priority,
      status:      'pending',
      retries:     0,
      maxRetries,
      assignedTo:  null,
      createdAt:   new Date().toISOString(),
      assignedAt:  null,
      completedAt: null,
      failedAt:    null,
      nextRetryAt: null,
      errorMsg:    null,
      meta,
    };

    this._tasks.set(task.id, task);
    this.emit('task:enqueued', task);
    return task;
  }

  /**
   * Dequeue the highest-priority pending task.
   * Returns null if nothing is ready.
   * @returns {Task|null}
   */
  dequeue() {
    const pending = this._pendingSorted();
    if (!pending.length) return null;
    return pending[0]; // highest priority, ready now
  }

  /**
   * Assign a pending task to an agent.
   * @param {string} taskId
   * @param {string} agentId
   * @returns {Task}
   */
  assign(taskId, agentId) {
    const task = this._get(taskId);
    if (task.status !== 'pending') {
      throw new Error(`Cannot assign task ${taskId} in state '${task.status}'`);
    }
    task.status     = 'assigned';
    task.assignedTo = agentId;
    task.assignedAt = new Date().toISOString();
    this.emit('task:assigned', task);
    return task;
  }

  /**
   * Mark a task as completed.
   * @param {string} taskId
   * @param {Object} [result={}]
   * @returns {Task}
   */
  complete(taskId, result = {}) {
    const task = this._get(taskId);
    task.status      = 'completed';
    task.completedAt = new Date().toISOString();
    task.meta.result = result;
    this.emit('task:completed', task);
    return task;
  }

  /**
   * Mark a task as failed.
   * Schedules retry with exponential backoff if retries remain,
   * otherwise moves to dead-letter.
   * @param {string} taskId
   * @param {string} [errorMsg='unknown error']
   * @returns {Task}
   */
  fail(taskId, errorMsg = 'unknown error') {
    const task = this._get(taskId);
    task.failedAt  = new Date().toISOString();
    task.errorMsg  = errorMsg;
    task.retries  += 1;

    this.emit('task:failed', { ...task, errorMsg });

    if (task.retries <= task.maxRetries) {
      const delay        = backoffMs(task.retries - 1);
      task.status        = 'pending';           // back to pending after delay
      task.assignedTo    = null;
      task.assignedAt    = null;
      task.nextRetryAt   = new Date(Date.now() + delay).toISOString();
      this.emit('task:retry-scheduled', { task, delay, attempt: task.retries });
    } else {
      task.status = 'dead';
      this._deadLetter.push(task);
      this._tasks.delete(taskId);
      this.emit('task:dead', task);
    }

    return task;
  }

  /**
   * Get a snapshot of all tasks (active map + dead-letter).
   * @returns {{ active: Task[], dead: Task[] }}
   */
  snapshot() {
    return {
      active: Array.from(this._tasks.values()),
      dead:   [...this._deadLetter],
    };
  }

  /**
   * Stats summary.
   * @returns {Object}
   */
  stats() {
    const active = Array.from(this._tasks.values());
    const counts = { pending: 0, assigned: 0, completed: 0, failed_backoff: 0 };
    for (const t of active) {
      if (t.status === 'pending' && t.nextRetryAt) {
        counts.failed_backoff++;
      } else if (t.status === 'pending') {
        counts.pending++;
      } else if (t.status === 'assigned') {
        counts.assigned++;
      } else if (t.status === 'completed') {
        counts.completed++;
      }
    }
    return {
      ...counts,
      dead:  this._deadLetter.length,
      total: active.length + this._deadLetter.length,
    };
  }

  /** Get task by id (throws if missing). */
  get(taskId) { return this._get(taskId); }

  /** Stop the internal sweep timer. */
  destroy() {
    if (this._sweepInterval) clearInterval(this._sweepInterval);
  }

  // ── private ────────────────────────────────────────────────────────────────

  _get(taskId) {
    const t = this._tasks.get(taskId);
    if (!t) throw new Error(`Task not found: ${taskId}`);
    return t;
  }

  /** Return pending tasks whose nextRetryAt has passed, sorted by priority desc. */
  _pendingSorted() {
    const now = Date.now();
    return Array.from(this._tasks.values())
      .filter(t => {
        if (t.status !== 'pending') return false;
        if (t.nextRetryAt && new Date(t.nextRetryAt).getTime() > now) return false;
        return true;
      })
      .sort((a, b) => b.priority - a.priority);
  }

  /** Move back-off tasks to ready-pending when their timer expires. */
  _sweepBackoff() {
    const now = Date.now();
    for (const task of this._tasks.values()) {
      if (
        task.status === 'pending' &&
        task.nextRetryAt &&
        new Date(task.nextRetryAt).getTime() <= now
      ) {
        const was = task.nextRetryAt;
        task.nextRetryAt = null;
        this.emit('task:retry-ready', { task, was });
      }
    }
  }
}

module.exports = { TaskQueue, MAX_RETRIES, backoffMs };
