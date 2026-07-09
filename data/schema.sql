-- =============================================================================
-- Agent X — Reference Schema
-- =============================================================================
-- This file documents the logical data model used by Agent X.
-- The runtime persistence layer is JSON flat-files (data/*.json, memory/*.json)
-- rather than a relational DB, so this SQL is provided as a canonical
-- reference / for future migration to a relational backend.
-- =============================================================================

-- ---------------------------------------------------------------------------
-- agents
-- ---------------------------------------------------------------------------
-- Tracks every agent registered in the Agent Registry.
-- Maintained at runtime via agent-x-core/registry/agent-registry.js.
-- Heartbeats are recorded via POST /api/agents/:id/heartbeat and the
-- heartbeat monitor (agent-x-core/registry/heartbeat-monitor.js) demotes
-- non-responsive agents to "stale" every 30 seconds.
--
-- status lifecycle:
--   idle     → newly registered or finished current task
--   active   → currently executing a task
--   stale    → missed heartbeat threshold (60 s by default)
--   offline  → manually set offline or gracefully shut down
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS agents (
    id               TEXT        PRIMARY KEY,           -- UUID v4
    name             TEXT        NOT NULL,
    type             TEXT        NOT NULL,              -- e.g. "worker", "orchestrator"
    capabilities     TEXT        NOT NULL DEFAULT '[]', -- JSON-serialised string[]
    status           TEXT        NOT NULL DEFAULT 'idle'
                                 CHECK (status IN ('active', 'idle', 'stale', 'offline')),
    current_task_id  TEXT        DEFAULT NULL,
    last_heartbeat   DATETIME    DEFAULT NULL,          -- UTC ISO-8601; NULL = never heartbeated
    created_at       DATETIME    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at       DATETIME    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE INDEX IF NOT EXISTS idx_agents_status ON agents (status);
CREATE INDEX IF NOT EXISTS idx_agents_type   ON agents (type);

-- ---------------------------------------------------------------------------
-- tasks
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tasks (
    id          TEXT     PRIMARY KEY,                   -- UUID v4
    type        TEXT     NOT NULL,
    payload     TEXT     NOT NULL DEFAULT '{}',         -- JSON blob
    status      TEXT     NOT NULL DEFAULT 'queued'
                         CHECK (status IN ('queued', 'running', 'done', 'failed')),
    agent_id    TEXT     DEFAULT NULL REFERENCES agents(id) ON DELETE SET NULL,
    created_at  DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at  DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE INDEX IF NOT EXISTS idx_tasks_status   ON tasks (status);
CREATE INDEX IF NOT EXISTS idx_tasks_agent_id ON tasks (agent_id);

-- ---------------------------------------------------------------------------
-- products
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS products (
    id          TEXT     PRIMARY KEY,
    name        TEXT     NOT NULL,
    type        TEXT     NOT NULL,
    price       REAL     NOT NULL DEFAULT 0,
    currency    TEXT     NOT NULL DEFAULT 'usd',
    stripe_id   TEXT     DEFAULT NULL,
    published   INTEGER  NOT NULL DEFAULT 0,            -- boolean 0/1
    created_at  DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at  DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

-- ---------------------------------------------------------------------------
-- revenue
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS transactions (
    id          TEXT     PRIMARY KEY,
    product_id  TEXT     DEFAULT NULL REFERENCES products(id) ON DELETE SET NULL,
    amount      REAL     NOT NULL,
    currency    TEXT     NOT NULL DEFAULT 'usd',
    source      TEXT     DEFAULT NULL,                  -- e.g. "stripe", "manual"
    created_at  DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);
