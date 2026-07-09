/**
 * Zangi Webhook Handler
 *
 * Processes inbound webhook events posted by Zangi and routes them to the
 * correct Agent X agent process.
 *
 * Routing logic:
 *   1. Resolve the source/target from the Zangi event payload.
 *   2. Look up the agent in zangi-agent-map.js.
 *   3. Dispatch a JSON task packet to the agent's stdin (if stdio-based)
 *      or forward via the internal event bus.
 *
 * HMAC verification:
 *   If ZANGI_WEBHOOK_SECRET is set, every inbound request is verified against
 *   the X-Zangi-Signature header using HMAC-SHA256.
 *
 * Supported Zangi event types:
 *   - message.received   → route to target agent or broadcast handler
 *   - message.delivered  → ACK logging
 *   - message.read       → ACK logging
 *   - (unknown)          → logged and ignored
 */

'use strict';

const crypto = require('crypto');
const { resolve: resolveAgent, getByZangiUserId, getByZangiChannelId, listAll } = require('./zangi-agent-map');
const { createTask, STATUS } = require('./packet-schema');

// ---------------------------------------------------------------------------
// HMAC verification
// ---------------------------------------------------------------------------

const WEBHOOK_SECRET = process.env.ZANGI_WEBHOOK_SECRET || '';

/**
 * Verify the HMAC-SHA256 signature on an inbound Zangi webhook request.
 *
 * Zangi is expected to include:
 *   X-Zangi-Signature: sha256=<hex-digest>
 *
 * @param {string|Buffer} rawBody   Raw request body bytes
 * @param {string} signatureHeader  Value of X-Zangi-Signature header
 * @returns {boolean}
 */
function verifySignature(rawBody, signatureHeader) {
  if (!WEBHOOK_SECRET) {
    // Secret not configured — skip verification (development mode)
    console.warn('[ZangiWebhook] ZANGI_WEBHOOK_SECRET not set — skipping HMAC verification');
    return true;
  }

  if (!signatureHeader) return false;

  const [algo, provided] = signatureHeader.split('=');
  if (algo !== 'sha256' || !provided) return false;

  const expected = crypto
    .createHmac('sha256', WEBHOOK_SECRET)
    .update(rawBody)
    .digest('hex');

  // Constant-time comparison
  return crypto.timingSafeEqual(
    Buffer.from(provided, 'hex'),
    Buffer.from(expected, 'hex')
  );
}

// ---------------------------------------------------------------------------
// Agent dispatch
// ---------------------------------------------------------------------------

/**
 * Registry of in-process agent handlers.
 * Key: agentId | agentName
 * Value: (task: object) => Promise<void>
 */
const _handlers = new Map();

/**
 * Register an in-process handler for a named agent.
 * The handler receives a fully-formed Agent X task packet.
 *
 * @param {string} agentIdOrName
 * @param {function} handler  async (task) => void
 */
function registerAgentHandler(agentIdOrName, handler) {
  if (typeof handler !== 'function') throw new Error('handler must be a function');
  _handlers.set(agentIdOrName, handler);
  console.info(`[ZangiWebhook] Registered in-process handler for agent: ${agentIdOrName}`);
}

/**
 * Unregister a previously registered in-process handler.
 * @param {string} agentIdOrName
 */
function unregisterAgentHandler(agentIdOrName) {
  _handlers.delete(agentIdOrName);
}

/**
 * Dispatch a task packet to an agent.
 *
 * Priority order:
 *   1. In-process handler (fastest, registered via registerAgentHandler)
 *   2. External event bus (if hub_bridge is available)
 *   3. Fallback: log to console
 *
 * @param {object} agentEntry   Entry from zangi-agent-map
 * @param {object} task         Agent X task packet (from createTask)
 * @returns {Promise<void>}
 */
async function dispatchToAgent(agentEntry, task) {
  const { agentId, agentName } = agentEntry;

  // 1. In-process handler
  const handler = _handlers.get(agentId) || _handlers.get(agentName);
  if (handler) {
    try {
      await handler(task);
      console.info(`[ZangiWebhook] Dispatched to in-process handler: ${agentName || agentId}`);
      return;
    } catch (err) {
      console.error(`[ZangiWebhook] In-process handler for ${agentName} threw:`, err.message);
    }
  }

  // 2. Event bus (optional — loaded lazily to avoid circular deps)
  try {
    // hub_bridge publishes events that the Node.js orchestrator subscribes to
    const hubBridge = _tryRequire('../core/hub_bridge.js');
    if (hubBridge && typeof hubBridge.publish === 'function') {
      await hubBridge.publish('zangi:inbound', { agentId, agentName, task });
      console.info(`[ZangiWebhook] Published to hub_bridge for agent: ${agentName || agentId}`);
      return;
    }
  } catch (err) {
    console.warn('[ZangiWebhook] hub_bridge unavailable:', err.message);
  }

  // 3. Fallback — at minimum log so nothing is silently dropped
  console.warn(
    `[ZangiWebhook] No handler registered for agent "${agentName || agentId}". ` +
    `Task dropped: ${JSON.stringify(task)}`
  );
}

/**
 * Safe dynamic require that won't crash if the module doesn't exist.
 * @param {string} modulePath
 * @returns {any|null}
 */
function _tryRequire(modulePath) {
  try {
    return require(modulePath);
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// Event handlers
// ---------------------------------------------------------------------------

/**
 * Handle a `message.received` event from Zangi.
 *
 * @param {object} event  Parsed Zangi webhook event
 * @returns {Promise<{dispatched: boolean, agent: string|null, task: object|null}>}
 */
async function handleMessageReceived(event) {
  const { from, to, channelId, message, metadata = {} } = event;

  // ------------------------------------------------------------------
  // Resolve the target agent
  // ------------------------------------------------------------------
  let agentEntry = null;

  // Prefer explicit channelId match (per-agent private channel)
  if (channelId) {
    agentEntry = getByZangiChannelId(channelId);
  }

  // Fall back to the `to` user ID
  if (!agentEntry && to) {
    agentEntry = getByZangiUserId(to);
  }

  // Fall back to metadata hint (agentId or agentName in Zangi message metadata)
  if (!agentEntry && metadata.agentId) {
    agentEntry = resolveAgent(metadata.agentId);
  }
  if (!agentEntry && metadata.agentName) {
    agentEntry = resolveAgent(metadata.agentName);
  }

  if (!agentEntry) {
    console.warn('[ZangiWebhook] message.received: could not resolve target agent.', { from, to, channelId });
    return { dispatched: false, agent: null, task: null };
  }

  // ------------------------------------------------------------------
  // Build task packet
  // ------------------------------------------------------------------
  const messageType = metadata.messageType || 'zangi:message';
  const task = createTask({
    type: messageType,
    payload: {
      source: 'zangi',
      from,
      to,
      channelId: channelId || null,
      message,
      rawEvent: event,
    },
    priority: metadata.priority || 'normal',
  });

  // ------------------------------------------------------------------
  // Dispatch
  // ------------------------------------------------------------------
  await dispatchToAgent(agentEntry, task);

  return { dispatched: true, agent: agentEntry.agentName || agentEntry.agentId, task };
}

/**
 * Handle a broadcast event — deliver to all active agents' shared channel.
 * This is triggered when the target channelId matches the broadcast channel.
 *
 * @param {object} event
 * @returns {Promise<void>}
 */
async function handleBroadcastMessage(event) {
  const agents = listAll({ includeInactive: false });
  console.info(`[ZangiWebhook] Broadcasting inbound message to ${agents.length} active agents`);

  await Promise.allSettled(
    agents.map(async (agentEntry) => {
      const task = createTask({
        type: 'zangi:broadcast',
        payload: {
          source: 'zangi',
          broadcast: true,
          message: event.message,
          rawEvent: event,
        },
        priority: 'normal',
      });
      return dispatchToAgent(agentEntry, task);
    })
  );
}

// ---------------------------------------------------------------------------
// Main entry point — called by the Express route handler
// ---------------------------------------------------------------------------

/**
 * Process a single Zangi webhook event object.
 *
 * @param {object} event  Parsed event from Zangi (already validated)
 * @returns {Promise<object>}  Processing result summary
 */
async function processEvent(event) {
  const { type, channelId } = event;

  // Check if this is a broadcast channel message
  const broadcastChannelId = process.env.ZANGI_BROADCAST_CHANNEL_ID || '';
  if (channelId && broadcastChannelId && channelId === broadcastChannelId) {
    await handleBroadcastMessage(event);
    return { type, handled: true, broadcast: true };
  }

  switch (type) {
    case 'message.received':
      return { type, ...(await handleMessageReceived(event)) };

    case 'message.delivered':
    case 'message.read':
      // Acknowledgement events — log and move on
      console.info(`[ZangiWebhook] ${type} ack for message ${event.messageId || '(unknown)'}`);
      return { type, handled: true };

    default:
      console.warn(`[ZangiWebhook] Unrecognised event type: "${type}". Ignoring.`);
      return { type, handled: false };
  }
}

// ---------------------------------------------------------------------------
// Express middleware factory
// ---------------------------------------------------------------------------

/**
 * Returns an Express request handler that:
 *   1. Reads the raw body for HMAC verification.
 *   2. Validates the Zangi signature.
 *   3. Parses and processes each event.
 *   4. Responds 200 OK quickly (Zangi expects fast ACK).
 *
 * Mount this as:
 *   app.post('/webhooks/zangi', zangiWebhookMiddleware());
 *
 * @param {object} [opts]
 * @param {boolean} [opts.requireSignature]  Force signature check even without secret (default: false)
 * @returns {Function}  Express route handler
 */
function zangiWebhookMiddleware(opts = {}) {
  const { requireSignature = false } = opts;

  return async function zangiWebhookHandler(req, res) {
    // ------------------------------------------------------------------
    // 1. Capture raw body for HMAC (bodyParser must NOT have consumed it,
    //    or the raw body must be stored on req.rawBody by middleware).
    // ------------------------------------------------------------------
    const rawBody = req.rawBody || (req.body ? JSON.stringify(req.body) : '');

    // ------------------------------------------------------------------
    // 2. Verify signature
    // ------------------------------------------------------------------
    const signature = req.headers['x-zangi-signature'] || '';
    if (!verifySignature(rawBody, signature)) {
      if (requireSignature || WEBHOOK_SECRET) {
        console.error('[ZangiWebhook] Signature verification FAILED.');
        return res.status(401).json({ error: 'Invalid signature' });
      }
    }

    // ------------------------------------------------------------------
    // 3. Parse body
    // ------------------------------------------------------------------
    let payload;
    try {
      payload = typeof req.body === 'object' ? req.body : JSON.parse(rawBody);
    } catch (err) {
      console.error('[ZangiWebhook] Failed to parse request body:', err.message);
      return res.status(400).json({ error: 'Invalid JSON body' });
    }

    // ------------------------------------------------------------------
    // 4. ACK immediately (Zangi expects < 5 s response)
    // ------------------------------------------------------------------
    res.status(200).json({ received: true });

    // ------------------------------------------------------------------
    // 5. Process events asynchronously
    // ------------------------------------------------------------------
    const events = Array.isArray(payload.events) ? payload.events : [payload];

    for (const event of events) {
      try {
        const result = await processEvent(event);
        console.info('[ZangiWebhook] Processed event:', result);
      } catch (err) {
        console.error('[ZangiWebhook] Error processing event:', err.message, event);
      }
    }
  };
}

// ---------------------------------------------------------------------------
// Exports
// ---------------------------------------------------------------------------

module.exports = {
  zangiWebhookMiddleware,
  processEvent,
  verifySignature,
  registerAgentHandler,
  unregisterAgentHandler,
  dispatchToAgent,
};
