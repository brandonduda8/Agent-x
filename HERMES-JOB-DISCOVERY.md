# Agent Hermes — Job Discovery & Matching

## Overview

Agent Hermes is the **job discovery and routing subsystem** of Agent X. It continuously scans configured job sources, normalises discovered work items into a canonical schema, scores each item against the live agent registry, and assigns jobs to the best-matched agents.

```
┌──────────────────────────────────────────────────────────────┐
│                      Agent Hermes                            │
│                                                              │
│  ┌─────────────────────┐     ┌──────────────────────────┐   │
│  │   job-discovery.js  │────►│      job-store.js        │   │
│  │  ─────────────────  │     │  ──────────────────────  │   │
│  │  Internal queues    │     │  In-memory Map +         │   │
│  │  Remote job boards  │     │  disk persistence        │   │
│  │  Mock board (dev)   │     │  (data/hermes-jobs.json) │   │
│  └─────────────────────┘     └────────────┬─────────────┘   │
│                                           │                  │
│  ┌────────────────────────────────────────▼─────────────┐   │
│  │                   job-matcher.js                      │   │
│  │  ─────────────────────────────────────────────────   │   │
│  │  Capability coverage  (50 pts)                        │   │
│  │  Type affinity        (20 pts)                        │   │
│  │  Inverse agent load   (15 pts)                        │   │
│  │  Priority boost       (10 pts)                        │   │
│  │  Status health        ( 5 pts)                        │   │
│  └────────────────────────────────────────┬─────────────┘   │
│                                           │                  │
│  ┌────────────────────────────────────────▼─────────────┐   │
│  │                  hermes-agent.js                      │   │
│  │  ─────────────────────────────────────────────────   │   │
│  │  Orchestrates discovery + matching lifecycle          │   │
│  │  Polls agent registry (HERMES_REGISTRY_URL)           │   │
│  │  Emits events on hermesEvents EventEmitter            │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐   │
│  │         agent-x-core/routes/hermes.js                 │   │
│  │  REST API mounted at /api/hermes                      │   │
│  └───────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

---

## File Reference

| File | Role |
|---|---|
| `hermes/job-store.js` | Persistent job state — in-memory Map + `data/hermes-jobs.json` |
| `hermes/job-discovery.js` | Scans internal task files, remote boards, and the built-in mock board |
| `hermes/job-matcher.js` | Scores and routes jobs to agents via a weighted capability algorithm |
| `hermes/hermes-agent.js` | Core orchestrator — wires discovery, matching, registry polling, events |
| `agent-x-core/routes/hermes.js` | Express router exposing the `/api/hermes` REST API |
| `hermes/hermes.test.js` | Full test suite (no external framework required) |

---

## REST API

Mount point: **`/api/hermes`** (configured in `agent-x-core/index.js`)

### Jobs

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/hermes/jobs` | List all jobs. Filter via `?status=`, `?type=`, `?source=`. Paginate via `?limit=&offset=`. Sort via `?sort=&order=`. |
| `POST` | `/api/hermes/jobs` | Submit a new job directly into the pipeline |
| `GET` | `/api/hermes/jobs/:id` | Get a single job by ID |
| `PATCH` | `/api/hermes/jobs/:id` | Update mutable fields (status, priority, payload, etc.) |
| `DELETE` | `/api/hermes/jobs/:id` | Permanently remove a job |
| `GET` | `/api/hermes/jobs/:id/rank` | Rank all available agents for a job (read-only, no assignment) |

### Control

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/hermes/scan` | Trigger a one-shot discovery scan; returns newly added jobs |
| `POST` | `/api/hermes/match` | Trigger a one-shot match cycle; returns `{ assigned, unmatched, elapsed }` |
| `GET` | `/api/hermes/stats` | Aggregate statistics (total jobs, by-status counts, agent cache size) |
| `GET` | `/api/hermes/health` | Liveness probe — always `200 OK` when mounted |

### POST /api/hermes/jobs — Request Body

```json
{
  "title"       : "Write 3-email welcome sequence",
  "type"        : "content",
  "source"      : "api",
  "requiredCaps": ["draft", "email"],
  "payload"     : { "product": "SaaS onboarding", "tone": "friendly" },
  "priority"    : 8,
  "expiresAt"   : null
}
```

### Response Envelope

All responses follow the same envelope:

```json
{
  "ok"   : true,
  "ts"   : "2025-01-01T00:00:00.000Z",
  "data" : { ... }
}
```

Errors return `"ok": false` with an `"error"` field and an appropriate HTTP status code.

---

## Job Schema

```json
{
  "id"           : "uuid-v4",
  "title"        : "Human-readable job title",
  "source"       : "internal-queue:data | board:<url> | mock-board | api",
  "type"         : "content | research | publish | infrastructure | data | generic",
  "requiredCaps" : ["draft", "email"],
  "payload"      : {},
  "priority"     : 7,
  "status"       : "open | assigned | in-progress | done | failed",
  "assignedTo"   : "agent-id | null",
  "score"        : 82,
  "createdAt"    : "ISO8601",
  "updatedAt"    : "ISO8601",
  "expiresAt"    : "ISO8601 | null"
}
```

---

## Scoring Model

The matcher awards up to **100 points** per `(job, agent)` pair:

| Component | Weight | Logic |
|---|---|---|
| **Capability coverage** | 50 pts | `matched_caps / required_caps × 50`. Full marks if job has no required caps. |
| **Type affinity** | 20 pts | Checks agent's `types`, `capabilities`, `type`, and `name` for the job's type string. Exact = 20, substring = 12, none = 0. |
| **Inverse agent load** | 15 pts | `(1 − load/10) × 15`. Prefers agents with fewer active tasks. |
| **Priority boost** | 10 pts | High-priority jobs nudge the score toward less-loaded agents. |
| **Status health** | 5 pts | `active=5`, `registered=3`, `stale=1`, `dead=0`. |

Agents with **zero capability overlap** (when caps are required) are excluded entirely. Dead agents are always excluded.

---

## Job Discovery Sources

### 1. Internal Task Queues (always enabled)

Reads from:
- `data/tasks.json`
- `agent-x-core/tasks.json`
- `memory/tasks.json`

Accepts arrays at the root or under keys `tasks`, `jobs`, `items`, `queue`. Already-completed items (`status: done/completed/cancelled`) are skipped.

### 2. Remote Job Boards (optional)

Set the `HERMES_JOB_BOARDS` environment variable to a comma-separated list of URLs that return JSON arrays of job objects:

```bash
HERMES_JOB_BOARDS=https://jobs.example.com/api/feed,https://board2.example.com/tasks
```

Each endpoint must return either a JSON array or an object with a `jobs`, `tasks`, `items`, or `data` key.

### 3. Mock Board (dev / CI)

Enabled by default. Disable with `HERMES_MOCK_BOARD=false`.

Provides 6 representative jobs covering all capability types, useful for testing the matcher without external dependencies.

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `HERMES_DISCOVERY_INTERVAL_MS` | `60000` | Discovery poll interval (ms) |
| `HERMES_MATCH_INTERVAL_MS` | `15000` | Match cycle interval (ms) |
| `HERMES_REGISTRY_URL` | `http://localhost:3000/v1/registry/agents` | Agent registry endpoint |
| `HERMES_JOB_BOARDS` | _(empty)_ | Comma-separated remote board URLs |
| `HERMES_MOCK_BOARD` | `true` | Include built-in mock jobs (`false` to disable) |
| `HERMES_FETCH_TIMEOUT_MS` | `8000` | HTTP timeout for remote board fetches |

---

## Event Bus

`hermes-agent.js` exports an `events` `EventEmitter`. Other subsystems can subscribe:

```js
const hermes = require("./hermes/hermes-agent");

hermes.events.on("job:discovered", ({ job }) => {
  console.log("New job discovered:", job.title);
});

hermes.events.on("job:assigned", ({ job, agentId }) => {
  console.log(`Job "${job.title}" assigned to ${agentId} (score: ${job.score})`);
});

hermes.events.on("job:unmatched", ({ job }) => {
  console.warn(`No agent found for: ${job.title}`);
});

hermes.events.on("match:cycle", ({ assigned, unmatched, elapsed }) => {
  console.log(`Cycle: +${assigned} assigned, ${unmatched} pending, ${elapsed}ms`);
});
```

---

## Running Tests

```bash
# From repo root
node hermes/hermes.test.js

# Via npm script
npm test
npm run test:hermes
```

The test suite covers:
- `job-store` — CRUD, validation, expiry, stats
- `job-matcher` — scoring, ranking, exclusion rules, weight sum
- `job-discovery` — normalisation, dedup, mock board, scanAll
- `hermes-agent` — programmatic API, event emission

No external framework or network access required.

---

## Integration with Agent Registry

Hermes fetches the live agent list from `HERMES_REGISTRY_URL` (default: `/v1/registry/agents`) before each match cycle. It caches the last known list and falls back gracefully when the registry is unreachable (e.g. during startup race conditions).

Agent records must have:
- `id` — unique identifier
- `capabilities` — string array matching job `requiredCaps`
- `status` — `active | registered | stale | dead`
- `currentLoad` _(optional)_ — number of active tasks (0 if omitted)

---

## Persistence

Jobs are persisted to **`data/hermes-jobs.json`** automatically after every write operation (debounced, 10 ms). The store is reloaded from disk on startup, so jobs survive process restarts.

Expired jobs (`expiresAt` in the past) are purged on Hermes startup via `jobStore.purgeExpired()`.
