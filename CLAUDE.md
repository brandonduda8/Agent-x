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
│  │           Agent Hermes Job Discovery & Matching        │  │
│  │  hermes-client.js │ job-matcher.js │ hermes-api.js    │  │
│  │  job-schema.js    │ hermes-event-bridge.js            │  │
│  └────────┬──────────────────────────────────────────────┘  │
│           │                                                  │
│  ┌────────▼──────────────────────────────────────────────┐  │
│  │                  Worker Agents (stdio/JSON)            │  │
│  │  api-socket │ content-generator │ data-aggregator     │  │
│  │  infrastructure │ orchestrator │ publisher            │  │
│  └────────┬──────────────────────────────────────────────┘  │
│           │                                                  │
│  ┌────────▼──────────────────────────────────────────────┐  │
│  │              Zangi Communication Layer                 │  │
│  │  zangi-client.js │ zangi-router.js │ zangi-api.js     │  │
│  │  zangi-message-schema.js │ zangi-event-bridge.js      │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  dashboard  │  │  webhooks   │  │  stripe-catalog     │ │
│  │  (Flask/    │  │  listener   │  │  (Payment Layer)    │ │
│  │  SocketIO)  │  │  (Node.js)  │  │                     │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           Autonomous Build Pipeline                  │   │
│  │  build-pipeline.js │ build-monitor.js               │   │
│  │  build-api.js      │ build-schema.js                │   │
│  │  build-event-bridge.js                              │   │
│  └─────────────────────────────────────────────────────┘   │
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
| Hermes Job Discovery | `agent-x-core/hermes/` | Job discovery, capability-based matching, opportunity intake |
| Zangi Communication | `agent-x-core/zangi/` | Inter-agent and external messaging via Zangi protocol |
| Autonomous Build Pipeline | `agent-x-core/build/` | Self-directed build orchestration, real-time monitoring, build event streaming |
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

### Agent Hermes Job Discovery & Matching (`agent-x-core/hermes/`)

| File | Purpose |
|---|---|
| `hermes-client.js` | Core Hermes protocol client — manages connection lifecycle, authentication, and job feed polling from external job/opportunity sources |
| `job-matcher.js` | Capability-based job matching engine — scores and ranks discovered jobs against registered agent capabilities, filters by configurable criteria |
| `hermes-api.js` | Express router exposing Hermes REST endpoints for querying discovered jobs, triggering match runs, and managing job intake |
| `job-schema.js` | JSON Schema definitions and validation for job/opportunity envelopes — enforces structure before ingestion and matching |
| `hermes-event-bridge.js` | Bridges Hermes job discovery events into the internal agent event bus, enabling agents to react to newly matched opportunities |

### Zangi Communication Layer (`agent-x-core/zangi/`)

| File | Purpose |
|---|---|
| `zangi-client.js` | Core Zangi protocol client — manages connection lifecycle, authentication, and message dispatch to Zangi endpoints |
| `zangi-router.js` | Routes inbound Zangi messages to registered agent handlers based on message type and target |
| `zangi-api.js` | Express router exposing Zangi REST endpoints for sending messages, querying channel status, and managing subscriptions |
| `zangi-message-schema.js` | JSON Schema definitions and validation for Zangi message envelopes — enforces structure before send/receive |
| `zangi-event-bridge.js` | Bridges Zangi inbound events into the internal agent event bus, enabling agents to react to external Zangi messages |

### Autonomous Build Pipeline (`agent-x-core/build/`)

| File | Purpose |
|---|---|
| `build-pipeline.js` | Core autonomous build orchestrator — manages build lifecycle, step execution, dependency resolution, artifact tracking, and automatic retry/rollback on failure |
| `build-monitor.js` | Real-time build monitor — tracks step-level progress, collects metrics (duration, success rate, artifact counts), emits live status events |
| `build-api.js` | Express router exposing build REST endpoints — trigger builds, query status, retrieve logs, manage build history |
| `build-schema.js` | JSON Schema definitions and validation for build job envelopes, step definitions, and artifact manifests |
| `build-event-bridge.js` | Bridges build pipeline events into the internal agent event bus, enabling agents and the dashboard to react to build state changes in real time |

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
| `llm_client.py` | LLM API client abstraction with multi-provider fallback chain — attempts providers in priority order, falls back automatically on failure or unavailability |
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
| `memory/zangi-channels.json` | Persisted Zangi channel subscriptions and connection state |
| `memory/hermes-jobs.json` | Persisted discovered job records and match scores (written by job-matcher.js) |
| `memory/build-history.json` | Persisted build run records, step logs, artifact manifests, and outcome metrics (written by build-pipeline.js) |
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
| `ajv` | latest | JSON Schema validation (used by config-schema-validator.js, zangi-message-schema.js, job-schema.js, and build-schema.js) |

### Python (Secondary Runtime)

| Library | Usage |
|---|---|
| `flask` | Dashboard HTTP server |