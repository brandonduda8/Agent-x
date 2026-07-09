# Agent Upgrade & Configuration Versioning

Complete reference for the Agent X upgrade system: configuration version history,
graceful restart orchestration, and full audit logging.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [File Map](#file-map)
4. [Data Schemas](#data-schemas)
5. [REST API Reference](#rest-api-reference)
6. [Upgrade Lifecycle](#upgrade-lifecycle)
7. [Rollback](#rollback)
8. [Audit Log](#audit-log)
9. [Graceful Restart Strategy](#graceful-restart-strategy)
10. [Configuration (Environment Variables)](#configuration-environment-variables)
11. [Usage Examples](#usage-examples)
12. [Running Tests](#running-tests)

---

## Overview

The upgrade system provides three tightly-integrated capabilities:

| Capability | Module | Description |
|---|---|---|
| **Config versioning** | `agent-config-store.js` | Append-only version history per agent stored in `data/agent_configs.json` |
| **Upgrade orchestration** | `upgrade-manager.js` | Validates config, writes new version, restarts agent, confirms liveness, rolls back on failure |
| **Audit logging** | `audit-log.js` | Append-only record of every upgrade event written to `data/upgrade_audit.json` |

---

## Architecture

```
POST /api/agents/:id/upgrade
          │
          ▼
  routes/upgrade.js         ← Express router, validates HTTP layer
          │
          ▼
  upgrade-manager.js        ← Orchestration engine
    │  1. _validateConfig()
    │  2. configStore.createVersion()
    │  3. auditLog.append(UPGRADE_STARTED)
    │  4. Attempt graceful restart:
    │       a) pm2 restart <agentName>
    │       b) registry.restartAgent(id)  ← callback from watchdog
    │       c) manual-required            ← fallback
    │  5. Poll registry heartbeat for liveness
    │  6. configStore.setCurrentVersion() ← on success
    │     configStore.setCurrentVersion(prior) ← on rollback
    │  7. auditLog.append(CONFIG_UPGRADED | CONFIG_ROLLED_BACK)
    │
    ├──► agent-config-store.js   ← data/agent_configs.json
    └──► audit-log.js            ← data/upgrade_audit.json
```

---

## File Map

```
agent-x-core/
├── registry/
│   ├── agent-config-store.js   ← Versioned config store
│   ├── upgrade-manager.js      ← Upgrade orchestration + rollback
│   ├── audit-log.js            ← Append-only audit log
│   ├── agent-registry.js       ← Agent CRUD + restart callback registry
│   ├── heartbeat-monitor.js    ← Periodic liveness checker
│   ├── registry-api.js         ← REST: /v1/registry/agents/*
│   └── registry.test.js        ← Unit + integration tests
├── routes/
│   ├── upgrade.js              ← REST: /api/agents/:id/upgrade etc.
│   └── agents.js               ← Existing agent route
└── index.js                    ← Express app — mounts all routers

data/
├── agent_configs.json          ← Config version history (auto-created)
└── upgrade_audit.json          ← Audit log (auto-created)
```

---

## Data Schemas

### `data/agent_configs.json`

```json
{
  "<agentId>": {
    "currentVersion": 3,
    "versions": [
      {
        "version":   1,
        "createdAt": "2025-01-01T00:00:00.000Z",
        "createdBy": "system",
        "label":     "initial",
        "config":    { "timeout": 5000, "retries": 3 },
        "changelog": "Initial configuration"
      },
      {
        "version":   2,
        "createdAt": "2025-01-02T00:00:00.000Z",
        "createdBy": "user:alice",
        "label":     "bump-timeout",
        "config":    { "timeout": 9000, "retries": 3 },
        "changelog": "Increased timeout for slow upstream"
      }
    ]
  }
}
```

**Rules:**
- Version numbers are monotonically increasing integers starting at `1`
- All prior versions are retained for rollback (up to `MAX_CONFIG_VERSIONS`, default 50)
- The `config` object is deep-cloned at write time — mutations to the original object do not affect stored versions

### `data/upgrade_audit.json`

```json
[
  {
    "id":             "uuid-v4",
    "timestamp":      "ISO8601",
    "agentId":        "agent-uuid",
    "agentName":      "content-generator",
    "action":         "UPGRADE_STARTED",
    "actor":          "user:alice",
    "fromVersion":    2,
    "toVersion":      3,
    "configSnapshot": { "timeout": 9000 },
    "outcome":        "success",
    "reason":         "Bumped timeout",
    "meta":           { "restartMethod": "pm2" }
  }
]
```

### Audit Actions

| Action | Triggered when |
|---|---|
| `CONFIG_CREATED` | New config staged via `POST /api/agents/:id/configs` |
| `UPGRADE_STARTED` | `applyUpgrade()` begins |
| `CONFIG_UPGRADED` | Upgrade completed and new version committed as current |
| `AGENT_RESTARTED` | Agent process successfully restarted |
| `RESTART_FAILED` | All restart methods failed |
| `CONFIG_ROLLED_BACK` | Agent did not heartbeat within timeout — prior version restored |
| `UPGRADE_ABORTED` | Config validation failed before any write |

---

## REST API Reference

All upgrade endpoints are mounted at `/api/agents`.
The base URL for a running instance is `http://localhost:3000`.

### `POST /api/agents/:id/upgrade`

Apply a new configuration version and restart the agent gracefully.

**Request headers:**
- `Content-Type: application/json`
- `X-Actor: user:alice` *(optional — recorded in audit log)*

**Request body:**
```json
{
  "config":      { "timeout": 9000, "retries": 5 },
  "changelog":   "Bumped timeout for slow upstream API",
  "label":       "v2-timeout-bump",
  "skipRestart": false
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `config` | object | ✅ | Full new configuration for the agent |
| `changelog` | string | — | Human-readable description of changes |
| `label` | string | — | Short label for this version |
| `skipRestart` | boolean | — | If `true`, commits the config without restarting (staging) |

**Response 200 (success):**
```json
{
  "ok":           true,
  "agentId":      "abc-123",
  "newVersion":   3,
  "priorVersion": 2,
  "rolledBack":   false,
  "restartMethod":"pm2",
  "auditId":      "uuid-of-audit-entry",
  "error":        null
}
```

**Response 200 with rollback:**
```json
{
  "ok":           false,
  "agentId":      "abc-123",
  "newVersion":   3,
  "priorVersion": 2,
  "rolledBack":   true,
  "restartMethod":"pm2",
  "auditId":      "uuid-of-rollback-audit-entry",
  "error":        "Agent did not send a heartbeat within 30000ms after restart"
}
```

**Response 400** — invalid/missing `config`  
**Response 409** — concurrent upgrade already in progress

---

### `POST /api/agents/:id/rollback`

Roll back to a specific prior config version.

**Request body:**
```json
{ "targetVersion": 1 }
```

**Response:** Same shape as `/upgrade`.

---

### `POST /api/agents/:id/configs`

Stage a new config version without triggering a restart.

**Request body:**
```json
{
  "config":    { "timeout": 9000 },
  "changelog": "Staged for review",
  "label":     "staging-v3"
}
```

**Response 201:**
```json
{
  "ok":           true,
  "agentId":      "abc-123",
  "versionRecord": { "version": 3, "createdAt": "...", ... }
}
```

---

### `GET /api/agents/:id/configs`

List all config versions for an agent (newest first).

**Response:**
```json
{
  "ok":             true,
  "agentId":        "abc-123",
  "currentVersion": 2,
  "totalVersions":  3,
  "versions":       [ ... ]
}
```

---

### `GET /api/agents/:id/configs/current`

Return the active config version.

---

### `GET /api/agents/:id/configs/:version`

Return a specific version record.

---

### `GET /api/agents/:id/configs/diff/:fromVersion/:toVersion`

Return a shallow diff between two versions.

**Response:**
```json
{
  "ok":          true,
  "agentId":     "abc-123",
  "fromVersion": 1,
  "toVersion":   2,
  "changedKeys": 1,
  "diff": {
    "timeout": [5000, 9000]
  }
}
```

---

### `GET /api/agents/:id/upgrade/status`

Return the in-memory upgrade progress state for a single agent.

```json
{
  "ok":          true,
  "agentId":     "abc-123",
  "upgradeState": {
    "status":      "done",
    "newVersion":  3,
    "priorVersion":2,
    "startedAt":   "2025-01-01T00:00:00.000Z",
    "completedAt": "2025-01-01T00:00:05.000Z",
    "error":       null
  }
}
```

**Status values:** `pending` | `restarting` | `confirming` | `done` | `failed`

---

### `GET /api/agents/upgrade/status`

Return all in-memory upgrade states.

---

### `GET /api/agents/audit`

Query the audit log.

**Query params:**

| Param | Description |
|---|---|
| `agentId` | Filter by agent |
| `action` | Filter by action type (e.g. `CONFIG_UPGRADED`) |
| `limit` | Max entries (default 200) |

---

### `GET /api/agents/audit/:entryId`

Return a single audit log entry by ID.

---

### `GET /api/agents/configs`

Return a summary of all agents that have config records.

---

## Upgrade Lifecycle

```
Client
  │  POST /api/agents/:id/upgrade { config, changelog }
  │
  ▼
upgrade.js (router)
  │  Resolve actor from X-Actor header
  │  Validate body shape
  │
  ▼
upgradeManager.applyUpgrade()
  │
  ├─[1]─ _validateConfig(newConfig)
  │         • must be non-null non-array object
  │         • must not be empty
  │         • must not contain __proto__ / constructor
  │       → Abort with 400 if invalid (UPGRADE_ABORTED audit entry)
  │
  ├─[2]─ configStore.createVersion()
  │         → New version record appended (NOT yet set as current)
  │
  ├─[3]─ auditLog.append(UPGRADE_STARTED)
  │
  ├─[4]─ Graceful restart (see Restart Strategy below)
  │         → auditLog.append(AGENT_RESTARTED | RESTART_FAILED)
  │
  ├─[5]─ Heartbeat poll (up to UPGRADE_CONFIRM_TIMEOUT_MS)
  │         → Poll registry.getAgent(id).lastHeartbeat every
  │           HEARTBEAT_POLL_INTERVAL_MS ms
  │
  ├─[6a] SUCCESS: configStore.setCurrentVersion(newVersion)
  │         → auditLog.append(CONFIG_UPGRADED)
  │         → upgradeState = { status: 'done' }
  │
  └─[6b] FAILURE (no heartbeat): configStore.setCurrentVersion(priorVersion)
            → auditLog.append(CONFIG_ROLLED_BACK)
            → upgradeState = { status: 'failed' }
            → Response: { ok: false, rolledBack: true, error: "..." }
```

---

## Rollback

Two rollback mechanisms are available:

### Automatic Rollback
If the agent does not send a heartbeat within `UPGRADE_CONFIRM_TIMEOUT_MS`
(default 30 s) after a restart, the prior version is automatically restored
as the active config, and a `CONFIG_ROLLED_BACK` audit entry is written.

### Manual Rollback
```bash
curl -X POST http://localhost:3000/api/agents/<id>/rollback \
  -H "Content-Type: application/json" \
  -H "X-Actor: user:alice" \
  -d '{"targetVersion": 1}'
```

**Important:** Manual rollback does not delete the failed version — it creates
a *new* version record that mirrors the target config. This preserves a complete
linear audit trail. The version number keeps incrementing; only `currentVersion`
changes.

---

## Audit Log

Every material event writes an entry to `data/upgrade_audit.json`.
The file is append-only (entries are never modified or deleted by the system,
only by the optional `purgeOld()` housekeeping function).

### Query the audit log

```bash
# All upgrades for a specific agent
curl "http://localhost:3000/api/agents/audit?agentId=<id>&limit=20"

# All rollback events across all agents
curl "http://localhost:3000/api/agents/audit?action=CONFIG_ROLLED_BACK"

# Single entry
curl "http://localhost:3000/api/agents/audit/<entryId>"
```

### Purge old entries (programmatic)

```js
const auditLog = require('./agent-x-core/registry/audit-log');
const removed = auditLog.purgeOld({ maxAgeDays: 30, agentId: 'abc-123' });
console.log(`Purged ${removed} old entries`);
```

---

## Graceful Restart Strategy

The upgrade manager attempts restarts in priority order:

| Priority | Method | When available |
|---|---|---|
| 1 | `pm2 restart <agentName>` | PM2 is installed and the agent is registered as a PM2 process |
| 2 | Registry restart callback | `registry.registerRestartCallback(agentId, fn)` was called by watchdog/orchestrator |
| 3 | `manual-required` | Neither PM2 nor a callback is available — config is still committed but operator must restart the agent |

**Registering a restart callback (e.g. from watchdog.js):**

```js
const registry = require('./registry/agent-registry');
const { spawn } = require('child_process');

// When you launch an agent process, register a restart callback:
registry.registerRestartCallback(agentId, async (id) => {
  // Kill existing process and re-spawn
  existingProcess.kill('SIGTERM');
  await new Promise(r => setTimeout(r, 1000));
  spawnAgent(id);
});
```

---

## Configuration (Environment Variables)

| Variable | Default | Description |
|---|---|---|
| `HEARTBEAT_INTERVAL_MS` | `15000` | How often the heartbeat monitor ticks |
| `STALE_THRESHOLD_MS` | `30000` | Time without heartbeat before agent → `stale` |
| `DEAD_THRESHOLD_MS` | `60000` | Time without heartbeat before agent → `dead` |
| `UPGRADE_CONFIRM_TIMEOUT_MS` | `30000` | Max wait for post-restart heartbeat |
| `HEARTBEAT_POLL_INTERVAL_MS` | `2000` | How often to poll during confirmation window |
| `PM2_BINARY` | `pm2` | Path to PM2 binary |
| `MAX_CONFIG_VERSIONS` | `50` | Max stored versions per agent (oldest pruned) |
| `PORT` | `3000` | agent-x-core HTTP port |

Set these in your `.env` file or export them before starting the service.

---

## Usage Examples

### Full upgrade flow (cURL)

```bash
# 1. Register an agent
AGENT=$(curl -s -X POST http://localhost:3000/v1/registry/agents/register \
  -H "Content-Type: application/json" \
  -d '{"name":"content-generator","type":"worker","capabilities":["draft","email"]}')

AGENT_ID=$(echo $AGENT | python3 -c "import sys,json; print(json.load(sys.stdin)['agent']['id'])")
echo "Agent ID: $AGENT_ID"

# 2. Apply initial config (no prior version → bootstraps v1)
curl -X POST "http://localhost:3000/api/agents/$AGENT_ID/upgrade" \
  -H "Content-Type: application/json" \
  -H "X-Actor: user:alice" \
  -d '{
    "config":    { "timeout": 5000, "retries": 3, "model": "gpt-4o-mini" },
    "changelog": "Initial deployment config",
    "skipRestart": true
  }'

# 3. Apply an upgrade
curl -X POST "http://localhost:3000/api/agents/$AGENT_ID/upgrade" \
  -H "Content-Type: application/json" \
  -H "X-Actor: user:alice" \
  -d '{
    "config":    { "timeout": 9000, "retries": 5, "model": "gpt-4o" },
    "changelog": "Upgraded model and bumped timeout"
  }'

# 4. View version history
curl "http://localhost:3000/api/agents/$AGENT_ID/configs"

# 5. Diff v1 → v2
curl "http://localhost:3000/api/agents/$AGENT_ID/configs/diff/1/2"

# 6. Roll back to v1
curl -X POST "http://localhost:3000/api/agents/$AGENT_ID/rollback" \
  -H "Content-Type: application/json" \
  -H "X-Actor: user:alice" \
  -d '{"targetVersion": 1}'

# 7. Query audit log
curl "http://localhost:3000/api/agents/audit?agentId=$AGENT_ID"
```

---

## Running Tests

```bash
cd agent-x-core
npm test
# or directly:
node registry/registry.test.js
```

The test suite covers:

- `_validateConfig` — valid, null, array, empty, prototype-pollution inputs
- `agent-config-store` — createVersion, getCurrent, setCurrentVersion (error path),
  listVersions, diffVersions, deleteAgent, listAll
- `audit-log` — append, query (agentId filter, action filter, limit), getById,
  getById (null), missing agentId error, AUDIT_ACTIONS completeness
- `upgrade-manager.applyUpgrade` (skipRestart) — success path, version increment,
  empty config rejection, non-object config rejection, audit entries, state tracking
- `upgrade-manager.rollbackTo` — creates mirror version, unknown version error,
  already-on-version error
- Concurrent upgrade guard

All tests run with redirected temp-file paths so they never touch real data files.
