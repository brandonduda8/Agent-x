# Agent X — Project Context Document

## Project Overview

Agent X is an **autonomous income infrastructure** system designed to operate as a self-directed, multi-agent platform for generating revenue through automated content creation, data aggregation, product publishing, and service orchestration. The system runs persistently, executes tasks without manual intervention, and integrates with external services like Stripe for payments and webhooks for event-driven workflows.

The project targets deployment on both **Termux (Android)** and **standard Linux environments**, with Docker support for containerized production deployments.

---

## Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────────┐
│                        Agent X System                        │
│                                                             │
│  ┌──────────────────┐        ┌──────────────────────────┐  │
│  │  agent-x-core    │◄──────►│      digital-twin        │  │
│  │  (Command Center)│        │   (Execution Layer)      │  │
│  │  Port: 3000      │        │   Port: 3001             │  │
│  └────────┬─────────┘        └──────────────────────────┘  │
│           │                                                  │
│  ┌────────▼──────────────────────────────────────────────┐  │
│  │              Agent Registry & Heartbeat System         │  │
│  │  registry.js │ heartbeat.js │ registry-api.js         │  │
│  └────────┬──────────────────────────────────────────────┘  │
│           │                                                  │
│  ┌────────▼──────────────────────────────────────────────┐  │
│  │           Agent Upgrade & Config Versioning Layer      │  │
│  │  upgrade-manager.js │ config-version-store.js         │  │
│  │  upgrade-api.js     │ config-schema-validator.js      │  │
│  └────────┬──────────────────────────────────────────────┘  │
│           │                                                  │
│  ┌────────▼──────────────────────────────────────────────┐  │
│  │                  Worker Agents (stdio/JSON)            │  │
│  │  api-socket │ content-generator │ data-aggregator     │  │
│  │  infrastructure │ orchestrator │ publisher            │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  dashboard  │  │  webhooks   │  │  stripe-catalog     │ │
│  │  (Flask/    │  │  listener   │  │  (Payment Layer)    │ │
│  │  SocketIO)  │  │  (Node.js)  │  │                     │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Layer Breakdown

| Layer | Directory | Role |
|---|---|---|
| Command Center | `agent-x-core/` | Express API, task routing, agent orchestration |
| Execution Layer | `digital-twin/` | Pipeline runners, artifact generation |
| Worker Agents | `agent-x-core/agents/` | Standalone stdio JSON processes |
| Agent Registry | `agent-x-core/registry/` | Agent registration, heartbeat tracking, health monitoring |
| Upgrade & Versioning | `agent-x-core/upgrade/` | Agent upgrade management, config versioning, schema validation |
| Python Core | `core/` | Brain, state management, supervisor, LLM client |
| Agent Modules | `agents/` | Python-based builder, planner, researcher, revenue agents |
| Dashboard | `dashboard/` | Flask + SocketIO real-time monitoring UI |
| Products | `products/` | Product factory, catalog, publishing, order management |
| Blueprints | `blueprints/` | Reusable revenue module templates |
| Communication | `communication/` | Shared inter-service packet schema |
| Execution | `execution/` | Stripe integration, webhook handling |
| Deployment | `deployment/` | Dockerfile, systemd service files, Termux boot scripts |

---

## Key Files

### Entry Points

| File | Purpose |
|---|---|
| `agent-x-core/index.js` | Main command center server (Express, Port 3000) |
| `digital-twin/index.js` | Execution layer server (Express, Port 3001) |
| `dashboard/app.py` | Real-time Flask dashboard with SocketIO |
| `app.py` | Standalone sentiment analysis demo (HuggingFace Transformers) |
| `run.js` | Top-level JS runner |
| `run.py` | Top-level Python runner |

### Agent Registry & Heartbeat System (`agent-x-core/registry/`)

| File | Purpose |
|---|---|
| `registry.js` | Core agent registry — stores agent metadata, tracks registration/deregistration, manages agent state map |
| `heartbeat.js` | Heartbeat monitor — periodically checks agent liveness, marks agents as `dead`/`stale` when heartbeats are missed, triggers restart callbacks |
| `registry-api.js` | Express router exposing registry REST endpoints (`GET /agents`, `POST /agents/register`, `POST /agents/:id/heartbeat`, `DELETE /agents/:id`) |

### Agent Upgrade & Configuration Versioning (`agent-x-core/upgrade/`)

| File | Purpose |
|---|---|
| `upgrade-manager.js` | Core upgrade orchestrator — manages agent upgrade lifecycle, coordinates version transitions, triggers rollback on failure |
| `config-version-store.js` | Versioned configuration store — persists config snapshots with version numbers, supports diff and rollback to any prior version |
| `upgrade-api.js` | Express router exposing upgrade/config REST endpoints (see Upgrade API section below) |
| `config-schema-validator.js` | JSON Schema validation for agent configurations — enforces schema correctness before applying config versions |

### Core Worker Agents (`agent-x-core/agents/`)

| File | Purpose |
|---|---|
| `orchestrator.js` | Coordinates agent task routing and execution |
| `api-socket.js` | Outbound HTTP GET/POST with headers and timeout control |
| `content-generator.js` | Drafts copy, posts, emails for monetization |
| `data-aggregator.js` | Fetches datasets, summarizes health, returns artifacts |
| `infrastructure.js` | Service lifecycle, env sanity checks, network probes |
| `publisher.js` | Publishes content/products to external destinations |
| `watchdog.js` | Monitors agent health and triggers restarts |
| `status-saver.py` | Persists agent status to disk |
| `orchestrator.run.py` | Python wrapper to launch orchestrator |
| `Status.cli.py` | CLI tool for viewing agent status |

### Python Core Layer (`core/`)

| File | Purpose |
|---|---|
| `brain.js` | JS-side brain/decision logic |
| `intelligence_brain.py` | Python AI decision engine |
| `revenue_brain.py` | Revenue-focused decision logic |
| `revenue_engine.py` | Revenue execution and optimization |
| `supervisor.py` | Agent supervision and lifecycle management |
| `state_manager.py` | Persistent state read/write |
| `task_registry.py` | Task registration and lookup |
| `loop_engine.py` | Autonomous execution loop |
| `llm_client.py` | LLM API client abstraction |
| `event_bus.py` | Python-side pub/sub event system |
| `hub_bridge.py` | Bridge between Python and Node.js layers |

### Python Agent Modules (`agents/`)

| File | Purpose |
|---|---|
| `builder/builder_agent.py` | Builds projects and artifacts |
| `planner/planner_agent.py` | Plans tasks and roadmaps |
| `researcher/researcher_agent.py` | Researches topics and data |
| `revenue/revenue_agent.py` | Revenue generation strategies |
| `titan_architect.md` | Architecture blueprint document |

### Products Layer (`products/`)

| File | Purpose |
|---|---|
| `product-factory.py` | Generates product definitions |
| `product-orchestrator.py` | Coordinates product lifecycle |
| `product-publisher.py` | Publishes products to storefront |
| `batch-generate.py` | Batch product generation |
| `order-manifest.py` | Manages order records |
| `catalog/catalog.json` | Product catalog data |
| `storefront.html` | Frontend storefront UI |

### Infrastructure & Deployment

| File | Purpose |
|---|---|
| `deployment/Dockerfile` | Multi-service Docker image (Node 20 Alpine) |
| `docker-compose.yml` | Orchestrates agent-x-core + digital-twin services |
| `deployment/agent-x-core.service` | systemd service for core |
| `deployment/digital-twin.service` | systemd service for digital-twin |
| `deployment/termux-boot.sh` | Auto-start script for Termux |

### Data & Memory

| File | Purpose |
|---|---|
| `memory/brain.json` | Persistent AI brain state |
| `memory/state.json` | System state snapshot |
| `memory/tasks.json` | Queued/completed task records |
| `memory/registry.json` | Persisted agent registry snapshot (written by registry.js) |
| `memory/config-versions/` | Directory of versioned config snapshots (written by config-version-store.js) |
| `data/db.json` | General database (JSON flat file) |
| `data/tasks.json` | Task definitions |
| `data/revenue.json` | Revenue tracking data |
| `data/schema.sql` | SQL schema reference |
| `config/settings.yaml` | Central configuration |

---

## Tech Stack

### Node.js (Primary Runtime)

| Package | Version | Usage |
|---|---|---|
| `express` | ^5.2.1 | HTTP API server (both agent-x-core and digital-twin) |
| `axios` | ^1.17.0 | HTTP client for outbound requests |
| `cors` | ^2.8.6 | Cross-origin resource sharing |
| `dotenv` | ^17.4.2 | Environment variable management |
| `uuid` | ^14.0.0 | Unique ID generation for tasks/requests |
| `stripe` | ^22.2.1 | Payment processing |
| `jsonwebtoken` | ^9.0.3 | JWT authentication |
| `bcryptjs` | ^3.0.3 | Password hashing |
| `lowdb` | ^7.0.1 | JSON flat-file database |
| `nodemon` | ^3.1.14 | Development hot-reload |
| `pm2` | ^5.3.0 | Production process manager |
| `node-fetch` | ^3.3.2 | Optional fetch for communication layer |
| `ajv` | latest | JSON Schema validation (used by config-schema-validator.js) |

### Python (Secondary Runtime)

| Library | Usage |
|---|---|
| `flask` | Dashboard HTTP server |
| `flask-socketio` | Real-time WebSocket streaming |
| `transformers` | HuggingFace LLM/NLP pipeline |
| Standard Library | `os`, `sys`, `json` for state/file management |

### Infrastructure

| Technology | Usage |
|---|---|
| Docker / Docker Compose | Containerized deployment |
| Node 20 Alpine | Docker base image |
| systemd | Linux service management |
| Termux | Android-native deployment |

---

## Agent Registry & Heartbeat System

### Overview

The Agent Registry provides a centralized catalog of all active agents with real-time liveness tracking via periodic heartbeats. It is a core subsystem of `agent-x-core`, exposed via REST API and integrated with the orchestrator and watchdog.

### Agent Lifecycle States

```
REGISTERED → ACTIVE → STALE → DEAD
                ↑         │
                └─────────┘  (re-heartbeat recovers to ACTIVE)
```

| State | Meaning |
|---|---|
| `registered` | Agent has registered but not yet sent a heartbeat |
| `active` | Agent is sending heartbeats within the expected interval |
| `stale` | Agent missed heartbeat window but has not exceeded dead threshold |
| `dead` | Agent has exceeded the dead threshold; restart callback triggered |

### Agent Registration Schema

```json
{
  "id": "uuid-v4",
  "name": "content-generator",
  "type": "worker",
  "capabilities": ["draft", "email", "post"],
  "status": "active",
  "registeredAt": "ISO8601",
  "lastHeartbeat": "ISO8601",
  "missedHeartbeats": 0,
  "meta": {}
}
```

### Registry REST API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/agents` | List all registered agents and their status |
| `POST` | `/agents/register` | Register a new agent (returns assigned ID) |
| `POST` | `/agents/:id/heartbeat` | Record a heartbeat for the specified agent |
| `DELETE` | `/agents/:id` | Deregister an agent |

### Heartbeat Configuration

| Setting | Default | Description |
|---|---|---|
| `HEARTBEAT_INTERVAL_MS` | `15000` | How often agents should send heartbeats (15s) |
| `STALE_THRESHOLD_MS` | `30000` | Time without heartbeat before marked `stale` (30s) |
| `DEAD_THRESHOLD_MS` | `60000` | Time without heartbeat before marked `dead` (60s) |

All thresholds are configurable via environment variables.

### Integration Points

- **`watchdog.js`** — subscribes to `dead` agent events from `heartbeat.js` to trigger restarts
- **`orchestrator.js`** — queries registry before routing tasks to ensure target agent is `active`
- **`registry-api.js`** — mounted on `agent-x-core` Express app (e.g., `/v1/registry`)
- **`memory/registry.json`** — registry state is persisted to disk for recovery after restarts

---

## Agent Upgrade & Configuration Versioning System

### Overview

The Upgrade & Configuration Versioning system provides controlled, auditable agent upgrades with full config history, schema validation, and rollback support. It is mounted on `agent-x-core` and integrates with the registry to gate upgrades against agent liveness state.

### Upgrade Lifecycle

```
PENDING → IN_PROGRESS → COMPLETE
                │
                └──► FAILED → ROLLED_BACK
```

| State | Meaning |
|---|---|
| `pending` | Upgrade requested but not yet started |
| `in_progress` | Upgrade is actively being applied |
| `complete` | Upgrade applied successfully |
| `failed` | Upgrade encountered an error |
| `rolled_back` | Automatic or manual rollback to prior version applied |

### Config Version Schema

```json
{
  "agentId": "uuid-v4",
  "version": 3,
  "config": { ... },
  "schema": "agent-config-v1",
  "appliedAt": "ISO8601",
  "appliedBy": "upgrade-manager",
  "changelog": "Description of what changed",
  "previousVersion": 2
}
```

### Upgrade API (`/v1/upgrade`)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/agents/:id/upgrade` | Initiate an upgrade for a specific agent |
| `GET` | `/agents/:id/upgrade/status` | Get current upgrade status for an agent |
| `POST` | `/agents/:id/upgrade/rollback` | Roll back agent to previous config version |
| `GET` | `/agents/:id/config/versions` | List all config versions for an agent |
| `GET` | `/agents/:id/config/versions/:version` | Retrieve a specific config version snapshot |
| `POST` | `/agents/:id/config` | Apply a new config version (with schema validation) |
| `GET`