/**
 * Zangi Webhook Listener — Standalone Server
 *
 * A lightweight standalone Express server that listens exclusively for inbound
 * Zangi webhook events and routes them to Agent X agent processes.
 *
 * This service can be run independently alongside agent-x-core when you need
 * to expose a separate public endpoint for Zangi callbacks (e.g. different
 * port, different reverse-proxy rule, or running on a separate host).
 *
 * Port:  ZANGI_LISTENER_PORT (default: 3002)
 *
 * Environment variables:
 *   ZANGI_API_KEY            – Zangi API key
 *   ZANGI_API_SECRET         – Zangi API secret
 *   ZANGI_APP_ID             – Zangi application ID
 *   ZANGI_BASE_URL           – Zangi REST API base URL
 *   ZANGI_WEBHOOK_SECRET     – HMAC secret for signature verification
 *   ZANGI_BROADCAST_CHANNEL_ID – Shared group channel ID
 *   ZANGI_LISTENER_PORT      – Port to listen on (default: 3002)
 *   ZANGI_MAP_FILE           – Path to zangi-agent-map.json
 *   AGENT_X_CORE_URL         – Internal URL of agent-x-core (default: http://localhost:3000)
 *
 * Usage:
 *   node webhook-listener/zangi-listener.js
 */

'use strict';

const express = require('express');
const http = require('http');
const { URL } = require('url');
const path = require('path');

// ---------------------------------------------------------------------------
// Imports
// ---------------------------------------------------------------------------

const {
  zangiWebhookMiddleware,
  processEvent,
  registerAgentHandler,
} = require('../communication/zangi-webhook-handler');

const agentMap = require('../communication/zangi-agent-map');
const { ZangiClient } = require('../communication/zangi-client');

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

const PORT = parseInt(process.env.ZANGI_LISTENER_PORT || '3002', 10);
const AGENT_X_CORE_URL = (process.env.AGENT_X_CORE_URL || 'http://localhost:3000').replace(/\/$/, '');

// ---------------------------------------------------------------------------
// Forward-to-core helper
// ---------------------------------------------------------------------------

/**
 * Forward an Agent X task packet to agent-x-core via its internal task API.
 * This bridges the standalone listener into the main orchestration layer.
 *
 * @param {object} task  Agent X task packet
 * @returns {Promise<void>}
 */
async function forwardTaskToCore(task) {
  const url = `${AGENT_X_CORE_URL}/v1/tasks`;
  const payload = JSON.stringify(task);

  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const options = {
      hostname: parsed.hostname,
      port: parsed.port || 3000,
      path: parsed.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload),
        'X-Internal-Source': 'zangi-listener',
      },
    };

    const req = http.request(options, (res) => {
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => {
        const body = Buffer.concat(chunks).toString('utf8');
        if (res.statusCode >= 200 && res.statusCode < 300) {
          console.info(`[ZangiListener] Forwarded task ${task.id} to core → ${res.statusCode}`);
          resolve();
        } else {
          console.warn(`[ZangiListener] Core returned ${res.statusCode} for task ${task.id}: ${body}`);
          resolve(); // Don't reject — task was received, just note the core issue
        }
      });
    });

    req.setTimeout(8000, () => {
      req.destroy();
      console.error(`[ZangiListener] Timeout forwarding task ${task.id} to core`);
      reject(new Error('Timeout forwarding to core'));
    });

    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

// ---------------------------------------------------------------------------
// Register forwarding handlers for every mapped agent
// ---------------------------------------------------------------------------

/**
 * Wire up in-process handlers that forward tasks to agent-x-core.
 * Called once at startup; also re-called after agentMap.reload().
 */
function wireForwardingHandlers() {
  const agents = agentMap.listAll({ includeInactive: true });
  for (const entry of agents) {
    registerAgentHandler(entry.agentId, async (task) => {
      try {
        await forwardTaskToCore(task);
      } catch (err) {
        console.error(
          `[ZangiListener] Failed to forward task for agent ${entry.agentName}: ${err.message}`
        );
      }
    });

    if (entry.agentName && entry.agentName !== entry.agentId) {
      registerAgentHandler(entry.agentName, async (task) => {
        try {
          await forwardTaskToCore(task);
        } catch (err) {
          console.error(
            `[ZangiListener] Failed to forward task for agent ${entry.agentName}: ${err.message}`
          );
        }
      });
    }
  }
  console.info(`[ZangiListener] Wired forwarding handlers for ${agents.length} agent(s)`);
}

// ---------------------------------------------------------------------------
// Raw body capture middleware
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
// Express app
// ---------------------------------------------------------------------------

const app = express();

// Health check
app.get('/health', (req, res) => {
  res.json({
    service: 'zangi-listener',
    status: 'ok',
    port: PORT,
    agentsCounted: agentMap.listAll().length,
    uptime: process.uptime(),
  });
});

// Agent map endpoint (read-only view)
app.get('/agents', (req, res) => {
  const includeInactive = req.query.includeInactive === 'true';
  res.json({ agents: agentMap.listAll({ includeInactive }) });
});

// Reload agent map from disk
app.post('/agents/reload', express.json(), (req, res) => {
  agentMap.reload();
  wireForwardingHandlers();
  res.json({ ok: true, agents: agentMap.listAll().length });
});

// ---------------------------------------------------------------------------
// Primary webhook endpoint — Zangi will POST here
// ---------------------------------------------------------------------------

app.post(
  '/webhook',
  rawBodyCapture,
  zangiWebhookMiddleware({ requireSignature: false })
);

// Legacy path in case Zangi is configured with /zangi/webhook
app.post(
  '/zangi/webhook',
  rawBodyCapture,
  zangiWebhookMiddleware({ requireSignature: false })
);

// ---------------------------------------------------------------------------
// 404 handler
// ---------------------------------------------------------------------------

app.use((req, res) => {
  res.status(404).json({ error: 'Not found', path: req.path });
});

// ---------------------------------------------------------------------------
// Error handler
// ---------------------------------------------------------------------------

app.use((err, req, res, next) => {
  console.error('[ZangiListener] Unhandled error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------

function start() {
  wireForwardingHandlers();

  const server = app.listen(PORT, () => {
    console.info(`[ZangiListener] ✓ Zangi Webhook Listener running on port ${PORT}`);
    console.info(`[ZangiListener]   Webhook endpoint:  http://0.0.0.0:${PORT}/webhook`);
    console.info(`[ZangiListener]   Health:            http://0.0.0.0:${PORT}/health`);
    console.info(`[ZangiListener]   Forwarding tasks → ${AGENT_X_CORE_URL}`);
  });

  // Graceful shutdown
  process.on('SIGTERM', () => {
    console.info('[ZangiListener] SIGTERM received — shutting down gracefully');
    server.close(() => process.exit(0));
  });

  process.on('SIGINT', () => {
    console.info('[ZangiListener] SIGINT received — shutting down gracefully');
    server.close(() => process.exit(0));
  });

  return server;
}

// ---------------------------------------------------------------------------
// Run if invoked directly
// ---------------------------------------------------------------------------

if (require.main === module) {
  start();
}

module.exports = { app, start, wireForwardingHandlers, forwardTaskToCore };
