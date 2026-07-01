# Agent X — Project Context Document

## Project Overview

Agent X is an **autonomous income infrastructure** system designed to run AI-powered agents that generate revenue through content creation, data aggregation, product publishing, and Stripe-based commerce. The system is built to operate continuously (including on mobile via Termux), orchestrate multiple specialized agents, and expose dashboards and APIs for monitoring and control.

The project blends a **Node.js microservices core** with a **Python intelligence/dashboard layer**, connected through shared memory files, JSON messaging, and HTTP APIs.

---

## Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────┐
│                   Agent X System                    │
│                                                     │
│  ┌───────────────┐      ┌──────────────────────┐   │
│  │ agent-x-core  │◄────►│    digital-twin      │   │
│  │  (Node.js)    │      │    (Node.js)         │   │
│  │  Port: 3000   │      │    Port: 3001        │   │
│  └───────┬───────┘      └──────────────────────┘   │
│          │                                          │
│  ┌───────▼───────────────────────────────────────┐ │
│  │              Worker Agents (stdio JSON)        │ │
│  │  api-socket │ content-generator │ data-agg... │ │
│  └───────────────────────────────────────────────┘ │
│                                                     │
│  ┌────────────────┐     ┌──────────────────────┐   │
│  │ Python Layer   │     │  Dashboard (Flask)   │   │
│  │ core/*.py      │     │  dashboard/app.py    │   │
│  │ agents/*.py    │     │  Port: 3001          │   │
│  └────────────────┘     └──────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### Service Breakdown

| Service | Runtime | Port | Role |
|---|---|---|---|
| `agent-x-core` | Node.js | 3000 | Command center, task API, orchestrator |
| `digital-twin` | Node.js | 3001 | Execution layer, pipelines, artifacts |
| `dashboard` | Python/Flask | 3001* | Real-time UI via SocketIO |
| `communication` | Node.js | — | Shared packet schema + sender |
| `webhook-listener` | Node.js | — | Stripe/external webhook ingestion |
| `stripe-catalog` | Node.js | — | Product catalog + Stripe integration |

> *Dashboard may conflict with digital-twin on port 3001 — check `PORT` env var.

---

## Termux Compatibility

The system is explicitly designed to run on **Android via Termux**. A dedicated audit and compatibility pass has been completed. Key patterns and constraints:

### Termux-Specific Constraints
- **No `systemd`**: Termux does not support systemd. Service management uses PM2 (Node.js) or manual process supervision scripts instead.
- **No `docker`**: Docker is not available in Termux. All services run as native processes.
- **Home directory**: Termux home is `/data/data/com.termux/files/home` — all hardcoded paths must use `$HOME` or dynamic resolution, never `/root` or `/home/user`.
- **Package manager**: `pkg` (not `apt`) is the Termux package manager. Install scripts must use `pkg install` for system dependencies.
- **Python binary**: May be `python` or `python3` depending on Termux version — scripts should detect or default to `python3`.
- **Node binary**: Available via `pkg install nodejs`.
- **Foreground services**: Long-running processes should use `termux-wake-lock` to prevent Android from killing them.
- **Storage permissions**: File I/O outside Termux home requires `termux-setup-storage`.

### Termux Bootstrap / Startup
- **`deployment/termux-boot.sh`**: Auto-start script for Termux:Boot addon — launches all services on device boot.
- Scripts must be POSIX-compatible (`#!/bin/sh` or `#!/bin/bash` with bash verified available).
- Avoid GNU-specific flags not present in Termux's busybox utilities.

### Termux-Safe Scripting Patterns
```bash
# Use $HOME not hardcoded paths
cd "$HOME/agent-x"

# Detect python
PYTHON=$(command -v python3 || command -v python)

# Use pkg for installs in setup scripts
pkg install nodejs python -y

# Wake lock for long-running agents
termux-wake-lock
node agent-x-core/index.js &
```

### Process Management on Termux
- **PM2** is the preferred process manager for Node.js services on Termux.
- Python agents can be managed via `process-manager.py` or launched directly with `nohup`.
- No systemd `.service` files are used in Termux deployments (those exist only for Linux server deployments).

---

## Repository Structure

```
agent-x/
│
├── agent-x-core/               # Primary command center (Node.js + Express)
│   ├── index.js                # Entry point — Express API server
│   ├── tasks.json              # Task queue/definitions
│   ├── package.json            # Dependencies: axios, cors, dotenv, express, uuid
│   └── agents/                 # Worker agents (stdio JSON processes)
│       ├── api-socket.js       # Outbound HTTP GET/POST agent
│       ├── content-generator.js# Copy/post/email drafting agent
│       ├── data-aggregator.js  # Dataset fetch + summarize agent
│       ├── infrastructure.js   # Service lifecycle + env checks
│       ├── orchestrator.js     # Coordinates agent execution
│       ├── orchestrator.run.py # Python orchestrator runner
│       ├── publisher.js        # Content publishing agent
│       ├── watchdog.js         # Process health monitor
│       ├── status-saver.py     # Writes status to disk
│       ├── Status.cli.py       # CLI status viewer
│       └── run_one.py          # Single agent launcher
│
├── agent-x-core/Status.show.py # Status display utility
│
├── digital-twin/               # Execution layer
│   └── index.js                # Pipeline runner + artifact manager
│
├── communication/              # Shared messaging layer
│   ├── packet-schema.js        # JSON envelope schema
│   └── package.json
│
├── blueprints/                 # Reusable revenue modules
│   ├── content-pipeline/       # Blog/copy generation pipeline
│   │   └── runner.js
│   └── data-aggregator/        # HTTP data collection pipeline
│       └── runner.js
│
├── core/                       # Python intelligence core
│   ├── agent.js                # JS agent base
│   ├── brain.js                # JS brain logic
│   ├── intelligence_brain.py   # Python AI brain
│   ├── revenue_brain.py        # Revenue logic
│   ├── revenue_engine.py       # Revenue execution
│   ├── loop_engine.py          # Continuous loop control
│   ├── llm_client.py           # LLM API abstraction
│   ├── supervisor.py           # Agent supervision
│   ├── state_manager.py        # Global state management
│   ├── task_registry.py        # Task registration + listing
│   ├── event_bus.py            # Python event pub/sub
│   ├── hub_bridge.py           # Cross-service bridge
│   ├── database.js             # JS data layer
│   └── db.js                   # JS DB helpers
│
├── agents/                     # Python agent definitions
│   ├── builder/
│   │   └── builder_agent.py    # Build/code generation agent
│   ├── planner/
│   │   └── planner_agent.py    # Task planning agent
│   ├── researcher/
│   │   └── researcher_agent.py # Research/data gathering agent
│   ├── revenue/
│   │   └── revenue_agent.py    # Revenue generation agent
│   ├── builder_agent.py        # Flat builder agent (alt)
│   ├── planner_agent.py        # Flat planner agent (alt)
│   ├── dev-agent.js            # JS dev agent
│   └── titan_architect.md      # Architecture notes
│
├── dashboard/                  # Flask real-time dashboard
│   ├── app.py                  # Flask + SocketIO server
│   └── templates/
│       └── index.html          # Dashboard UI
│
├── products/                   # Product catalog & generation
│   ├── product-factory.py      # Product creation
│   ├── product-orchestrator.py # Product pipeline coordinator
│   ├── product-publisher.py    # Publishes to Stripe
│   ├── batch-generate.py       # Bulk product generation
│   ├── order-manifest.py       # Order tracking
│   ├── index.js                # Products JS entry
│   ├── storefront.html         # Storefront UI
│   └── catalog/
│       └── catalog.json        # Product catalog data
│
├── execution/                  # Revenue execution layer
│   ├── server.js               # Execution HTTP server
│   ├── stripe.js               # Stripe payment integration
│   └── webhook.js              # Webhook handlers
│
├── stripe-catalog/             # Stripe product catalog
│   ├── index.js
│   └── config.json
│
├── generated/                  # AI-generated artifacts (auto-created)
│   ├── asset-*.json
│   ├── build-*.json
│   ├── product-*.json
│   └── run_*.json
│
├── products/deliverables/      # Generated product files
│   └── prod_*.json             # Individual product deliverables
│
├── memory/                     # Persistent agent memory
│   ├── brain.json              # Brain state
│   ├── state.json              # System state
│   └── tasks.json              # Active tasks
│
├── data/                       # Structured data storage
│   ├── db.json                 # Main database
│   ├── projects.json           # Project records
│   ├── revenue.json            # Revenue tracking
│   ├── schema.sql              # DB schema
│   └── tasks.json              # Task data
│
├── deployment/                 # Deployment manifests
│   ├── Dockerfile              # Docker image (node:20-alpine) — server only
│   ├── docker-compose.yml      # Multi-service compose — server only
│   ├── agent-x-core.service    # systemd service — Linux server only
│   ├── digital-twin.service    # systemd service — Linux server only
│   └── termux-boot.sh          # Termux auto-start (Termux:Boot addon)
│
├── tools/                      # Python tool modules
│   ├── code_tools.py           # Code generation tools
│   └── deployment_tools.py     # Deployment helpers
│
├── integrations/               # External service adapters
│   └── pure_graph_adapter.py   # Graph/workflow integration
│
├── overmind/index.js           # Top-level orchestration controller
├── hermes/router.js            # Internal message router
├── engine/orchestrator.js      # Alternate orchestrator
├── income_squad/index.js       # Income-focused agent squad
├── titan-core/                 # Titan architecture core
│   ├── config.js
│   └── master.js
│
├── config/settings.yaml        # Global configuration
├── memory.json                 # Root-level memory file
├── app.py                      # Standalone NLP/sentiment demo
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Root compose file (server deployments)
├── run.py                      # Python launch script
├── run.js                      # JS launch script
├── auto-publish.js             # Auto-publishing trigger
├── auto-publish.py             # Auto-publishing (Python)
├── process-manager.py          # Python process manager
├── setup_agents.sh             # Agent setup script (Termux-compatible)
├── upgrade_agents.sh           # Agent upgrade script (Termux-compatible)
└── strategy.md                 # Revenue/product strategy notes
```

---

## Tech Stack

### JavaScript / Node.js
| Package | Version | Purpose |
|---|---|---|
| `express` | ^5.2.1 | HTTP API server |
| `axios` | ^1.17.0 | Outbound HTTP requests |
| `cors` | ^2.8.6 | CORS middleware |
| `dotenv` | ^17.4.2 | Environment variable loading |
| `uuid` | ^14.0.0 | Request/artifact/task ID generation |
| `stripe` | ^22.2.1 | Payment processing |
| `jsonwebtoken` | ^9.0.3 | Auth tokens |
| `bcryptjs` | ^3.0.3 | Password hashing |
| `lowdb` | ^7.0.1 | Lightweight JSON database |
| `nodemon` | ^3.1.14 | Dev file watching |
| `pm2` | ^5.3.0 | Process management (server + Termux) |
| `node-fetch` | ^3.3.2 | Fetch API (optional, communication) |

### Python
| Package | Purpose |
|---|---|
| `flask` | Dashboard HTTP server |
| `flask-socketio` | Real-time WebSocket events |
| `transformers` | HuggingFace NLP/LLM pipelines |
| `requests` (implied) | HTTP calls from Python agents |

### Infrastructure
- **Docker**: `node:20-alpine` base image — **Linux server deployments only**
- **docker-compose**: Multi-service orchestration — **Linux server deployments only**
- **systemd**: Linux service management — **Linux server deployments only**
- **Termux**: Android/mobile deployment target — uses PM2 + `termux-boot.sh`, no Docker/systemd
- **PM2**: Node.js process manager — used in both server and Termux deployments

---

## Key Files Reference

| File | Purpose |
|---|---|
| `agent-x-core/index.js` | Main Express server — task submission entry point |
| `agent-x-core/agents/orchestrator.js` | Routes tasks to worker agents |
| `agent-x-core/agents/content-generator.js` | Drafts marketing copy, emails, posts |
| `agent-x-core/agents/data-aggregator.js` | Fetches and summarizes external data |
| `agent-x-core/agents/api-socket.js` | Performs outbound HTTP calls |
| `digital-twin/index.js` | Execution pipeline runner |
| `dashboard/app.py` | Flask + SocketIO dashboard |
| `core/supervisor.py` | Monitors and manages Python agents |
| `core/task_registry.py` | Tracks all tasks and their states |
| `core/state_manager.py` | Global persistent state |
| `core/llm_client.py` | Abstraction over LLM providers |
| `core/loop_engine.py` | Continuous autonomous loop |
| `core/revenue_engine.py` | Revenue generation logic |
| `products/product-factory.py` | Creates product definitions |
| `execution/stripe.js` | Stripe checkout and fulfillment |
| `config/settings.yaml` | Central configuration |
| `memory/state.json` | Live system state |
| `data/db.json` | Primary data store |
| `deployment/Dockerfile` | Container image definition (server only) |
| `deployment/termux-boot.sh` | Termux auto-start on device boot |
| `setup_agents.sh` | Termux-compatible agent setup script |

---

## Agent Communication Protocol

Worker agents in `agent-x-core/agents/` communicate via **stdio JSON envelopes** — one JSON object per line on stdin, one response on stdout.

### Request Envelope
```json
{
  "action": "draft",
  "requestId":