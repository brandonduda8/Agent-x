// Agent X packet schema shared between core and clients
// Keep JSON serializable; no circular structures.

const STATUS = Object.freeze({
  QUEUED: 'queued',
  RUNNING: 'running',
  COMPLETED: 'completed',
  FAILED: 'failed'
});

// ---------------------------------------------------------------------------
// Task types
// ---------------------------------------------------------------------------

const TASK_TYPES = Object.freeze({
  // Generic
  GENERIC: 'generic',

  // Zangi messaging
  ZANGI_MESSAGE: 'zangi:message',
  ZANGI_BROADCAST: 'zangi:broadcast',
  ZANGI_COMMAND: 'zangi:command',
  ZANGI_STATUS: 'zangi:status',
  ZANGI_RESULT: 'zangi:result',

  // Core agent types
  CONTENT: 'content',
  DATA: 'data',
  PUBLISH: 'publish',
  INFRA: 'infrastructure',
  ORCHESTRATE: 'orchestrate',
});

// ---------------------------------------------------------------------------
// Task factory
// ---------------------------------------------------------------------------

function createTask({ type = 'generic', payload = {}, webhook = null, priority = 'normal' }) {
  return {
    id: crypto.randomUUID(),
    type,
    payload,
    webhook,
    priority,
    status: STATUS.QUEUED,
    events: [{ type: 'created', timestamp: new Date().toISOString() }],
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    completedAt: null,
    result: null
  };
}

// ---------------------------------------------------------------------------
// Zangi-specific packet factories
// ---------------------------------------------------------------------------

/**
 * Create a task packet wrapping an inbound Zangi message.
 *
 * @param {object} opts
 * @param {string} opts.from          Zangi sender user ID
 * @param {string} [opts.to]          Zangi recipient user ID (null for channels)
 * @param {string} [opts.channelId]   Zangi channel ID (null for DMs)
 * @param {string} opts.message       Message text body
 * @param {object} [opts.rawEvent]    Full raw Zangi webhook event
 * @param {string} [opts.priority]    Task priority (default: 'normal')
 * @returns {object}  Agent X task packet
 */
function createZangiMessageTask({ from, to = null, channelId = null, message, rawEvent = {}, priority = 'normal' }) {
  return createTask({
    type: TASK_TYPES.ZANGI_MESSAGE,
    payload: {
      source: 'zangi',
      from,
      to,
      channelId,
      message,
      rawEvent,
    },
    priority,
  });
}

/**
 * Create a broadcast task packet (sent to all active agents).
 *
 * @param {object} opts
 * @param {string} opts.message       Broadcast message text
 * @param {object} [opts.rawEvent]    Raw Zangi event
 * @param {string} [opts.priority]    Task priority
 * @returns {object}
 */
function createZangiBroadcastTask({ message, rawEvent = {}, priority = 'normal' }) {
  return createTask({
    type: TASK_TYPES.ZANGI_BROADCAST,
    payload: {
      source: 'zangi',
      broadcast: true,
      message,
      rawEvent,
    },
    priority,
  });
}

// ---------------------------------------------------------------------------
// Exports
// ---------------------------------------------------------------------------

module.exports = {
  STATUS,
  TASK_TYPES,
  createTask,
  createZangiMessageTask,
  createZangiBroadcastTask,
};
