# Agent X — Autonomous Build Pipeline & Real-Time Monitoring

## Overview

The pipeline subsystem adds a fully autonomous task execution layer to `agent-x-core`.
It handles work discovery, agent matching, dispatch, completion monitoring, failure retry
with exponential backoff, and real-time operator visibility via WebSocket.

```
External Hermes Jobs ──► JobSource fn
                              │
                    ┌─────────▼──────────┐
                    │   HermesPipeline   │  polls every N ms
                    │   (hermes-pipeline)│
                    └────────┬───────────┘
                             │
                    ┌────────▼───────────┐
                    │     TaskQueue      │  priority queue
                    │   (task-queue)     │  retry + backoff
                    │                   │  dead-letter store
                    └────────┬───────────┘
                             │
                    ┌────────▼───────────┐
                    │  AgentDispatcher   │  HTTP endpoint
                    │ (agent-dispatcher) │  stdio child-proc
                    │                   │  simulated (dev)
                    └────────┬───────────┘
                             │
              ┌──────────────▼──────────────────┐
              │         Shared Event Bus         │
              │         (EventEmitter)           │
              └──────────────┬──────────────────┘
                             │
              ┌──────────────▼──────────────────┐
              │       WsStatusServer             │
              │   /ws/agent-status  (ws pkg)     │
              │   broadcasts to dashboard clients│
              └─────────────────────────────────-┘
```

---

## File Map

| File | Purpose |
|---|---|
| `agent-x-core/pipeline/index.js` | Entry point; `mountPipeline()` wires everything together |
| `agent-x-core/pipeline/task-queue.js` | In-memory priority queue with retry/backoff/dead-letter |
| `agent-x-core/pipeline/hermes-pipeline.js` | Autonomous poll → match → dispatch loop |
| `agent-x-core/pipeline/agent-dispatcher.js` | HTTP / stdio / simulated dispatch strategies |
| `agent-x-core/pipeline/ws-status-server.js` | WebSocket server at `/ws/agent-status` |
| `agent-x-core/pipeline/pipeline-api.js` | Express router at `/pipeline` |
| `agent-x-core/pipeline/pipeline.test.js` | Full unit + integration test suite |

---

## Task Lifecycle

```
PENDING ──► ASSIGNED ──► COMPLETED
   ▲            │
   │            ▼
   └── (retry) FAILED ──(max retries)──► DEAD
```

| State | Meaning |
|---|---|
| `pending` | Waiting to be dispatched (includes back-off tasks waiting their timer) |
| `assigned` | Dispatched to an agent; awaiting completion signal |
| `completed` | Agent returned a successful result |
| `failed` | Dispatch raised an error; retries remain → scheduled for re-dispatch |
| `dead` | Retries exhausted; moved to dead-letter store for inspection |

### Retry Policy

| Attempt | Backoff |
|---------|---------|
| 1st retry | 1 s |
| 2nd retry | 2 s |
| 3rd retry | 4 s |
| (max 3 retries) | capped at 60 s |

---

## WebSocket — `/ws/agent-status`

### Connect

```js
const ws = new WebSocket('ws://localhost:3000/ws/agent-status');
```

### Server → Client message types

```jsonc
// Event stream
{ "type": "event", "event": "pipeline:task:completed", "data": { … }, "ts": "ISO8601" }

// Full snapshot (sent on connect + on demand)
{ "type": "snapshot", "ts": "…", "data": { "pipeline": {…}, "agents": […] } }

// Pong response
{ "type": "pong", "ts": "…" }

// Acknowledge task submission
{ "type": "ack", "data": { "taskId": "uuid" } }

// Error
{ "type": "error", "data": { "message": "…" } }
```

### Client → Server commands

```jsonc
// Ping
{ "cmd": "ping" }

// Request full snapshot
{ "cmd": "snapshot" }

// Submit a task from dashboard
{ "cmd": "submit", "task": { "type": "content-generator", "payload": {…} } }
```

### Event catalogue

| Event | Payload |
|---|---|
| `pipeline:started` | `{ at }` |
| `pipeline:stopped` | `{ at }` |
| `pipeline:poll` | `{ pendingCount, assignedCount, deadCount, inFlight }` |
| `pipeline:task:dispatched` | `{ task, agent }` |
| `pipeline:task:completed` | `{ task, result }` |
| `pipeline:task:failed` | `{ task, error, attempt }` |
| `pipeline:task:dead` | `{ task }` |
| `pipeline:no-agents` | `{ task }` |
| `pipeline:error` | `{ error, stack? }` |
| `queue:task:enqueued` | `{ task }` |
| `queue:task:retry-scheduled` | `{ task, delay, attempt }` |
| `queue:task:retry-ready` | `{ task, was }` |
| `queue:task:dead` | `{ task }` |
| `agent:registered` | registry event |
| `agent:heartbeat` | registry event |
| `agent:stale` | registry event |
| `agent:dead` | registry event |

---

## REST API — `/pipeline`

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/pipeline/status` | Running state, queue stats, WS info |
| `GET`  | `/pipeline/tasks` | All tasks (filterable by `?status=` `?type=`) |
| `GET`  | `/pipeline/tasks/:id` | Single task by ID |
| `POST` | `/pipeline/tasks` | Submit new task `{ type, payload, priority, maxRetries, meta }` |
| `POST` | `/pipeline/start` | Start the pipeline |
| `POST` | `/pipeline/stop` | Stop the pipeline |
| `GET`  | `/pipeline/ws-info` | WebSocket path + availability |

### Submit task example

```bash
curl -X POST http://localhost:3000/pipeline/tasks \
  -H 'Content-Type: application/json' \
  -d '{ "type": "content-generator", "payload": { "topic": "AI revenue" }, "priority": 5 }'
```

---

## Agent Dispatcher — matching strategy

1. **HTTP endpoint**: if the registry agent record has `httpEndpoint`, POST the task to `{endpoint}/task`
2. **stdio process**: if the agent `type` matches a known runner in `AGENT_RUNNERS`, spawn it as a child process (task JSON via stdin)
3. **Simulated**: graceful fallback for dev/test — resolves with a synthetic result

Capability matching (best-fit selection):

```
score = agent.capabilities.includes(task.type)  →  specialist selected
      | first healthy active agent               →  fallback
      | null                                     →  no-agents event fired
```

---

## Integration (agent-x-core/index.js)

```js
const { mountPipeline } = require('./pipeline');

const { pipeline, wsServer, router } = mountPipeline({
  app,
  httpServer: server,     // http.Server wrapping Express
  registry,               // agent registry instance
  bus,                    // shared EventEmitter
  pollMs:    2_000,       // poll interval (default)
  autoStart: true,        // start immediately
});

app.use('/pipeline', router);
```

---

## Running Tests

```bash
cd agent-x-core
npm test
# or
node --test pipeline/pipeline.test.js
```

Test coverage:
- `TaskQueue`: enqueue, priority ordering, assign, complete, fail, retry backoff, dead-letter, event emissions
- `HermesPipeline`: construction validation, task lifecycle, successful dispatch, retry-to-dead, no-agent path, external job ingestion
- `pipeline-api`: all REST endpoints via direct router invocation (no HTTP overhead)
