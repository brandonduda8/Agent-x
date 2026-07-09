/**
 * Zangi API Routes — /api/zangi
 *
 * Mounted on the agent-x-core Express app (Port 3000).
 *
 * Endpoints
 * ---------
 * POST /api/zangi/send
 *   Send a message to a specific agent or broadcast to all agents.
 *
 * POST /api/zangi/broadcast
 *   Shorthand broadcast to the shared group channel.
 *
 * POST /api/zangi/webhook
 *   Inbound webhook endpoint called by Zangi — routes messages to agents.
 *
 * GET  /api/zangi/agents
 *   List all Zangi ↔ Agent X mappings.
 *
 * GET  /api/zangi/agents/:agentId
 *   Get the Zangi mapping for a specific agent.
 *
 * POST /api/zangi/agents
 *   Add or update a Zangi ↔ Agent X mapping.
 *
 * DELETE /api/zangi/agents/:agentId
 *   Remove a mapping.
 *
 * POST /api/zangi/webhook/register
 *   Register this server's webhook URL with Zangi.
 *
 * GET  /api/zangi/webhooks
 *   List registered Zangi webhooks.
 */

'use strict';

const express = require('express');
const router = express.Router();

const { ZangiClient, MESSAGE_TYPES } = require('../../communication/zangi-client');
const agentMap = require('../../communication/zangi-agent-map');
const {
  zangiWebhookMiddleware,
  registerAgentHandler,
  unregisterAgentHandler,
} = require('../../communication/zangi-webhook-handler');

// ---------------------------------------------------------------------------
// Lazy singleton Zangi client
// ---------------------------------------------------------------------------

let _client = null;

function getClient() {
  if (!_client) {
    _client = new ZangiClient();
  }
  return _client;
}

// ---------------------------------------------------------------------------
// Middleware: capture raw body for HMAC verification on webhook endpoint.
// We store it on req.rawBody before JSON parsing.
// ---------------------------------------------------------------------------

function rawBodyCapture(req, res, next) {
  const chunks = [];
  req.on('data', (chunk) => chunks.push(chunk));
  req.on('end', () => {
    req.rawBody = Buffer.concat(chunks).toString('utf8');
    try {
      req.body = JSON.parse(req.rawBody);
    } catch {
      req.body = {};
    }
    next();
  });
  req.on('error', next);
}

// ---------------------------------------------------------------------------
// Validation helpers
// ---------------------------------------------------------------------------

/**
 * Assert required fields are present; send 400 on failure.
 * @param {object} body
 * @param {string[]} fields
 * @param {object} res
 * @returns {boolean}  true if valid
 */
function requireFields(body, fields, res) {
  const missing = fields.filter((f) => body[f] === undefined || body[f] === null || body[f] === '');
  if (missing.length > 0) {
    res.status(400).json({ error: `Missing required fields: ${missing.join(', ')}` });
    return false;
  }
  return true;
}

// ---------------------------------------------------------------------------
// POST /api/zangi/send
// ---------------------------------------------------------------------------

/**
 * Send a message to a specific agent (by agentId or agentName) or to a
 * raw Zangi user / channel ID.
 *
 * Body:
 * {
 *   "agentId"       : "content-generator",   // resolve from map (preferred)
 *   "zangiUserId"   : "zangi-uid-xxx",        // override: send to raw user
 *   "zangiChannelId": "zangi-chan-xxx",        // override: send to raw channel
 *   "message"       : "Hello agent!",
 *   "type"          : "text",                 // default: "text"
 *   "metadata"      : {}                      // optional extra metadata
 * }
 */
router.post('/send', async (req, res) => {
  const { agentId, zangiUserId, zangiChannelId, message, type, metadata } = req.body || {};

  if (!message) {
    return res.status(400).json({ error: 'message is required' });
  }

  const client = getClient();
  const msgType = type || MESSAGE_TYPES.TEXT;

  try {
    // ------------------------------------------------------------------
    // Case 1: Resolve agent from the map
    // ------------------------------------------------------------------
    if (agentId) {
      const entry = agentMap.resolve(agentId);
      if (!entry) {
        return res.status(404).json({ error: `No Zangi mapping found for agent: ${agentId}` });
      }

      if (!entry.active) {
        return res.status(409).json({ error: `Agent "${agentId}" is mapped but inactive` });
      }

      let result;

      // Prefer channel over user (channels are per-agent private rooms)
      if (entry.zangiChannelId) {
        result = await client.sendChannelMessage({
          channelId: entry.zangiChannelId,
          text: message,
          type: msgType,
          metadata: { agentId: entry.agentId, agentName: entry.agentName, ...(metadata || {}) },
        });
      } else if (entry.zangiUserId) {
        result = await client.sendDirectMessage({
          toUserId: entry.zangiUserId,
          text: message,
          type: msgType,
          metadata: { agentId: entry.agentId, agentName: entry.agentName, ...(metadata || {}) },
        });
      } else {
        return res.status(422).json({
          error: `Agent "${agentId}" has no zangiUserId or zangiChannelId configured`,
        });
      }

      return res.json({
        ok: true,
        agent: entry.agentName || entry.agentId,
        zangiResponse: result,
      });
    }

    // ------------------------------------------------------------------
    // Case 2: Raw zangiChannelId provided
    // ------------------------------------------------------------------
    if (zangiChannelId) {
      const result = await client.sendChannelMessage({
        channelId: zangiChannelId,
        text: message,
        type: msgType,
        metadata: metadata || {},
      });
      return res.json({ ok: true, zangiChannelId, zangiResponse: result });
    }

    // ------------------------------------------------------------------
    // Case 3: Raw zangiUserId provided
    // ------------------------------------------------------------------
    if (zangiUserId) {
      const result = await client.sendDirectMessage({
        toUserId: zangiUserId,
        text: message,
        type: msgType,
        metadata: metadata || {},
      });
      return res.json({ ok: true, zangiUserId, zangiResponse: result });
    }

    return res.status(400).json({
      error: 'Provide one of: agentId, zangiUserId, or zangiChannelId',
    });
  } catch (err) {
    console.error('[Zangi /send] Error:', err.message);
    const status = err.status || 500;
    return res.status(status).json({ error: err.message, details: err.response });
  }
});

// ---------------------------------------------------------------------------
// POST /api/zangi/broadcast
// ---------------------------------------------------------------------------

/**
 * Broadcast a message to the shared Zangi group channel.
 *
 * Body:
 * {
 *   "message"           : "System-wide announcement",
 *   "broadcastChannelId": "zangi-chan-broadcast",  // optional override
 *   "metadata"          : {}
 * }
 */
router.post('/broadcast', async (req, res) => {
  const { message, broadcastChannelId, metadata } = req.body || {};

  if (!requireFields(req.body || {}, ['message'], res)) return;

  try {
    const client = getClient();
    const result = await client.broadcast({
      text: message,
      broadcastChannelId,
      metadata: metadata || {},
    });

    return res.json({ ok: true, broadcast: true, zangiResponse: result });
  } catch (err) {
    console.error('[Zangi /broadcast] Error:', err.message);
    return res.status(err.status || 500).json({ error: err.message, details: err.response });
  }
});

// ---------------------------------------------------------------------------
// POST /api/zangi/webhook  (inbound from Zangi)
// ---------------------------------------------------------------------------

// Use the raw body capture + Zangi webhook middleware
router.post(
  '/webhook',
  rawBodyCapture,
  zangiWebhookMiddleware({ requireSignature: false })
);

// ---------------------------------------------------------------------------
// GET  /api/zangi/agents
// ---------------------------------------------------------------------------

router.get('/agents', (req, res) => {
  const includeInactive = req.query.includeInactive === 'true';
  const agents = agentMap.listAll({ includeInactive });
  return res.json({ agents, count: agents.length });
});

// ---------------------------------------------------------------------------
// GET  /api/zangi/agents/:agentId
// ---------------------------------------------------------------------------

router.get('/agents/:agentId', (req, res) => {
  const entry = agentMap.resolve(req.params.agentId);
  if (!entry) {
    return res.status(404).json({ error: `No mapping for agent: ${req.params.agentId}` });
  }
  return res.json(entry);
});

// ---------------------------------------------------------------------------
// POST /api/zangi/agents  (add / update mapping)
// ---------------------------------------------------------------------------

/**
 * Body:
 * {
 *   "agentId"        : "my-custom-agent",
 *   "agentName"      : "My Custom Agent",
 *   "zangiUserId"    : "zangi-uid-xxx",
 *   "zangiChannelId" : "zangi-chan-xxx",
 *   "capabilities"   : ["custom"],
 *   "active"         : true
 * }
 */
router.post('/agents', (req, res) => {
  if (!requireFields(req.body || {}, ['agentId'], res)) return;

  try {
    const entry = agentMap.upsert(req.body);
    return res.status(201).json({ ok: true, entry });
  } catch (err) {
    return res.status(400).json({ error: err.message });
  }
});

// ---------------------------------------------------------------------------
// DELETE /api/zangi/agents/:agentId
// ---------------------------------------------------------------------------

router.delete('/agents/:agentId', (req, res) => {
  const removed = agentMap.remove(req.params.agentId);
  if (!removed) {
    return res.status(404).json({ error: `No mapping for agent: ${req.params.agentId}` });
  }
  return res.json({ ok: true, removed: req.params.agentId });
});

// ---------------------------------------------------------------------------
// POST /api/zangi/webhook/register
// ---------------------------------------------------------------------------

/**
 * Register this server's webhook URL with Zangi.
 *
 * Body:
 * {
 *   "webhookUrl": "https://your-server.example.com/api/zangi/webhook",
 *   "events"    : ["message.received"]   // optional, defaults to all
 * }
 */
router.post('/webhook/register', async (req, res) => {
  if (!requireFields(req.body || {}, ['webhookUrl'], res)) return;

  try {
    const client = getClient();
    const result = await client.registerWebhook({
      webhookUrl: req.body.webhookUrl,
      events: req.body.events,
    });
    return res.json({ ok: true, zangiResponse: result });
  } catch (err) {
    console.error('[Zangi /webhook/register] Error:', err.message);
    return res.status(err.status || 500).json({ error: err.message, details: err.response });
  }
});

// ---------------------------------------------------------------------------
// GET /api/zangi/webhooks
// ---------------------------------------------------------------------------

router.get('/webhooks', async (req, res) => {
  try {
    const client = getClient();
    const result = await client.listWebhooks();
    return res.json({ webhooks: result });
  } catch (err) {
    console.error('[Zangi /webhooks] Error:', err.message);
    return res.status(err.status || 500).json({ error: err.message });
  }
});

// ---------------------------------------------------------------------------
// Handler registration exports (so orchestrator can wire up agents)
// ---------------------------------------------------------------------------

module.exports = router;
module.exports.registerAgentHandler = registerAgentHandler;
module.exports.unregisterAgentHandler = unregisterAgentHandler;
