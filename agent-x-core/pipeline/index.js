/**
 * agent-x-core/pipeline/index.js
 *
 * Single entry-point for the pipeline subsystem.
 *
 * Wires together:
 *   HermesPipeline  ← TaskQueue + agent-dispatcher + registry + bus
 *   WsStatusServer  ← httpServer + bus + pipeline
 *   pipeline-api    ← Express router
 *
 * Usage (from agent-x-core/index.js):
 *
 *   const { mountPipeline } = require('./pipeline');
 *   const { router, wsServer, pipeline } = mountPipeline({
 *     app, httpServer, registry, bus
 *   });
 *   app.use('/pipeline', router);
 */

'use strict';

const { HermesPipeline }     = require('./hermes-pipeline');
const { WsStatusServer }     = require('./ws-status-server');
const { createPipelineRouter } = require('./pipeline-api');
const { dispatch }           = require('./agent-dispatcher');

/**
 * @typedef {Object} MountOptions
 * @property {import('express').Application}  app
 * @property {import('http').Server}          httpServer
 * @property {Object}                         registry   – agent registry instance
 * @property {import('events').EventEmitter}  bus        – shared event bus
 * @property {Function}                       [jobSource] – async fn() → external job[]
 * @property {number}                         [pollMs]   – pipeline poll interval ms
 * @property {boolean}                        [autoStart] – start pipeline immediately (default true)
 */

/**
 * Mount the full pipeline subsystem onto the Express app.
 *
 * @param {MountOptions} opts
 * @returns {{ pipeline: HermesPipeline, wsServer: WsStatusServer, router: import('express').Router }}
 */
function mountPipeline(opts = {}) {
  const {
    app,
    httpServer,
    registry,
    bus,
    jobSource  = null,
    pollMs     = 2_000,
    autoStart  = true,
  } = opts;

  if (!httpServer) throw new Error('mountPipeline: httpServer is required');
  if (!registry)   throw new Error('mountPipeline: registry is required');
  if (!bus)        throw new Error('mountPipeline: bus is required');

  // 1. Build the pipeline
  const pipeline = new HermesPipeline({
    registry,
    bus,
    dispatcher: dispatch,
    pollMs,
    jobSource,
  });

  // 2. Attach the WebSocket status server
  const wsServer = new WsStatusServer({ httpServer, bus, pipeline, registry });

  // 3. Build Express router
  const router = createPipelineRouter(pipeline, wsServer);

  // 4. Optionally auto-start
  if (autoStart) pipeline.start();

  return { pipeline, wsServer, router };
}

module.exports = {
  mountPipeline,
  HermesPipeline,
  WsStatusServer,
  createPipelineRouter,
};
