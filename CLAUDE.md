# Agent X — CLAUDE.md
## Developer & AI-Agent Quick-Reference

---

## Essential Commands

```bash
# Install dependencies
cd agent-x-core && npm install
cd digital-twin  && npm install

# Start command center (port 3000)
cd agent-x-core && node index.js

# Start execution layer (port 3001)
cd digital-twin && node index.js

# Start Python dashboard (port 5000 by default)
cd dashboard && python app.py

# Run agent registry smoke tests (zero extra deps)
node agent-x-core/registry/registry.test.js

# Syntax-check a JS agent
node --check agent-x-core/agents/content-generator.js

# One-shot agent test
printf '%s' '{"action":"draft","requestId":"t1","payload":{"topic":"AI","audience":"devs","variant":"short"}}' \
  | node agent-x-core/agents/content-generator.js
```

---

## Architecture Overview

```
agent-x-core (port 3000)          digital-twin (port 3001)
├── index.js                       └── index.js
├── routes/
│   └── agents.js    ←── /api/agents REST endpoints
└── registry/
    ├── agent-registry.js   ←── CRUD + heartbeat logic
    ├── heartbeat-monitor.js ←── 30-second periodic stale check
    └── registry.test.js    ←── self-contained smoke tests
```

---

## Agent Registry & Heartbeat System

### Overview
The Agent Registry tracks every running agent (name, type, capabilities,
status, current task).  A background HeartbeatMonitor runs every
`HEARTBEAT_INTERVAL_MS` (default **30 s**) and demotes agents that haven't
pinged within `HEARTBEAT_STALE_MS` (default **60 s**) to `"stale"`.

### Agent Status Lifecycle
```
  [registered]
       │
       ▼
    "idle"  ◄──── heartbeat (no status payload)
       │
       ├──► "active"   (agent signals it picked up a task)
       │        │
       │        └──► "idle"  (task complete)
       │
       ├──► "stale"    (missed 60 s heartbeat window — set by monitor)
       │        │
       │        └──► "idle"  (revived on next heartbeat)
       │
       └──► "offline"  (manually set; monitor does NOT touch offline agents)
```

### REST Endpoints (`/api/agents`)

| Method | Path | Description |
|--------|------|-------------|
| `GET`    | `/api/agents`                    | List all agents (optional `?status=` `?type=`) |
| `POST`   | `/api/agents`                    | Register a new agent |
| `GET`    | `/api/agents/:id`                | Get single agent |
| `PATCH`  | `/api/agents/:id`                | Partial update |
| `DELETE` | `/api/agents/:id`                | Remove agent |
| `POST`   | `/api/agents/:id/heartbeat`      | Record liveness ping |
| `GET`    | `/api/agents/heartbeat/summary`  | Registry-wide status counts |

### Request / Response Envelope
All responses use the project's standard shape:
```json
{ "ok": true,  "data": { ... } }
{ "ok": false, "error": "...", "errors": ["optional", "array"] }
```

### Register an Agent
```bash
curl -s -X POST http://localhost:3000/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "content-generator-1",
    "type": "worker",
    "capabilities": ["draft", "email", "social"],
    "status": "idle"
  }' | jq .
```

### Send a Heartbeat
```bash
# Replace <id> with the UUID returned from POST /api/agents
curl -s -X POST http://localhost:3000/api/agents/<id>/heartbeat \
  -H "Content-Type: application/json" \
  -d '{ "status": "active", "current_task_id": "task-abc123" }' | jq .
```

### List Active Agents
```bash
curl -s "http://localhost:3000/api/agents?status=active" | jq .data.agents
```

### Registry Summary
```bash
curl -s http://localhost:3000/api/agents/heartbeat/summary | jq .data
```

### Environment Variables (heartbeat tuning)
| Variable | Default | Description |
|---|---|---|
| `HEARTBEAT_INTERVAL_MS` | `30000` | How often the monitor runs (ms) |
| `HEARTBEAT_STALE_MS`    | `60000` | Age of last heartbeat before "stale" (ms) |

---

## Module System

- **Node.js:** CommonJS (`require` / `module.exports`) — `"type": "commonjs"` in `agent-x-core/package.json`
- **Python:** Standard packages with `__init__.py` in each sub-directory

## Key Coding Conventions

- Filenames: `kebab-case.js` for Node, `snake_case.py` for Python
- All inter-service responses: `{ ok: true/false, data/error: ... }`
- Unique IDs: `uuid` package (`uuidv4()`)
- Persistence: JSON flat-files in `data/`, `memory/`, `generated/`
- No hardcoded secrets — always `process.env.VAR` / `os.getenv('VAR')`
- Worker agents: self-contained stdio JSON processes (read line → write JSON → exit)

## Port Map
| Service | Port |
|---|---|
| agent-x-core | 3000 |
| digital-twin | 3001 |
| dashboard | 5000 (or `PORT` env) |

## Data Files
| File | Purpose |
|---|---|
| `data/agents.json`   | Agent registry store (managed by agent-registry.js) |
| `data/db.json`       | General flat-file database |
| `data/revenue.json`  | Revenue tracking |
| `memory/state.json`  | System state snapshot |
| `memory/brain.json`  | AI brain state |
| `memory/tasks.json`  | Task queue |
| `data/schema.sql`    | Canonical SQL schema reference |
