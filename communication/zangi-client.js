/**
 * Zangi Communication Client
 *
 * Wraps the Zangi REST API for real-time messaging.
 * Handles authentication, message delivery, group broadcasts,
 * and retries with exponential back-off.
 *
 * Environment variables required:
 *   ZANGI_API_KEY      – your Zangi application API key
 *   ZANGI_API_SECRET   – your Zangi application API secret
 *   ZANGI_BASE_URL     – base URL for Zangi REST API
 *                        (default: https://api.zangi.com/v1)
 *   ZANGI_APP_ID       – Zangi application / tenant ID
 */

'use strict';

const https = require('https');
const http = require('http');
const { URL } = require('url');

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const DEFAULT_BASE_URL = 'https://api.zangi.com/v1';
const DEFAULT_TIMEOUT_MS = 10_000;
const MAX_RETRIES = 3;
const RETRY_BASE_DELAY_MS = 500;

// Message types recognised by Agent X
const MESSAGE_TYPES = Object.freeze({
  TEXT: 'text',
  TASK: 'task',
  STATUS: 'status',
  BROADCAST: 'broadcast',
  COMMAND: 'command',
  RESULT: 'result',
});

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Sleep for `ms` milliseconds.
 * @param {number} ms
 * @returns {Promise<void>}
 */
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Perform a raw HTTPS/HTTP JSON request.
 *
 * @param {object} options
 * @param {string} options.method       HTTP verb
 * @param {string} options.url          Full URL
 * @param {object} [options.headers]    Additional headers
 * @param {object|null} [options.body]  JSON-serialisable body (or null)
 * @param {number} [options.timeoutMs]  Request timeout in ms
 * @returns {Promise<{status: number, headers: object, body: any}>}
 */
function rawRequest({ method, url, headers = {}, body = null, timeoutMs = DEFAULT_TIMEOUT_MS }) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const isHttps = parsed.protocol === 'https:';
    const lib = isHttps ? https : http;

    const payload = body !== null ? JSON.stringify(body) : null;

    const reqOptions = {
      hostname: parsed.hostname,
      port: parsed.port || (isHttps ? 443 : 80),
      path: parsed.pathname + parsed.search,
      method: method.toUpperCase(),
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        ...headers,
        ...(payload !== null ? { 'Content-Length': Buffer.byteLength(payload) } : {}),
      },
    };

    const req = lib.request(reqOptions, (res) => {
      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => {
        const raw = Buffer.concat(chunks).toString('utf8');
        let parsed;
        try {
          parsed = JSON.parse(raw);
        } catch {
          parsed = raw;
        }
        resolve({ status: res.statusCode, headers: res.headers, body: parsed });
      });
    });

    req.setTimeout(timeoutMs, () => {
      req.destroy(new Error(`Zangi request timed out after ${timeoutMs}ms`));
    });

    req.on('error', reject);

    if (payload !== null) {
      req.write(payload);
    }
    req.end();
  });
}

// ---------------------------------------------------------------------------
// ZangiClient class
// ---------------------------------------------------------------------------

class ZangiClient {
  /**
   * @param {object} [opts]
   * @param {string} [opts.apiKey]      Override ZANGI_API_KEY env var
   * @param {string} [opts.apiSecret]   Override ZANGI_API_SECRET env var
   * @param {string} [opts.baseUrl]     Override ZANGI_BASE_URL env var
   * @param {string} [opts.appId]       Override ZANGI_APP_ID env var
   * @param {number} [opts.timeoutMs]   Request timeout in ms
   * @param {boolean} [opts.debug]      Log requests/responses to console
   */
  constructor(opts = {}) {
    this.apiKey = opts.apiKey || process.env.ZANGI_API_KEY || '';
    this.apiSecret = opts.apiSecret || process.env.ZANGI_API_SECRET || '';
    this.baseUrl = (opts.baseUrl || process.env.ZANGI_BASE_URL || DEFAULT_BASE_URL).replace(/\/$/, '');
    this.appId = opts.appId || process.env.ZANGI_APP_ID || '';
    this.timeoutMs = opts.timeoutMs || DEFAULT_TIMEOUT_MS;
    this.debug = opts.debug || process.env.ZANGI_DEBUG === 'true';

    if (!this.apiKey) {
      console.warn('[ZangiClient] WARNING: ZANGI_API_KEY is not set. API calls will fail.');
    }
    if (!this.appId) {
      console.warn('[ZangiClient] WARNING: ZANGI_APP_ID is not set.');
    }
  }

  // -------------------------------------------------------------------------
  // Internal helpers
  // -------------------------------------------------------------------------

  /** Build standard auth headers for every request. */
  _authHeaders() {
    // Zangi uses a simple API-Key + API-Secret header pair.
    // Adjust this if Zangi changes their auth scheme (e.g. Bearer JWT).
    return {
      'X-Zangi-Api-Key': this.apiKey,
      'X-Zangi-Api-Secret': this.apiSecret,
      'X-Zangi-App-Id': this.appId,
    };
  }

  /**
   * Send an authenticated request with retry on transient failures.
   *
   * @param {string} method   HTTP verb
   * @param {string} path     URL path relative to baseUrl (e.g. '/messages')
   * @param {object|null} body  Request body
   * @returns {Promise<any>}  Parsed response body
   */
  async _request(method, path, body = null) {
    const url = `${this.baseUrl}${path}`;
    const headers = this._authHeaders();

    let lastError;
    for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
      try {
        if (this.debug) {
          console.debug(`[ZangiClient] ${method} ${url}`, body ? JSON.stringify(body) : '');
        }

        const { status, body: resBody } = await rawRequest({
          method,
          url,
          headers,
          body,
          timeoutMs: this.timeoutMs,
        });

        if (this.debug) {
          console.debug(`[ZangiClient] → ${status}`, JSON.stringify(resBody));
        }

        // Treat 2xx as success
        if (status >= 200 && status < 300) {
          return resBody;
        }

        // 4xx errors are client errors — do not retry
        if (status >= 400 && status < 500) {
          const err = new Error(`Zangi API error ${status}: ${JSON.stringify(resBody)}`);
          err.status = status;
          err.response = resBody;
          throw err;
        }

        // 5xx — retry
        lastError = new Error(`Zangi server error ${status}: ${JSON.stringify(resBody)}`);
        lastError.status = status;
      } catch (err) {
        if (err.status && err.status >= 400 && err.status < 500) throw err; // no retry
        lastError = err;
      }

      if (attempt < MAX_RETRIES) {
        const delay = RETRY_BASE_DELAY_MS * Math.pow(2, attempt);
        console.warn(`[ZangiClient] Attempt ${attempt + 1} failed (${lastError.message}). Retrying in ${delay}ms…`);
        await sleep(delay);
      }
    }

    throw lastError;
  }

  // -------------------------------------------------------------------------
  // Messaging API
  // -------------------------------------------------------------------------

  /**
   * Send a direct message to a single Zangi user.
   *
   * @param {object} opts
   * @param {string} opts.toUserId        Zangi user ID of the recipient
   * @param {string} opts.text            Plain-text message body
   * @param {string} [opts.type]          Agent X message type (default: 'text')
   * @param {object} [opts.metadata]      Arbitrary JSON metadata attached to message
   * @returns {Promise<object>}           Zangi API response
   */
  async sendDirectMessage({ toUserId, text, type = MESSAGE_TYPES.TEXT, metadata = {} }) {
    if (!toUserId) throw new Error('sendDirectMessage: toUserId is required');
    if (!text) throw new Error('sendDirectMessage: text is required');

    return this._request('POST', '/messages/direct', {
      to: toUserId,
      message: text,
      type,
      metadata: {
        agentX: true,
        messageType: type,
        ...metadata,
      },
    });
  }

  /**
   * Send a message to a Zangi group / channel.
   *
   * @param {object} opts
   * @param {string} opts.channelId       Zangi channel / group ID
   * @param {string} opts.text            Plain-text message body
   * @param {string} [opts.type]          Agent X message type (default: 'broadcast')
   * @param {object} [opts.metadata]      Arbitrary JSON metadata
   * @returns {Promise<object>}           Zangi API response
   */
  async sendChannelMessage({ channelId, text, type = MESSAGE_TYPES.BROADCAST, metadata = {} }) {
    if (!channelId) throw new Error('sendChannelMessage: channelId is required');
    if (!text) throw new Error('sendChannelMessage: text is required');

    return this._request('POST', '/messages/channel', {
      channelId,
      message: text,
      type,
      metadata: {
        agentX: true,
        messageType: type,
        ...metadata,
      },
    });
  }

  /**
   * Broadcast a message to ALL agents via the shared group channel.
   *
   * @param {object} opts
   * @param {string} opts.text            Message text
   * @param {string} [opts.broadcastChannelId]  Override the default broadcast channel
   * @param {object} [opts.metadata]      Extra metadata
   * @returns {Promise<object>}
   */
  async broadcast({ text, broadcastChannelId, metadata = {} }) {
    const channelId = broadcastChannelId
      || process.env.ZANGI_BROADCAST_CHANNEL_ID
      || '';

    if (!channelId) {
      throw new Error(
        'broadcast: No channel ID provided and ZANGI_BROADCAST_CHANNEL_ID is not set'
      );
    }

    return this.sendChannelMessage({
      channelId,
      text,
      type: MESSAGE_TYPES.BROADCAST,
      metadata,
    });
  }

  /**
   * Retrieve recent messages from a channel (useful for polling / reconciliation).
   *
   * @param {string} channelId
   * @param {number} [limit=50]
   * @returns {Promise<object[]>}
   */
  async getChannelMessages(channelId, limit = 50) {
    if (!channelId) throw new Error('getChannelMessages: channelId is required');
    return this._request('GET', `/messages/channel/${encodeURIComponent(channelId)}?limit=${limit}`);
  }

  /**
   * Retrieve a user's direct message history.
   *
   * @param {string} userId
   * @param {number} [limit=50]
   * @returns {Promise<object[]>}
   */
  async getDirectMessages(userId, limit = 50) {
    if (!userId) throw new Error('getDirectMessages: userId is required');
    return this._request('GET', `/messages/direct/${encodeURIComponent(userId)}?limit=${limit}`);
  }

  // -------------------------------------------------------------------------
  // Webhook registration helpers
  // -------------------------------------------------------------------------

  /**
   * Register a webhook URL with Zangi so inbound events are forwarded.
   *
   * @param {object} opts
   * @param {string} opts.webhookUrl      Publicly reachable URL for this listener
   * @param {string[]} [opts.events]      Event types to subscribe (default: all)
   * @returns {Promise<object>}
   */
  async registerWebhook({ webhookUrl, events = ['message.received', 'message.delivered', 'message.read'] }) {
    if (!webhookUrl) throw new Error('registerWebhook: webhookUrl is required');
    return this._request('POST', '/webhooks', {
      url: webhookUrl,
      events,
      appId: this.appId,
      secret: this.apiSecret, // Zangi may use this for HMAC signing
    });
  }

  /**
   * List all registered webhooks for this application.
   * @returns {Promise<object[]>}
   */
  async listWebhooks() {
    return this._request('GET', '/webhooks');
  }

  /**
   * Delete a webhook registration.
   * @param {string} webhookId
   * @returns {Promise<object>}
   */
  async deleteWebhook(webhookId) {
    if (!webhookId) throw new Error('deleteWebhook: webhookId is required');
    return this._request('DELETE', `/webhooks/${encodeURIComponent(webhookId)}`);
  }

  // -------------------------------------------------------------------------
  // User / Channel management helpers
  // -------------------------------------------------------------------------

  /**
   * Create or upsert a Zangi user (used when mapping a new agent).
   *
   * @param {object} opts
   * @param {string} opts.userId    Your internal / Zangi user ID
   * @param {string} opts.name      Display name
   * @param {object} [opts.meta]    Arbitrary metadata
   * @returns {Promise<object>}
   */
  async upsertUser({ userId, name, meta = {} }) {
    return this._request('POST', '/users', { userId, name, meta });
  }

  /**
   * Create or upsert a Zangi channel.
   *
   * @param {object} opts
   * @param {string} opts.channelId   Your channel ID
   * @param {string} opts.name        Human-readable name
   * @param {string[]} [opts.members] Initial member user IDs
   * @returns {Promise<object>}
   */
  async upsertChannel({ channelId, name, members = [] }) {
    return this._request('POST', '/channels', { channelId, name, members });
  }
}

// ---------------------------------------------------------------------------
// Module exports
// ---------------------------------------------------------------------------

module.exports = { ZangiClient, MESSAGE_TYPES };
