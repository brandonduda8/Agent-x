/**
 * agent-x-core/pipeline/ws-status-server.js
 *
 * WebSocket server at path /ws/agent-status
 * ──────────────────────────────────────────
 * • Attaches to an existing http.Server (created by Express)
 * • Uses the native `ws` package (already a common dep) or falls back to
 *   a polling-SSE emitter if ws is unavailable
 * • Broadcasts real-time pipeline + registry status events to all connected
 *   operator dashboard clients
 * • Supports client-side commands:
 *     { cmd: "ping" }         → { type: "pong" }
 *     { cmd: "snapshot" }     → full queue + registry snapshot
 *     { cmd: "submit", task } → enqueue a task from dashboard
 *
 * Message envelope (server → client):
 * {
 *   type:    "event" | "snapshot" | "pong" | "error",
 *   event:   "<event name>",       // for type=event
 *   data:    { … },
 *   ts:      "ISO8601"
 * }
 */

'use strict';

const WS_PATH = '/ws/agent-status';

// ── ws package detection ──────────────────────────────────────────────────────
let WebSocketServer = null;
try {
  const ws = require('ws');
  WebSocketServer = ws.WebSocketServer || ws.Server;
} catch {
  console.warn('[ws-status] `ws` package not found — WebSocket endpoint disabled.');
  console.warn('[ws-status] Install with:  npm install ws');
}

// ─────────────────────────────────────────────────────────────────────────────

const HEARTBEAT_MS = 15_000;  // ping/pong liveness interval
const MAX_HISTORY  = 200;      // event history kept in memory for late-joiners

/**
 * @typedef {Object} WsStatusOptions
 * @property {import('http').Server}          httpServer
 * @property {import('events').EventEmitter}  bus           – shared event bus
 * @property {import('./hermes-pipeline').HermesPipeline} pipeline
 * @property {Object}                         [registry]    – agent registry
 */

class WsStatusServer {
  /**
   * @param {WsStatusOptions} opts
   */
  constructor({ httpServer, bus, pipeline, registry = null }) {
    this.bus      = bus;
    this.pipeline = pipeline;
    this.registry = registry;

    /** @type {import('ws').WebSocket[]} */
    this._clients  = [];

    /** @type {Array<{type,event,data,ts}>} */
    this._history  = [];

    this._wss = null;

    if (!WebSocketServer) return;

    this._wss = new WebSocketServer({ server: httpServer, path: WS_PATH });
    this._wss.on('connection', (ws, req) => this._onConnect(ws, req));
    this._wss.on('error', err => console.error('[ws-status] WSS error:', err.message));

    // Heartbeat sweep
    this._hbInterval = setInterval(() => this._heartbeat(), HEARTBEAT_MS);
    if (this._hbInterval.unref) this._hbInterval.unref();

    // Tap the shared event bus
    this._subscribeToBus();

    console.log(`[ws-status] WebSocket server listening at ${WS_PATH}`);
  }

  // ── connection handling ────────────────────────────────────────────────────

  _onConnect(ws, req) {
    ws.isAlive = true;
    ws.on('pong', () => { ws.isAlive = true; });
    ws.on('close', () => {
      this._clients = this._clients.filter(c => c !== ws);
    });
    ws.on('error', err => {
      console.warn('[ws-status] client error:', err.message);
    });
    ws.on('message', raw => this._handleMessage(ws, raw));

    this._clients.push(ws);

    // Send snapshot immediately upon connection
    this._sendSnapshot(ws);

    // Replay recent event history
    for (const msg of this._history.slice(-50)) {
      this._send(ws, msg);
    }
  }

  // ── inbound commands ───────────────────────────────────────────────────────

  _handleMessage(ws, raw) {
    let msg;
    try {
      msg = JSON.parse(raw.toString());
    } catch {
      this._send(ws, { type: 'error', data: { message: 'invalid JSON' } });
      return;
    }

    switch (msg.cmd) {
      case 'ping':
        this._send(ws, { type: 'pong', ts: new Date().toISOString() });
        break;

      case 'snapshot':
        this._sendSnapshot(ws);
        break;

      case 'submit':
        try {
          if (!msg.task?.type) throw new Error('task.type is required');
          const task = this.pipeline.submit(msg.task);
          this._send(ws, { type: 'ack', data: { taskId: task.id } });
        } catch (err) {
          this._send(ws, { type: 'error', data: { message: err.message } });
        }
        break;

      default:
        this._send(ws, { type: 'error', data: { message: `unknown cmd: ${msg.cmd}` } });
    }
  }

  // ── snapshot ───────────────────────────────────────────────────────────────

  _sendSnapshot(ws) {
    const pipelineStatus = this.pipeline.status();
    let agents = [];
    try {
      agents = this.registry?.list?.() || this.registry?.getAll?.() || [];
    } catch { /* registry may not be ready */ }

    this._send(ws, {
      type:  'snapshot',
      ts:    new Date().toISOString(),
      data: {
        pipeline: pipelineStatus,
        agents:   agents,
      },
    });
  }

  // ── bus subscription ───────────────────────────────────────────────────────

  _subscribeToBus() {
    // All pipeline events forwarded to connected clients
    const PIPELINE_EVENTS = [
      'pipeline:started',
      'pipeline:stopped',
      'pipeline:poll',
      'pipeline:task:dispatched',
      'pipeline:task:completed',
      'pipeline:task:failed',
      'pipeline:task:dead',
      'pipeline:no-agents',
      'pipeline:error',
      'queue:task:enqueued',
      'queue:task:retry-scheduled',
      'queue:task:retry-ready',
      'queue:task:dead',
    ];

    // Registry events
    const REGISTRY_EVENTS = [
      'agent:registered',
      'agent:deregistered',
      'agent:heartbeat',
      'agent:stale',
      'agent:dead',
    ];

    const handler = (eventName) => (data) => {
      this._broadcast(eventName, data);
    };

    for (const ev of [...PIPELINE_EVENTS, ...REGISTRY_EVENTS]) {
      this.bus.on(ev, handler(ev));
    }
  }

  // ── broadcast helpers ──────────────────────────────────────────────────────

  _broadcast(eventName, data) {
    const msg = {
      type:  'event',
      event: eventName,
      data:  data || {},
      ts:    new Date().toISOString(),
    };

    // Store in history ring
    this._history.push(msg);
    if (this._history.length > MAX_HISTORY) this._history.shift();

    for (const ws of this._clients) {
      if (ws.readyState === 1 /* OPEN */) {
        this._send(ws, msg);
      }
    }
  }

  _send(ws, payload) {
    if (ws.readyState !== 1) return;
    try {
      ws.send(JSON.stringify(payload));
    } catch (err) {
      console.warn('[ws-status] send error:', err.message);
    }
  }

  // ── heartbeat ──────────────────────────────────────────────────────────────

  _heartbeat() {
    const dead = [];
    for (const ws of this._clients) {
      if (!ws.isAlive) {
        dead.push(ws);
        continue;
      }
      ws.isAlive = false;
      try { ws.ping(); } catch { /* ignore */ }
    }
    for (const ws of dead) {
      try { ws.terminate(); } catch { /* ignore */ }
      this._clients = this._clients.filter(c => c !== ws);
    }
  }

  // ── accessors ──────────────────────────────────────────────────────────────

  get path()        { return WS_PATH; }
  get clientCount() { return this._clients.length; }
  get available()   { return this._wss !== null; }

  close() {
    if (this._hbInterval) clearInterval(this._hbInterval);
    if (this._wss) this._wss.close();
  }
}

module.exports = { WsStatusServer, WS_PATH };
