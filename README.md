# Agent X

**Autonomous income infrastructure** — AI-powered agents that generate revenue through content creation, data aggregation, product publishing, and Stripe-based commerce. Runs continuously on Linux servers *and* directly on Android via Termux.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Quick Start — Linux Server](#quick-start--linux-server)
4. [Termux Setup (Android)](#termux-setup-android)
   - [Prerequisites](#prerequisites)
   - [Step-by-step installation](#step-by-step-installation)
   - [Starting services](#starting-services)
   - [Stopping services](#stopping-services)
   - [Viewing logs](#viewing-logs)
   - [Auto-start on device reboot](#auto-start-on-device-reboot)
   - [Known limitations on Termux](#known-limitations-on-termux)
   - [Termux troubleshooting](#termux-troubleshooting)
5. [Configuration](#configuration)
6. [Services Reference](#services-reference)
7. [Agent Communication Protocol](#agent-communication-protocol)
8. [Revenue Modules](#revenue-modules)
9. [Contributing](#contributing)

---

## Overview

Agent X blends a **Node.js microservices core** with a **Python intelligence/dashboard layer**. Agents communicate through stdio JSON envelopes, shared memory files, and HTTP APIs. The system is built to orchestrate specialised agents and expose real-time dashboards for monitoring and control.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Agent X System                    │
│                                                     │
│  ┌───────────────┐      ┌──────────────────────┐   │
│  │ agent-x-core  │◄────►│    digital-twin      │   │
│  │  (Node.js)    │      │    (Node.js)         │   │
│  │  Port: 3000   │      │    Port: 3002        │   │
│  └───────┬───────┘      └──────────────────────┘   │
│          │                                          │
│  ┌───────▼───────────────────────────────────────┐ │
│  │              Worker Agents (stdio JSON)        │ │
│  │  api-socket │ content-generator │ data-agg    │ │
│  └───────────────────────────────────────────────┘ │
│                                                     │
│  ┌────────────────┐     ┌──────────────────────┐   │
│  │ Python Layer   │     │  Dashboard (Flask)   │   │
│  │ core/*.py      │     │  dashboard/app.py    │   │
│  │ agents/*.py    │     │  Port: 5000          │   │
│  └────────────────┘     └──────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

| Service | Runtime | Port | Role |
|---|---|---|---|
| `agent-x-core` | Node.js | 3000 | Command centre, task API, orchestrator |
| `digital-twin` | Node.js | 3002 | Execution layer, pipelines, artifacts |
| `dashboard` | Python/Flask | 5000 | Real-time UI via SocketIO |
| `webhook-listener` | Node.js | 3003 | Stripe/external webhook ingestion |

---

## Quick Start — Linux Server

> Docker and systemd are available on Linux servers only. **Do not use these on Termux** — skip to the [Termux Setup](#termux-setup-android) section instead.

```bash
# 1. Clone
git clone https://github.com/brandonduda8/Agent-x.git
cd Agent-x

# 2. Copy and fill in environment variables
cp .env.example .env
nano .env

# 3. Start all services (Docker Compose)
docker compose up -d

# 4. Check status
docker compose ps
curl http://localhost:3000/health
```

Alternatively, with PM2 directly:

```bash
npm install -g pm2
npm install          # root
(cd agent-x-core && npm install)
(cd digital-twin && npm install)
pm2 start agent-x-core/index.js --name agent-x-core
pm2 start digital-twin/index.js  --name digital-twin
pm2 start dashboard/app.py       --name dashboard --interpreter python3
pm2 save
```

---

## Termux Setup (Android)

Agent X runs fully on Android through [Termux](https://termux.dev). The `termux/` directory contains a complete set of scripts that replace Docker and systemd with PM2-managed native processes.

### Prerequisites

| Requirement | Install |
|---|---|
| **Termux** (F-Droid build) | [f-droid.org/packages/com.termux](https://f-droid.org/en/packages/com.termux/) |
| Android 7.0+ | — |
| ~2 GB free storage | (add ~3 GB more if you enable LLM packages) |
| Internet connection during setup | — |
| **Termux:Boot** *(optional, for auto-start)* | [f-droid.org/packages/com.termux.boot](https://f-droid.org/en/packages/com.termux.boot/) |

> ⚠️ **Use the F-Droid version of Termux**, not the Google Play version. The Play Store build is outdated and lacks package support needed by Agent X.

---

### Step-by-step installation

#### 1 — Clone the repository

```bash
# Inside Termux
pkg install git -y
git clone https://github.com/brandonduda8/Agent-x.git
cd Agent-x
```

#### 2 — Run the bootstrap setup script

```bash
bash termux/setup.sh
```

The script handles everything automatically:

| Step | What it does |
|---|---|
| Sanity check | Verifies you are inside Termux |
| Package index | `pkg update` |
| System packages | Installs `nodejs`, `python`, `git`, `curl`, `jq`, `clang`, and more via `pkg install` |
| npm upgrade | Upgrades npm to latest |
| Global npm tools | Installs `pm2` and `nodemon` globally |
| Python packages | Installs Flask, SocketIO, requests, psutil, stripe, and others via `pip` |
| LLM packages | Installs `transformers`, `tokenizers`, `openai`, `anthropic` *(skippable)* |
| `requirements.txt` | Installs repo-level Python deps |
| Node.js deps | Runs `npm install` in each service directory |
| Runtime dirs | Creates `memory/`, `data/`, `logs/`, `generated/`, etc. |
| State files | Initialises blank JSON state files idempotently |
| `.env` template | Writes a `.env` with all variables pre-populated with paths |
| CLI launcher | Installs an `agent-x` command into `$PREFIX/bin` |
| Termux:Boot hook | Installs auto-start script if Termux:Boot is present |
| Self-test | Verifies all key binaries and Python imports |

**Optional flag — skip heavy LLM packages** (recommended on low-RAM devices):

```bash
bash termux/setup.sh --no-llm
```

This skips `transformers`, `torch`, and related packages, saving ~3 GB of storage and significant install time. You can always install them later:

```bash
pip install transformers sentencepiece accelerate openai anthropic
```

#### 3 — Fill in your API keys

The setup script writes a `.env` template. Open it and replace placeholder values:

```bash
nano .env
```

Key variables to set:

```dotenv
STRIPE_SECRET_KEY=sk_live_...       # or sk_test_... for testing
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
OPENAI_API_KEY=sk-...               # if using OpenAI
ANTHROPIC_API_KEY=sk-ant-...        # if using Claude
```

Ports can be left at defaults unless another app is already using them:

```dotenv
PORT=3000               # agent-x-core
DIGITAL_TWIN_PORT=3002  # digital-twin
DASHBOARD_PORT=5000     # Flask dashboard
WEBHOOK_PORT=3003       # webhook-listener
```

---

### Starting services

```bash
# Start everything
bash termux/start.sh

# Or use the installed CLI shortcut
agent-x start

# Start individual services
bash termux/start.sh core       # agent-x-core only
bash termux/start.sh twin       # digital-twin only
bash termux/start.sh dashboard  # Python dashboard only
bash termux/start.sh webhook    # webhook-listener only
```

After starting, verify with:

```bash
bash termux/status.sh
```

Expected output:

```
PM2 Processes:
┌─────┬─────────────────────┬─────────┬──────┬───────────┐
│ id  │ name                │ status  │ cpu  │ memory    │
├─────┼─────────────────────┼─────────┼──────┼───────────┤
│ 0   │ agent-x-core        │ online  │ 0%   │ 45mb      │
│ 1   │ digital-twin        │ online  │ 0%   │ 38mb      │
│ 2   │ dashboard           │ online  │ 0%   │ 52mb      │
│ 3   │ webhook-listener    │ online  │ 0%   │ 30mb      │
└─────┴─────────────────────┴─────────┴──────┴───────────┘

HTTP Health Checks:
  ✔ agent-x-core      — http://localhost:3000/health  [HTTP 200]
  ✔ digital-twin      — http://localhost:3002/health  [HTTP 200]
  ✔ dashboard         — http://localhost:5000/        [HTTP 200]
```

---

### Stopping services

```bash
# Stop all services
bash termux/stop.sh

# Stop individual service
bash termux/stop.sh core
bash termux/stop.sh twin
bash termux/stop.sh dashboard
bash termux/stop.sh webhook

# Force-remove all PM2 entries (nuclear option)
bash termux/stop.sh kill
```

---

### Viewing logs

```bash
# Tail all logs (live)
bash termux/logs.sh

# Tail a specific service
bash termux/logs.sh core
bash termux/logs.sh twin
bash termux/logs.sh dashboard
bash termux/logs.sh webhook

# View raw log file
bash termux/logs.sh file agent-x-core

# Or use PM2 directly
pm2 logs
pm2 logs agent-x-core --lines 100
```

Log files are also written to `logs/` in the repo root:

```
logs/
├── agent-x-core.log
├── digital-twin.log
├── dashboard.log
├── webhook-listener.log
└── boot.log          ← written on device reboot
```

---

### Auto-start on device reboot

Agent X can restart automatically when your Android device reboots, using the **Termux:Boot** addon.

**Step 1** — Install Termux:Boot from F-Droid (not Google Play):
```
https://f-droid.org/en/packages/com.termux.boot/
```

**Step 2** — Open the Termux:Boot app once. This registers the `~/.termux/boot/` directory.

**Step 3** — Install the Agent X boot hook:
```bash
bash termux/install_boot.sh
```

This copies `termux/boot.sh` to `~/.termux/boot/agent-x-boot.sh` and patches the repo path. On every reboot, Termux:Boot will run this script, which:
1. Waits 8 seconds for networking to initialise
2. Attempts `pm2 resurrect` (restores last saved process list)
3. Falls back to `bash termux/start.sh all` if no saved state exists

**To disable auto-start:**
```bash
rm ~/.termux/boot/agent-x-boot.sh
```

---

### Known limitations on Termux

Understanding these constraints will help you avoid common pitfalls:

#### No `systemd`
Termux runs without root and without an init system. There are no `.service` files, `systemctl`, or `@reboot` cron entries. **PM2** is the sole process manager for Node.js services; Python agents are managed via PM2 with `--interpreter bash` wrapper scripts.

#### No `docker` / no `docker-compose`
Docker is not available in Termux (no kernel namespaces without root). The `deployment/Dockerfile` and `docker-compose.yml` files are for **Linux server deployments only** and will not work in Termux.

#### No `torch` / GPU acceleration
PyTorch with CUDA or MPS is not available in Termux. The `transformers` library can still be used in CPU-only mode for smaller models, but performance will be slow on mobile hardware. For LLM inference, prefer API-based providers (OpenAI, Anthropic) by setting the relevant keys in `.env`.

#### Path constraints
- Termux home is `/data/data/com.termux/files/home` — always use `$HOME`, never hardcoded `/root` or `/home/username`
- Termux prefix is `/data/data/com.termux/files/usr` — accessible as `$PREFIX`
- External SD card access requires `termux-setup-storage` first

#### Limited background execution
Android aggressively kills background processes to save battery. Mitigations:
- Run `termux-wake-lock` before starting services (included in `termux/start.sh`)
- Enable "Disable Battery Optimisation" for Termux in Android Settings → Battery
- Use Termux:Boot for reliable restart after kills

#### `pkg` not `apt`
Termux uses its own `pkg` package manager, which wraps `apt` but with a Termux-specific repository. Always use `pkg install` in Termux scripts, not `apt install`. Some packages have different names (e.g., `python` installs Python 3).

#### Single-user environment
Termux has no multi-user support and no `sudo`. If a script tries to write to `/etc` or run `sudo`, it will fail. All paths must stay within `$HOME` or `$PREFIX`.

#### Port binding
Ports below 1024 require root in standard Linux, but Termux on Android allows binding to any port unprivileged. The defaults (3000, 3002, 5000, 3003) all work fine. However, another app or service may already be listening on a port — change the relevant variable in `.env` if you get `EADDRINUSE` errors.

#### `clang` required for native Python packages
Some Python packages (e.g., `psutil`, `cryptography`) need to compile C extensions. Termux provides `clang` and `make` for this — the setup script installs them. If you skip them and later add a package that needs compilation, run `pkg install clang make` first.

#### `node-gyp` and native Node modules
Native Node.js addons that use `node-gyp` may fail or require additional Termux packages (`python`, `make`, `clang`). The packages used by Agent X are all pure-JS or pre-built, so this should not be an issue unless you add custom dependencies.

---

### Termux troubleshooting

**Setup fails with "unable to find package"**
```bash
pkg update -y && pkg upgrade -y
bash termux/setup.sh
```

**`pm2` command not found after install**
```bash
npm install -g pm2
# Then re-open Termux or run:
export PATH="$PATH:$(npm prefix -g)/bin"
```

**Port already in use (`EADDRINUSE`)**
```bash
# Find what's on port 3000
ss -tlnp | grep 3000
# Change the port in .env then restart
bash termux/stop.sh && bash termux/start.sh
```

**Python import errors after setup**
```bash
# Check which python pip is using
python -m pip show flask
# Re-install into the correct environment
python -m pip install flask flask-socketio --force-reinstall
```

**Services stop when screen turns off / app is backgrounded**
1. Go to Android Settings → Apps → Termux → Battery → Unrestricted
2. Run `termux-wake-lock` in your Termux session before starting services
3. Install Termux:Boot for automatic restart

**`transformers` import fails or is very slow**
```bash
# Use lightweight API clients instead of local models
python -m pip install openai anthropic
# Set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env
```

**Re-run setup cleanly (preserves .env and state files)**
```bash
bash termux/setup.sh        # fully idempotent — safe to re-run
```

---

## Configuration

The central configuration file is `.env` (generated by `termux/setup.sh` or copied from `.env.example`).

Additional configuration:

| File | Purpose |
|---|---|
| `config/settings.yaml` | Global agent behaviour settings |
| `agent-x-core/tasks.json` | Task queue definitions |
| `stripe-catalog/config.json` | Stripe product catalog config |
| `memory/state.json` | Live runtime state (auto-managed) |
| `data/db.json` | Primary data store (auto-managed) |

---

## Services Reference

### `agent-x-core` (Node.js, port 3000)

Primary command centre. Exposes a REST API for task submission, routes tasks to worker agents via stdio JSON, and manages the task queue.

```
POST /task         Submit a new task
GET  /tasks        List all tasks
GET  /health       Health check
GET  /status       System status
```

### `digital-twin` (Node.js, port 3002)

Execution layer. Runs pipelines, manages artifact lifecycle, and coordinates multi-step agent sequences.

### `dashboard` (Python/Flask, port 5000)

Real-time monitoring UI built with Flask and SocketIO. Shows agent status, task queue, revenue metrics, and live log streams. Open `http://localhost:5000` in your browser (or use port-forwarding for remote access).

### `webhook-listener` (Node.js, port 3003)

Ingests Stripe and other external webhooks. Validates signatures and routes events to the appropriate handlers.

---

## Agent Communication Protocol

Worker agents in `agent-x-core/agents/` communicate via **stdio JSON envelopes** — one JSON object per line on stdin, one JSON response on stdout.

**Request envelope:**
```json
{
  "action": "draft",
  "requestId": "uuid-v4",
  "payload": { "topic": "passive income ideas", "format": "blog" }
}
```

**Response envelope:**
```json
{
  "requestId": "uuid-v4",
  "status": "ok",
  "result": { "content": "..." },
  "duration": 312
}
```

**Error response:**
```json
{
  "requestId": "uuid-v4",
  "status": "error",
  "error": "LLM request timed out",
  "duration": 5001
}
```

---

## Revenue Modules

| Module | Location | Description |
|---|---|---|
| Content Pipeline | `blueprints/content-pipeline/` | Blog/copy generation → publish |
| Data Aggregator | `blueprints/data-aggregator/` | HTTP data collection + summarise |
| Product Factory | `products/product-factory.py` | AI product definition generation |
| Product Publisher | `products/product-publisher.py` | Push products to Stripe catalog |
| Stripe Checkout | `execution/stripe.js` | Checkout session creation + fulfillment |
| Revenue Engine | `core/revenue_engine.py` | Revenue tracking and optimisation |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes and test on both Linux and Termux if possible
4. Submit a pull request

When adding new scripts, follow these conventions:
- Use `#!/data/data/com.termux/files/usr/bin/bash` for Termux-only scripts
- Use `#!/usr/bin/env bash` for cross-platform scripts
- Always resolve paths via `$HOME` or `$REPO_DIR` — never hardcode `/root` or `/home/user`
- Use `pkg install` (not `apt install`) for Termux dependency instructions
- Test that `set -euo pipefail` doesn't break anything before committing
