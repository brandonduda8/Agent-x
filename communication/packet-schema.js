// Agent X packet schema shared between core and clients
// Keep JSON serializable; no circular structures.

const STATUS = Object.freeze({
  QUEUED: 'queued',
  RUNNING: 'running',
  COMPLETED: 'completed',
  FAILED: 'failed'
});

function createTask({ type = 'generic', payload = {}, webhook = null, priority = 'normal' }) {
  return {
    id: crypto.randomUUID(),
    type,
    payload,
    webhook,
    priority,
    status: STATUS.QUEUED,
    events: [{ type: 'created' }],
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    completedAt: null,
    result: null
  };
}

module.exports = { STATUS, createTask };
