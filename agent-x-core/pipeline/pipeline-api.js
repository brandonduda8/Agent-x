/**
 * agent-x-core/pipeline/pipeline-api.js
 *
 * Express router — mounts at /pipeline
 *
 * REST Endpoints:
 *
 *   GET  /pipeline/status        → pipeline running state + queue stats
 *   GET  /pipeline/tasks         → full active + dead-letter task list
 *   GET  /pipeline/tasks/:id     → single task by id
 *   POST /pipeline/tasks         → submit a new task
 *   POST /pipeline/start         → start the pipeline
 *   POST /pipeline/stop          → stop the pipeline
 *   GET  /pipeline/ws-info       → WebSocket endpoint metadata
 */

'use strict';

const { Router } = require('express');

/**
 * @param {import('./hermes-pipeline').HermesPipeline} pipeline
 * @param {import('./ws-status-server').WsStatusServer} wsServer
 * @returns {Router}
 */
function createPipelineRouter(pipeline, wsServer) {
  const router = Router();

  // ── GET /pipeline/status ────────────────────────────────────────────────────
  router.get('/status', (req, res) => {
    res.json({
      ok:        true,
      pipeline:  pipeline.status(),
      ws: {
        path:        wsServer?.path      ?? null,
        available:   wsServer?.available ?? false,
        clients:     wsServer?.clientCount ?? 0,
      },
    });
  });

  // ── GET /pipeline/tasks ─────────────────────────────────────────────────────
  router.get('/tasks', (req, res) => {
    const { active, dead } = pipeline.queue.snapshot();
    const { status, type } = req.query;

    const filterFn = (task) => {
      if (status && task.status !== status) return false;
      if (type   && task.type   !== type)   return false;
      return true;
    };

    res.json({
      ok:     true,
      stats:  pipeline.queue.stats(),
      active: active.filter(filterFn),
      dead:   dead.filter(filterFn),
    });
  });

  // ── GET /pipeline/tasks/:id ─────────────────────────────────────────────────
  router.get('/tasks/:id', (req, res) => {
    try {
      const task = pipeline.queue.get(req.params.id);
      res.json({ ok: true, task });
    } catch (err) {
      res.status(404).json({ ok: false, error: err.message });
    }
  });

  // ── POST /pipeline/tasks ────────────────────────────────────────────────────
  router.post('/tasks', (req, res) => {
    const { type, payload, priority, maxRetries, meta } = req.body || {};

    if (!type) {
      return res.status(400).json({ ok: false, error: 'type is required' });
    }

    try {
      const task = pipeline.submit({
        type,
        payload:    payload    ?? {},
        priority:   typeof priority    === 'number' ? priority    : 0,
        maxRetries: typeof maxRetries  === 'number' ? maxRetries  : undefined,
        meta:       meta       ?? {},
      });

      res.status(201).json({ ok: true, task });
    } catch (err) {
      res.status(500).json({ ok: false, error: err.message });
    }
  });

  // ── POST /pipeline/start ────────────────────────────────────────────────────
  router.post('/start', (req, res) => {
    pipeline.start();
    res.json({ ok: true, message: 'Pipeline started' });
  });

  // ── POST /pipeline/stop ─────────────────────────────────────────────────────
  router.post('/stop', (req, res) => {
    pipeline.stop();
    res.json({ ok: true, message: 'Pipeline stopped' });
  });

  // ── GET /pipeline/ws-info ───────────────────────────────────────────────────
  router.get('/ws-info', (req, res) => {
    res.json({
      ok:        true,
      wsPath:    wsServer?.path    ?? '/ws/agent-status',
      available: wsServer?.available ?? false,
      note:      'Connect via WebSocket. Send { cmd:"snapshot" } for full state.',
    });
  });

  return router;
}

module.exports = { createPipelineRouter };
