# Agent X — Termux Compatibility Guide

> **TL;DR** — Run `bash termux/setup.sh` once, then `bash termux/start.sh`.

---

## Table of Contents

1. [Quick Start](#1-quick-start)
2. [pkg install dependencies](#2-pkg-install-dependencies)
3. [pip install dependencies](#3-pip-install-dependencies)
4. [npm install dependencies](#4-npm-install-dependencies)
5. [What Changed (Audit Results)](#5-what-changed-audit-results)
6. [Path Conventions](#6-path-conventions)
7. [systemd → PM2 Migration](#7-systemd--pm2-migration)
8. [Docker → Native Migration](#8-docker--native-migration)
9. [Auto-start on Boot](#9-auto-start-on-boot)
10. [File-by-File Change Log](#10-file-by-file-change-log)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. Quick Start

```bash
# 1. Clone the repo into Termux home
git clone <repo-url> ~/agent-x
cd ~/agent-x

# 2. Run the bootstrap (installs everything)
bash termux/setup.sh

# 3. Edit your API keys
nano .env

# 4. Start all services
bash termux/start.sh

# 5. Check status
bash termux/status.sh
```

---

## 2. `pkg install` Dependencies

Run once (or let `termux/setup.sh` handle it):

```bash
pkg update -y && pkg install -y \
  bash \
  coreutils \
  curl \
  wget \
  git \
  nodejs \
  python \
  python-pip \
  make \
  clang \
  binutils \
  openssl \
  libffi \
  pkg-config \
  zip \
  unzip \
  procps \
  iproute2 \
  less \
  nano \
  jq
```

| Package | Why |
|---|---|
| `bash` | All scripts use `#!/data/data/com.termux/files/usr/bin/bash` |
| `coreutils` | `mkdir`, `cp`, `chmod`, `sed`, `tail`, `wc`, etc. |
| `curl` | HTTP health checks in `termux/status.sh` |
| `git` | `upgrade_agents.sh` pulls latest code |
| `nodejs` | Runs `agent-x-core`, `digital-twin`, all JS worker agents |
| `python` | Runs dashboard, Python agents, process manager |
| `python-pip` | Install Python packages |
| `make` / `clang` | Needed by some pip packages that compile C extensions |
| `openssl` / `libffi` | TLS + `cryptography` library deps |
| `procps` | `ps`, used by watchdog/status scripts |
| `jq` | JSON pretty-printing in shell scripts |

---

## 3. `pip install` Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install \
  flask \
  flask-socketio \
  flask-cors \
  eventlet \
  requests \
  pyyaml \
  python-dotenv \
  stripe \
  schedule \
  psutil \
  colorama \
  rich \
  python-dateutil
```

| Package | Used By |
|---|---|
| `flask` | `dashboard/app.py` |
| `flask-socketio` | `dashboard/app.py` — real-time events |
| `flask-cors` | Cross-origin requests to dashboard |
| `eventlet` | Async driver for SocketIO (avoids `gevent` compile issues on ARM) |
| `requests` | Python agents making HTTP calls |
| `pyyaml` | `config/settings.yaml` loading |
| `python-dotenv` | `.env` file loading in Python scripts |
| `stripe` | `products/product-publisher.py` |
| `schedule` | `core/loop_engine.py` task scheduling |
| `psutil` | `process-manager.py` — PID existence checks |
| `colorama` | Terminal colour support on Android |
| `rich` | Pretty terminal output |
| `python-dateutil` | Date parsing in data aggregator |

### Optional ML Packages (may fail on Termux without pre-built wheels)

```bash
# Only install if you need local LLM inference
pip install transformers
# torch for ARM is large; prefer API-based LLM (OpenAI/Anthropic) in Termux
```

---

## 4. `npm install` Dependencies

These are installed automatically by `npm install` in each sub-project.

### Root / `agent-x-core`
| Package | Version | Purpose |
|---|---|---|
| `express` | ^5.2.1 | HTTP API server |
| `axios` | ^1.17.0 | Outbound HTTP |
| `cors` | ^2.8.6 | CORS middleware |
| `dotenv` | ^17.4.2 | `.env` loading |
| `uuid` | ^14.0.0 | ID generation |

### `execution` / `stripe-catalog`
| Package | Purpose |
|---|---|
| `stripe` | ^22.2.1 | Stripe SDK |
| `jsonwebtoken` | Auth tokens |
| `bcryptjs` | Password hashing |

### Global npm tools (installed once)
```bash
npm install -g pm2 nodemon
```

| Tool | Purpose |
|---|---|
| `pm2` | Process manager — replaces systemd in Termux |
| `nodemon` | Dev file watching |

---

## 5. What Changed (Audit Results)

### Problems Found

| File | Problem | Fix |
|---|---|---|
| `deployment/termux-boot.sh` (old) | Empty / placeholder | Replaced with working boot script |
| `deployment/agent-x-core.service` | systemd unit — unavailable in Termux | Added Termux warning; kept for Linux use |
| `deployment/digital-twin.service` | systemd unit — unavailable in Termux | Same |
| `setup_agents.sh` | Hardcoded `/usr/local/bin/node`, no validation | Rewritten with `$PREFIX`-relative node path, syntax checks |
| `upgrade_agents.sh` | Called `systemctl restart` | Rewritten with `pm2 restart` |
| `agent-x-core/agents/run_one.py` | Used hardcoded `/usr/bin/node` | Now resolves via `$PREFIX/bin/node` with PATH fallback |
| `agent-x-core/agents/orchestrator.run.py` | Used hardcoded paths | Same fix |
| `agent-x-core/agents/status-saver.py` | Called `systemctl status` | Rewritten to use PM2 jlist + PID files |
| `agent-x-core/agents/Status.cli.py` | Called `systemctl` | Rewritten to use status-saver.py output |
| `agent-x-core/Status.show.py` | Called `systemctl` | Rewritten with PM2 + JSON state |
| `process-manager.py` | Assumed `/var/run` PID dirs, called `service` | Fully rewritten for Termux |
| `run.py` | Sparse / incomplete | Rewritten to delegate to process-manager.py |
| `requirements.txt` | Missing many deps; included `transformers` unconditionally | Annotated; heavy ML deps now optional |

### New Files Added

| File | Purpose |
|---|---|
| `termux/setup.sh` | One-shot bootstrap: pkg + pip + npm install |
| `termux/start.sh` | Start all services via PM2 |
| `termux/stop.sh` | Stop services via PM2 |
| `termux/status.sh` | PM2 table + HTTP health checks + state file summary |
| `termux/logs.sh` | Log viewer (PM2 or raw files) |
| `termux/boot.sh` | Boot script (Termux:Boot app entry point) |
| `termux/install_boot.sh` | Installs boot.sh into `~/.termux/boot/` |
| `termux/run_dashboard.sh` | Launches Flask dashboard (called by PM2) |
| `TERMUX-COMPAT.md` | This file |

---

## 6. Path Conventions

### The Core Rule

**Never hardcode `/usr/...` paths in Termux scripts.**

In Termux, the filesystem root for installed packages is:
```
/data/data/com.termux/files/usr
```

This is exposed as the `$PREFIX` environment variable.

### Mapping

| Linux path | Termux equivalent | Script usage |
|---|---|---|
| `/usr/bin/node` | `$PREFIX/bin/node` | `${PREFIX}/bin/node` |
| `/usr/bin/python3` | `$PREFIX/bin/python` | `$(which python)` |
| `/usr/local/bin/pm2` | `$PREFIX/bin/pm2` | `pm2` (via PATH) |
| `/etc/systemd/system/` | ❌ N/A | Use PM2 instead |
| `/var/run/*.pid` | `~/agent-x/logs/pids/` | `$REPO_DIR/logs/pids/` |
| `/var/log/` | `~/agent-x/logs/` | `$REPO_DIR/logs/` |
| `$HOME` | `/data/data/com.termux/files/home` | `$HOME` (works normally) |

### Script Header Template

All shell scripts in this repo use:

```bash
#!/data/data/com.termux/files/usr/bin/bash
PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
```

Python scripts use:

```python
import os, sys
from pathlib import Path
PREFIX   = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
REPO_DIR = Path(__file__).resolve().parent  # adjust .parent depth as needed
```

---

## 7. systemd → PM2 Migration

**systemd is NOT available in Termux** (requires root and a full Linux kernel init).

### Equivalences

| systemd | PM2 (Termux) |
|---|---|
| `systemctl start agent-x-core` | `pm2 start agent-x-core` |
| `systemctl stop agent-x-core` | `pm2 stop agent-x-core` |
| `systemctl restart agent-x-core` | `pm2 restart agent-x-core` |
| `systemctl status` | `pm2 list` |
| `journalctl -u agent-x-core` | `pm2 logs agent-x-core` |
| `systemctl enable agent-x-core` | `pm2 startup` + `pm2 save` |
| `/etc/systemd/system/*.service` | `termux/start.sh` (pm2 launch config) |

### Start everything

```bash
bash termux/start.sh       # uses pm2 under the hood
```

### Persist across reboots

```bash
pm2 save                   # save current process list
bash termux/install_boot.sh  # install Termux:Boot hook
```

---

## 8. Docker → Native Migration

**Docker is NOT available in standard Termux** (requires kernel namespacing/cgroups unavailable without root).

All services that were containerised in `deployment/docker-compose.yml` run
natively in Termux instead — the exact same Node.js and Python processes, just
without the container wrapper.

The `deployment/Dockerfile` is kept for Linux/cloud deployment only.

### Port mapping (no Docker networking)

| Service | Port | Access |
|---|---|---|
| `agent-x-core` | 3000 | `http://localhost:3000` |
| `digital-twin` | 3002 | `http://localhost:3002` |
| `dashboard` | 5000 | `http://localhost:5000` |
| `webhook-listener` | (set in `.env`) | `http://localhost:<PORT>` |

> Note: original config had both `digital-twin` and `dashboard` on port 3001.
> This repo uses **3002** for digital-twin and **5000** for dashboard to avoid
> the conflict.  Update `DIGITAL_TWIN_PORT` and `DASHBOARD_PORT` in `.env`.

---

## 9. Auto-start on Boot

Requires the **Termux:Boot** app from **F-Droid** (not Google Play):
<https://f-droid.org/en/packages/com.termux.boot/>

```bash
# 1. Install Termux:Boot from F-Droid
# 2. Open Termux:Boot once to register the boot directory
# 3. Install the Agent X boot hook:
bash termux/install_boot.sh

# 4. Reboot device — Agent X will start automatically
```

The boot script at `~/.termux/boot/agent-x-boot.sh`:
1. Waits 10 s for Android networking to initialise
2. Calls `pm2 resurrect` to restore the saved process list
3. Falls back to `termux/start.sh all` if no saved state exists

---

## 10. File-by-File Change Log

### `setup_agents.sh`
- **Removed**: hardcoded `/usr/local/bin/node`, `which nodejs` fallback
- **Added**: `$PREFIX`-based node resolution, Python syntax validation via `ast.parse`, permission fixup for all `termux/*.sh`

### `upgrade_agents.sh`
- **Removed**: `systemctl restart ...` calls
- **Added**: `pm2 restart` for each service, `pm2 update`, pip `--upgrade` flags

### `process-manager.py`
- **Removed**: `/var/run/` PID paths, `subprocess.run(["service", ...])` calls
- **Added**: `$PREFIX`-aware node resolution, `start_new_session=True` for daemonisation, `psutil` PID checks with `os.kill(pid, 0)` fallback

### `run.py`
- **Removed**: sparse stub that didn't delegate properly
- **Added**: alias map (`start`, `stop`, `status`, `core`, etc.) delegating to `process-manager.py`

### `agent-x-core/agents/run_one.py`
- **Removed**: hardcoded `/usr/bin/node`
- **Added**: `$PREFIX/bin/node` + `shutil.which("node")` fallback, `.env` loader

### `agent-x-core/agents/orchestrator.run.py`
- **Removed**: hardcoded node path, no env loading
- **Added**: `$PREFIX` resolution, `.env` loader, argparse CLI, timeout handling

### `agent-x-core/agents/status-saver.py`
- **Removed**: `subprocess.run(["systemctl", "status", ...])` calls
- **Added**: `pm2 jlist` JSON parsing with PID-file fallback, revenue/task counts

### `agent-x-core/agents/Status.cli.py`
- **Removed**: `systemctl` calls, hardcoded paths
- **Added**: delegates to `status-saver.py`, `--watch` mode, ANSI colour display

### `agent-x-core/Status.show.py`
- **Removed**: `systemctl` / `service` calls
- **Added**: PM2 jlist, memory/state.json display, `--json` / `--services` / `--tasks` flags

### `deployment/termux-boot.sh`
- **Removed**: placeholder / empty content
- **Added**: full working boot script with `pm2 resurrect` + fallback

### `deployment/agent-x-core.service` / `digital-twin.service`
- **Added**: prominent Termux warning comment at top
- Kept for Linux/server use

### `deployment/Dockerfile`
- **Added**: Termux warning, Python layer install, PM2 global install

### `requirements.txt`
- **Added**: all missing runtime deps (`flask-cors`, `eventlet`, `schedule`, `psutil`, `colorama`, `rich`, `python-dateutil`)
- **Annotated**: `transformers` / `torch` as optional (may fail on ARM)

---

## 11. Troubleshooting

### `bash: /usr/bin/bash: No such file or directory`
Scripts use `#!/data/data/com.termux/files/usr/bin/bash`.  Make sure bash is installed:
```bash
pkg install bash
```

### `node: command not found`
```bash
pkg install nodejs
```

### `pm2: command not found`
```bash
npm install -g pm2
```

### `pip install` fails with compiler error
Some packages need `clang` and `make`:
```bash
pkg install clang make libffi openssl
pip install <package>
```

### Port already in use
Check what's on the port and adjust `.env`:
```bash
ss -tlnp | grep 3000
# or
netstat -tlnp 2>/dev/null | grep 3000
```

### PM2 shows all processes as `stopped` after reboot
Run:
```bash
bash termux/install_boot.sh
pm2 save
```
Then verify Termux:Boot app is installed and opened at least once.

### Dashboard import error (`from app import socketio`)
Make sure `eventlet` is installed (not `gevent`):
```bash
pip install eventlet
```
And the dashboard app uses:
```python
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")
```

### `transformers` fails to install
This is expected on many Android devices — comment it out in `requirements.txt`
and use the OpenAI/Anthropic API via `core/llm_client.py` instead.
