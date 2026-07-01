# Agent X — Termux Dev Server & Build Process Test Report

This document records the findings from running the automated test suites
(`termux/test-build.sh` and `termux/test-dev-server.sh`) in a live Termux
environment. It covers ARM-specific issues, permission problems, known
workarounds, and a quick-reference troubleshooting table.

---

## Table of Contents

1. [How to Run the Tests](#1-how-to-run-the-tests)
2. [Build Process Validation](#2-build-process-validation)
3. [Dev Server Startup Validation](#3-dev-server-startup-validation)
4. [ARM-Specific Issues & Workarounds](#4-arm-specific-issues--workarounds)
5. [Permission-Related Issues & Workarounds](#5-permission-related-issues--workarounds)
6. [Common Error Reference](#6-common-error-reference)
7. [Port & Configuration Conflicts](#7-port--configuration-conflicts)
8. [Memory & Disk Constraints](#8-memory--disk-constraints)
9. [Python / Flask Dashboard Issues](#9-python--flask-dashboard-issues)
10. [PM2 on Termux](#10-pm2-on-termux)
11. [Interpreting Test Output](#11-interpreting-test-output)

---

## 1. How to Run the Tests

### Full test suite (build + dev server)
```bash
bash termux/test-runner.sh
```

### Build tests only (no services started)
```bash
bash termux/test-build.sh
```

### Dev server tests only (assumes build is complete)
```bash
bash termux/test-dev-server.sh
```

### Quick mode — no installs, no service starts
```bash
bash termux/test-runner.sh --fast --no-start
```

### Skip heavy LLM packages during build
```bash
bash termux/test-runner.sh --no-llm
```

### After a first-time clone (run setup first, then test)
```bash
bash termux/setup.sh --no-llm   # bootstrap
bash termux/test-runner.sh --no-start  # verify build
bash termux/start.sh            # start services
bash termux/test-dev-server.sh --no-start  # verify health
```

### Test log files
All test output is written to timestamped files under `logs/`:
```
logs/test-build-YYYYMMDD-HHMMSS.log
logs/test-dev-server-YYYYMMDD-HHMMSS.log
logs/test-runner-YYYYMMDD-HHMMSS.log
```

---

## 2. Build Process Validation

### What the build test checks

| Step | What is verified | Pass condition |
|---|---|---|
| System packages | `bash`, `node`, `npm`, `git`, `curl`, `jq`, `make`, `python` in PATH | All binaries found |
| Node.js version | Major version ≥ 18 (required by Express 5, uuid@14) | `node -v` ≥ 18 |
| npm version | Major version ≥ 7 (package-lock v2 support) | `npm -v` ≥ 7 |
| Python version | ≥ 3.7 | `python3 --version` ≥ 3.7 |
| npm install (root) | All root dependencies installed | `node_modules/` populated |
| npm install (agent-x-core) | Express, axios, uuid, dotenv, etc. | `node_modules/` populated |
| npm install (digital-twin) | Express + dependencies | `node_modules/` populated |
| npm install (communication) | node-fetch + dependencies | `node_modules/` populated |
| npm install (webhook-listener) | stripe, express | `node_modules/` populated |
| Package versions | express ≥ 5, axios ≥ 1, uuid ≥ 9, dotenv ≥ 16 | Semver check passes |
| pip install | flask, flask-socketio, requests, dotenv, psutil | All importable |
| Runtime dirs | `memory/`, `data/`, `generated/`, `logs/`, etc. | Directories exist + writable |
| JSON state files | `memory/state.json`, `data/db.json`, etc. | Valid JSON, non-empty |
| `.env` file | Required keys set, no port collisions | PORT etc. are non-empty |
| PM2 daemon | pm2 installed, daemon reachable | `pm2 ping` succeeds |
| ARM native addons | No x86 `.node` binaries; bcryptjs (pure JS) confirmed | No arch mismatch |
| `require()` smoke test | Critical packages loadable at runtime | No module load error |
| Syntax check | `node --check` on entry points | Zero parse errors |
| Idempotency | State files preserved after re-run | Files not zeroed |

### Expected passing build output
```
── 6. npm install (per service) ──
  [PASS]  root: npm install OK — 142 packages in 47s
  [PASS]  agent-x-core: npm install OK — 68 packages in 12s
  [PASS]  digital-twin: npm install OK — 31 packages in 8s
  ...

── 14. Post-build smoke tests ──
  [PASS]  require('express') OK in agent-x-core
  [PASS]  require('axios') OK in agent-x-core
  [PASS]  Syntax OK: agent-x-core/index.js
  [PASS]  Syntax OK: digital-twin/index.js
  [PASS]  dashboard/app.py compiles without syntax errors
```

---

## 3. Dev Server Startup Validation

### What the dev server test checks

| Step | What is verified |
|---|---|
| Pre-flight | node, python, pm2, curl available |
| File integrity | All critical `.js`, `.py`, `package.json` files present |
| Port availability | Target ports free before start |
| Port conflict detection | Warns if two services share a port |
| ARM permission | Exec bits set; write access to repo; W^X not enforced |
| Wake lock hint | `termux-wake-lock` available |
| Syntax check | `node --check` on all worker agents |
| Python imports | flask, flask_socketio, requests, dotenv importable |
| Service start | `termux/start.sh all` exits 0 |
| Port open check | Each port binds within 30s (configurable via `STARTUP_TIMEOUT`) |
| HTTP health check | GET `/health` returns 2xx for core + twin; GET `/` for dashboard |
| `/api/tasks` probe | agent-x-core tasks endpoint responds |
| PM2 status | Each process shows `online` in `pm2 jlist` |
| Log creation | `logs/agent-x-core.log`, `logs/digital-twin.log`, etc. created |
| Log error scan | Scans logs for `EADDRINUSE`, `Cannot find module`, `SyntaxError` |
| ARM native addon arch | `.node` binaries are ARM64, not x86_64 |
| RAM check | ≥ 512 MB available recommended |
| Disk check | ≥ 500 MB free recommended |

### Healthy startup sequence (expected log flow)

**agent-x-core** (`logs/agent-x-core.log`):
```
[agent-x-core] Express server listening on port 3000
[agent-x-core] Task API ready
[agent-x-core] Orchestrator initialised
```

**digital-twin** (`logs/digital-twin.log`):
```
[digital-twin] Pipeline runner ready on port 3002
[digital-twin] Artifact manager initialised
```

**dashboard** (`logs/dashboard.log`):
```
 * Running on http://0.0.0.0:5000
 * SocketIO initialised
```

---

## 4. ARM-Specific Issues & Workarounds

### 4.1 Native Node.js addons (`.node` binary files)

**Problem**: Some npm packages include pre-built native C++ addons. Pre-built
binaries are typically compiled for `x86_64` Linux. When installed on an
`aarch64` Android device they either fail to load at runtime or cause
`SIGILL` (Illegal Instruction) crashes.

**Affected packages in Agent X**: None in the current dependency set —
`bcryptjs` (pure JS), `stripe` (pure JS), `axios` (pure JS), `express` (pure JS)
are all architecture-safe.

**How to detect**:
```bash
find agent-x-core/node_modules -name "*.node" | xargs file 2>/dev/null
# Look for "ELF 64-bit LSB shared object, x86-64" — that is a mismatch
# Safe output: "ELF 64-bit LSB shared object, ARM aarch64"
```

**Workaround** (if a native addon is required):
```bash
# Rebuild from source using Termux's clang/make toolchain
cd agent-x-core
npm rebuild <package-name> --build-from-source

# If node-gyp fails, ensure build tools are installed:
pkg install clang make binutils python
```

**Workaround for `bcrypt` → `bcryptjs`** (if pure-JS alternative exists):
```bash
npm uninstall bcrypt
npm install bcryptjs
# Update require('bcrypt') → require('bcryptjs') in code
```

---

### 4.2 Node.js version on ARM

**Problem**: Termux ships a recent Node.js LTS. However, some older Termux
installs may have Node 16 or 14, which is incompatible with:
- `express@^5.x` (requires Node ≥ 18)
- `uuid@^14.x` (requires Node ≥ 18)
- ES Module syntax (`import`/`export`) in newer packages

**Detection**:
```bash
node --version   # Must be v18.x or higher
```

**Fix**:
```bash
pkg update
pkg upgrade nodejs
# Or install a specific version:
pkg install nodejs-lts
```

---

### 4.3 Heap memory exhaustion during npm install

**Problem**: `npm install` on ARM devices with limited RAM (< 2 GB) can fail
with JavaScript heap out of memory errors, particularly when processing large
dependency trees or running `postinstall` scripts.

**Symptoms**:
```
FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory
 1: 0x... node::Abort() ...
```

**Workarounds**:

Option A — Set `--max-old-space-size` before running npm:
```bash
export NODE_OPTIONS="--max-old-space-size=512"
npm install
```

Option B — Use `--prefer-offline` to reduce memory footprint:
```bash
npm install --prefer-offline --no-audit --no-fund
```

Option C — Add a swapfile (if device allows):
```bash
# Requires root or a swap-enabled kernel module
# Non-root alternative: use zram if available
```

Option D — Install packages one at a time:
```bash
npm install express axios dotenv cors uuid stripe --save
npm install jsonwebtoken bcryptjs lowdb --save
npm install nodemon pm2 --save-dev
```

---

### 4.4 Python wheel availability on ARM

**Problem**: Some Python packages don't publish ARM64 wheels on PyPI. `pip`
will attempt to compile from source, which requires gcc/clang and may fail
in Termux if build headers are missing.

**Common affected packages**:
- `cryptography` — requires `libssl-dev`, `libffi-dev`
- `numpy` / `scipy` — large, slow to compile; use Termux's pre-built package
- `torch` / `tensorflow` — generally not available on Android ARM via pip

**Flask + flask-socketio** (used by Agent X dashboard): pure Python, no
compilation needed — should install cleanly.

**Fix for compilation failures**:
```bash
# Install Termux build essentials
pkg install clang python-dev openssl libffi pkg-config

# Then retry pip install
pip install <package-name>
```

**Avoid transformers + torch on low-RAM ARM** (use `--no-llm` flag):
```bash
bash termux/setup.sh --no-llm
bash termux/test-runner.sh --no-llm
```

---

### 4.5 `SIGBUS` / alignment errors on 32-bit ARM

**Problem**: On `armv7l` (32-bit) Android devices, some Node.js internals
can produce `SIGBUS` errors related to unaligned memory access, particularly
with older libc versions.

**Workaround**: Use a 64-bit (`aarch64`) Android build target. All modern
Android phones (Android 5+, 64-bit) run on `aarch64`. Check:
```bash
uname -m   # Should print: aarch64
```

If `armv7l`, consider using the 32-bit Termux Node build:
```bash
pkg install nodejs
# Termux auto-selects the correct architecture package
```

---

## 5. Permission-Related Issues & Workarounds

### 5.1 W^X (Write XOR Execute) restriction on Android 10+

**Problem**: Android 10+ enforces a W^X memory protection policy that
prevents pages from being both writable and executable at the same time.
This breaks JIT compilation in some Node.js and Python operations.

**Detection**:
```bash
# If node fails immediately with "Illegal instruction" or "Killed"
node -e "console.log('ok')"
```

**Workaround**: Termux's `nodejs` package is compiled with W^X compatibility.
If using a custom Node.js build, ensure it is compiled with `--without-snapshot`
or use the Termux repo package:
```bash
pkg install nodejs   # uses the Termux-patched build
```

For Python, use Termux's Python package (not a custom compile):
```bash
pkg install python   # W^X-safe Termux build
```

---

### 5.2 Execute permission stripped by Android `/data` mount

**Problem**: The `/data` partition may be mounted `noexec` on some Android
versions, preventing scripts in `/data/data/com.termux/files/home` from
being executed directly.

**Symptom**:
```
bash: ./termux/start.sh: Permission denied
```

**Workaround**: Always invoke scripts via `bash`:
```bash
bash termux/start.sh     # ← correct
./termux/start.sh        # ← may fail on noexec mounts
```

The test scripts are invoked via `bash <script>` for this reason. The
shebang line (`#!/data/data/com.termux/files/usr/bin/bash`) is present as
a fallback for environments where exec IS permitted.

---

### 5.3 `TMPDIR` / temp directory restrictions

**Problem**: Some npm postinstall scripts write executables to `/tmp`, which
may be on a `noexec` mount on Android.

**Fix**:
```bash
# Redirect tmp to the Termux-safe prefix
export TMPDIR="${PREFIX}/tmp"
mkdir -p "${TMPDIR}"
npm install
```

The `test-build.sh` script detects this condition:
```
[WARN] Cannot execute scripts in /tmp — possible W^X restriction
       Ensure scripts are in Termux home or use PREFIX paths
       tmpdir: use export TMPDIR=$PREFIX/tmp
```

---

### 5.4 Storage permission for files outside Termux home

**Problem**: By default, Termux cannot read/write to `/sdcard` or external
storage locations. Agent X stores all data under `$HOME/agent-x/` (Termux
home), so this is generally not an issue — but Stripe webhook files or
generated exports that a user moves to `/sdcard` will fail.

**Fix** (if external storage access is needed):
```bash
termux-setup-storage
# Tap "Allow" in the Android dialog
# External storage is then accessible at ~/storage/
```

---

### 5.5 Wake lock — Android killing background processes

**Problem**: Android's battery optimiser aggressively kills background
processes. Long-running PM2-managed Node.js processes may be terminated
after the screen turns off.

**Detection**: Processes disappear from `pm2 list` without explicit stop.

**Fix**:
```bash
# Acquire a wake lock before starting services
termux-wake-lock

# Then start services
bash termux/start.sh
```

`termux-wake-lock` requires the **Termux:API** app from F-Droid:
```
https://f-droid.org/en/packages/com.termux.api/
```

After installing Termux:API, install the companion package:
```bash
pkg install termux-api
```

Add to `~/.bashrc` or `~/.profile` for persistence:
```bash
termux-wake-lock
```

---

### 5.6 File descriptor limits

**Problem**: Termux's default `ulimit -n` (open file descriptors) is often
1024. Node.js event-driven servers and PM2 can hit this limit under load.

**Check**:
```bash
ulimit -n   # typical Termux output: 1024
```

**Fix**:
```bash
ulimit -n 4096
# Or add to ~/.bashrc:
echo "ulimit -n 4096" >> ~/.bashrc
```

---

## 6. Common Error Reference

| Error message | Cause | Fix |
|---|---|---|
| `EADDRINUSE: address already in use :::3000` | Another process is using the port | `pm2 delete agent-x-core && bash termux/start.sh core` or change `PORT` in `.env` |
| `Cannot find module 'express'` | `node_modules` missing | `cd agent-x-core && npm install` |
| `Error: ENOENT: no such file or directory, open '.env'` | `.env` file missing | `bash termux/setup.sh` |
| `SyntaxError: Unexpected token '.'` | Node.js version too old for optional chaining | `pkg upgrade nodejs` (need Node ≥ 14) |
| `FATAL ERROR: Reached heap limit` | Out of memory during npm/node | `export NODE_OPTIONS=--max-old-space-size=512` |
| `Illegal instruction` | x86 binary on ARM, or W^X violation | Rebuild native addons: `npm rebuild` |
| `pm2: command not found` | pm2 not installed or PATH not set | `npm install -g pm2` |
| `ModuleNotFoundError: No module named 'flask'` | Python package not installed | `pip install flask flask-socketio` |
| `OSError: [Errno 98] Address already in use` (Python) | Dashboard port taken | Change `DASHBOARD_PORT` in `.env` |
| `Permission denied` when running `./script.sh` | noexec mount or missing +x bit | Use `bash script.sh` instead |
| `npm ERR! code EACCES` | Permission error on global npm packages | `npm install -g pm2 --prefix $PREFIX` |
| `gyp ERR! build error` | Native addon compilation failed | Install build deps: `pkg install clang make python` |
| `signal: killed` during npm install | OOM killed by Android kernel | Reduce memory usage; add swap |
| `termux-wake-lock: not found` | Termux:API not installed | Install Termux:API from F-Droid |
| `pm2: No process found` | PM2 state cleared after reboot | `pm2 resurrect` or `bash termux/start.sh` |
| `flask_socketio` import error | eventlet/gevent not installed | `pip install eventlet flask-socketio` |

---

## 7. Port & Configuration Conflicts

### Default port assignments

| Service | Default port | `.env` key |
|---|---|---|
| `agent-x-core` | 3000 | `PORT` |
| `digital-twin` | 3002 | `DIGITAL_TWIN_PORT` |
| `dashboard` (Flask) | 5000 | `DASHBOARD_PORT` |
| `webhook-listener` | 3003 | `WEBHOOK_PORT` |

### ⚠️ Known conflict in default config

The project context document notes that `digital-twin` and `dashboard`
**may conflict on port 3001**. The `.env` template generated by `setup.sh`
resolves this by assigning distinct defaults (3002 and 5000 respectively).

**Always verify your `.env`**:
```bash
grep -E 'PORT|TWIN|DASHBOARD|WEBHOOK' .env
```

Expected output:
```
PORT=3000
DIGITAL_TWIN_PORT=3002
DASHBOARD_PORT=5000
WEBHOOK_PORT=3003
```

### Checking what is bound to a port
```bash
# Using ss (iproute2)
ss -tlnp | grep 3000

# Using netstat (net-tools)
netstat -tlnp | grep 3000

# Using bash TCP probe (no tools needed)
(echo >/dev/tcp/localhost/3000) 2>/dev/null && echo "open" || echo "closed"
```

### Resolving port conflicts
```bash
# Find the PID using the port
ss -tlnp | grep :3000

# Kill it
kill -9 <PID>

# Or stop via pm2
pm2 stop agent-x-core
pm2 delete agent-x-core
```

---

## 8. Memory & Disk Constraints

### Recommended minimums for running all services

| Resource | Minimum | Recommended |
|---|---|---|
| Free RAM | 256 MB | 512 MB+ |
| Free disk | 300 MB | 1 GB+ |
| Android version | 8.0 | 10.0+ |
| CPU architecture | armv7l | aarch64 |

### Reducing memory footprint

1. **Use `--no-llm` flag** — skips `transformers` (saves ~3 GB disk, ~1 GB RAM):
   ```bash
   bash termux/setup.sh --no-llm
   ```

2. **Limit Node.js heap size**:
   ```bash
   # Add to .env:
   NODE_OPTIONS=--max-old-space-size=256
   ```

3. **Run fewer concurrent services** — start only what you need:
   ```bash
   bash termux/start.sh core   # only agent-x-core
   ```

4. **Enable PM2 memory limits**:
   ```bash
   pm2 start agent-x-core/index.js --max-memory-restart 200M
   ```

5. **Add a swapfile** (requires write access to a suitable location):
   ```bash
   # If /data has space:
   dd if=/dev/zero of="${HOME}/swapfile" bs=1M count=512
   mkswap "${HOME}/swapfile"
   # Note: swapon requires root on most non-rooted Android devices
   ```

### Checking memory and disk from Termux
```bash
# RAM
free -m
cat /proc/meminfo | grep -E 'MemTotal|MemAvailable'

# Disk
df -h ~
df -h "${PREFIX}"
```

---

## 9. Python / Flask Dashboard Issues

### 9.1 eventlet vs. threading mode

Flask-SocketIO requires an async driver. The `run_dashboard.sh` script uses
`socketio.run(app, ...)` which auto-selects `eventlet` if available.

**If eventlet causes errors**:
```
ImportError: No module named 'eventlet'
# or
RuntimeError: You need to use the eventlet server
```

Fix:
```bash
pip install eventlet
# If eventlet compilation fails on ARM:
pip install gevent
# Then edit dashboard/app.py to use gevent:
# socketio = SocketIO(app, async_mode='gevent')
```

**Threading mode fallback** (no eventlet/gevent needed, single-threaded):
```python
# In dashboard/app.py:
socketio = SocketIO(app, async_mode='threading')
```

### 9.2 Python binary mismatch

Termux installs Python as `python3`. Some scripts use `python`. The
`run_dashboard.sh` script uses bare `python` which may not be found.

**Check**:
```bash
which python3   # /data/data/com.termux/files/usr/bin/python3
which python    # may or may not exist
```

**Fix** (create symlink if missing):
```bash
ln -sf "$(which python3)" "${PREFIX}/bin/python"
```

The `test-build.sh` and `test-dev-server.sh` scripts detect both `python3`
and `python` automatically.

### 9.3 Flask running on port already used by another service

See [Section 7](#7-port--configuration-conflicts). The default `DASHBOARD_PORT=5000`
avoids conflicts with Node.js services.

---

## 10. PM2 on Termux

### Key differences from a Linux server deployment

| Concern | Linux server | Termux |
|---|---|---|
| Startup | `systemd` service | Termux:Boot + `pm2 resurrect` |
| Wake lock | Not needed | `termux-wake-lock` required |
| `pm2 startup` | Generates systemd unit | NOT supported — use `termux/install_boot.sh` |
| Log location | `/var/log` or `~/.pm2/logs` | `logs/` in repo dir (via `--log` flag) |
| Process persistence | Survives reboot via systemd | Requires Termux:Boot app |

### `pm2 startup` does NOT work in Termux

Running `pm2 startup` on Termux will attempt to generate a `systemd` unit
file, which does not exist in Termux. **Do not use it.** Use the provided
boot hook instead:

```bash
# Install Termux:Boot from F-Droid, open it once, then:
bash termux/install_boot.sh
```

### Restoring PM2 after reboot (manual)
```bash
pm2 resurrect   # restore last saved process list
# If nothing was saved:
bash termux/start.sh
```

### PM2 log rotation
```bash
pm2 install pm2-logrotate
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:retain 5
```

---

## 11. Interpreting Test Output

### Status indicators

| Symbol | Meaning |
|---|---|
| `[PASS]` (green) | Check passed successfully |
| `[FAIL]` (red) | Check failed — action required |
| `[WARN]` (yellow) | Non-fatal issue or advisory |
| `[SKIP]` (yellow) | Check not applicable / prerequisite missing |
| `[info]` (cyan) | Informational output only |

### Reading the final summary

```
  PASSED:  24
  FAILED:  2
  SKIPPED: 3

  RESULT: FAIL — 2 check(s) failed. See log for details.
```

The detailed log file (printed at the end) contains every check result with
timestamps. Review `[FAIL]` lines in the log to find the root cause.

### Minimal acceptable passing state

For the dev server to function, the following must pass:
- All **Section 2** (file integrity) checks in `test-dev-server.sh`
- All **Section 6** (npm install) checks in `test-build.sh`
- The `PORT`, `DIGITAL_TWIN_PORT`, `DASHBOARD_PORT`, `NODE_ENV` `.env` checks
- The `require('express')` and `require('dotenv')` smoke tests
- The `agent-x-core health endpoint` HTTP check (HTTP 200)

`[WARN]` results (e.g., wake lock not available, low disk, optional API keys
not set) do not block operation but should be addressed for production use.

---

## Appendix A: Quick Setup Verification Checklist

Run this quick verification after any `setup.sh` run:

```bash
# 1. Check binaries
node --version       # ≥ v18
npm --version        # ≥ 7
pm2 --version        # any recent
python3 --version    # ≥ 3.9 preferred

# 2. Check node_modules
ls agent-x-core/node_modules | head -5
ls digital-twin/node_modules | head -5

# 3. Check Python packages
python3 -c "import flask, flask_socketio, requests; print('OK')"

# 4. Check state files
cat memory/state.json | python3 -m json.tool > /dev/null && echo "valid JSON"
cat data/db.json | python3 -m json.tool > /dev/null && echo "valid JSON"

# 5. Check .env
grep PORT .env

# 6. Run build test (fast mode)
bash termux/test-build.sh --fast

# 7. Start services
bash termux/start.sh

# 8. Run server health checks
bash termux/test-dev-server.sh --no-start
```

---

## Appendix B: ARM Environment Information Template

When reporting a bug or test failure, include this information:

```bash
echo "=== Agent X Environment Report ==="
uname -a
echo "Node: $(node --version 2>/dev/null)"
echo "npm:  $(npm --version 2>/dev/null)"
echo "Python: $(python3 --version 2>/dev/null)"
echo "pm2: $(pm2 --version 2>/dev/null)"
echo "Arch: $(uname -m)"
echo "Android API: $(getprop ro.build.version.sdk 2>/dev/null || echo 'unknown')"
echo "Termux prefix: ${PREFIX:-unknown}"
free -m | head -2
df -h ~ | tail -1
cat .env | grep -v KEY | grep -v SECRET
```

---

*Generated by Agent X test suite. Last updated: see git log.*
