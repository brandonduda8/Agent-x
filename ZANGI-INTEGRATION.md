# Zangi Communication Layer — Integration Guide

This document covers the full design, configuration, and usage of the **Zangi
real-time messaging integration** for Agent X.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [File Map](#file-map)
4. [Configuration](#configuration)
5. [Agent ↔ Zangi Mapping](#agent--zangi-mapping)
6. [API Reference](#api-reference)
7. [Webhook Setup](#webhook-setup)
8. [Message Routing](#message-routing)
9. [Broadcast](#broadcast)
10. [Running the Standalone Listener](#running-the-standalone-listener)
11. [Adding a New Agent](#adding-a-new-agent)
12. [Testing Without Zangi Credentials](#testing-without-zangi-credentials)

---

## Overview

The Zangi layer gives every Agent X worker agent a real-time messaging
identity. Operators and external systems can:

- **Send commands** to any agent by posting to `/api/zangi/send`.
- **Broadcast** system-wide announcements to all agents at once.
- **Receive status updates and results** from agents via Zangi messages routed
  back through the webhook listener.

Zangi acts as the transport; Agent X task packets are the payload.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        Zangi Cloud                           │
│   User / Operator ──► Zangi App ──► Zangi API               │
└───────────────────────────┬──────────────────────────────────┘
                            │  Webhook POST
                            ▼
         ┌──────────────────────────────────┐
         │  agent-x-core  (Port 3000)       │
         │  POST /api/zangi/webhook         │  ← HMAC verified
         │  → zangi-webhook-handler.js      │
         │  → resolve agent via map         │
         │  → dispatch task to agent        │
         └──────────────┬───────────────────┘
                        │
          ┌─────────────┴──────────────────────────┐
          │  OR: standalone zangi-listener          │
          │  (Port 3002)                            │
          │  POST /webhook                          │
          │  → forward task to /v1/tasks on core    │
          └─────────────────────────────────────────┘

Outbound (Agent X → Zangi):
  agent-x-core
  POST /api/zangi/send     → ZangiClient.sendDirectMessage()
  POST /api/zangi/broadcast → ZangiClient.broadcast()
```

---

## File Map

| File | Purpose |
|---|---|
| `communication/zangi-client.js` | Zangi REST API wrapper (auth, retry, send, broadcast) |
| `communication/zangi-agent-map.js` | Agent ↔ Zangi ID mapping (in-memory + disk persistence) |
| `communication/zangi-webhook-handler.js` | Inbound event processor; HMAC verification; agent dispatch |
| `communication/packet-schema.js` | Updated with Zangi task types (`zangi:message`, `zangi:broadcast`) |
| `agent-x-core/routes/zangi.js` | Express router — all `/api/zangi/*` endpoints |
| `agent-x-core/index.js` | Mounts Zangi router at `/api/zangi` and `/v1/zangi` |
| `webhook-listener/zangi-listener.js` | Standalone listener service (Port 3002) |
| `data/zangi-agent-map.json` | Persistent mapping file (edit or update via API) |
| `.env.zangi.example` | Environment variable template |

---

## Configuration

Copy `.env.zangi.example` to `.env` (or merge into your existing `.env`) and
fill in your Zangi credentials:

```bash
cp .env.zangi.example .env
```

### Required variables

| Variable | Description |
|---|---|
| `ZANGI_API_KEY` | Zangi application API key |
| `ZANGI_API_SECRET` | Zangi application API secret |
| `ZANGI_APP_ID` | Zangi application / tenant ID |
| `ZANGI_BROADCAST_CHANNEL_ID` | Shared group channel for system-wide broadcasts |

### Optional variables

| Variable | Default | Description |
|---|---|---|
| `ZANGI_BASE_URL` | `https://api.zangi.com/v1` | Zangi REST API base URL |
| `ZANGI_WEBHOOK_SECRET` | _(none)_ | HMAC-SHA256 secret for webhook signature verification |
| `ZANGI_LISTENER_PORT` | `3002` | Port for the standalone listener |
| `AGENT_X_CORE_URL` | `http://localhost:3000` | Core URL used by standalone listener |
| `ZANGI_DEBUG` | `false` | Log all API requests/responses |
| `ZANGI_MAP_FILE` | `data/zangi-agent-map.json` | Path to agent map file |

### Per-agent variables

Each worker agent has two optional env vars:

```
ZANGI_USER_<NAME>=zangi-uid-xxxx       # Zangi user ID for DM
ZANGI_CHANNEL_<NAME>=zangi-chan-xxxx   # Per-agent private channel (preferred)
```

Where `<NAME>` is the upper-snake-case agent name, e.g.:
`ZANGI_USER_CONTENT_GENERATOR`, `ZANGI_CHANNEL_ORCHESTRATOR`.

These values are used when seeding the default `data/zangi-agent-map.json` if
no file exists yet. Once the file exists, update via the API or edit directly.

---

## Agent ↔ Zangi Mapping

The mapping lives in `data/zangi-agent-map.json` and is managed by
`communication/zangi-agent-map.js`.

### Schema

```json
{
  "agents": [
    {
      "agentId"       : "content-generator",
      "agentName"     : "content-generator",
      "zangiUserId"   : "zangi-uid-content-generator-xxxx",
      "zangiChannelId": "zangi-chan-content-generator-xxxx",
      "capabilities"  : ["draft", "email", "post"],
      "active"        : true
    }
  ]
}
```

### Special entry: `__broadcast__`

```json
{
  "agentId"       : "__broadcast__",
  "agentName"     : "broadcast",
  "zangiChannelId": "zangi-chan-broadcast-xxxx",
  "active"        : true
}
```

This entry's `zangiChannelId` is the shared group channel. Set it via
`ZANGI_BROADCAST_CHANNEL_ID` or the PATCH API.

### Routing priority (inbound messages)

For an inbound Zangi webhook event, the handler resolves the target agent in
this order:

1. `channelId` → lookup `zangiChannelId` in map
2. `to` (Zangi user ID) → lookup `zangiUserId` in map
3. `metadata.agentId` → lookup by Agent X ID
4. `metadata.agentName` → lookup by agent name
5. If none match → log warning, drop message

---

## API Reference

All endpoints are mounted at both `/api/zangi/*` and `/v1/zangi/*`.

---

### `POST /api/zangi/send`

Send a message to a specific agent.

**Body (send to mapped agent):**
```json
{
  "agentId" : "content-generator",
  "message" : "Draft a blog post about AI revenue tools",
  "type"    : "task",
  "metadata": { "priority": "high" }
}
```

**Body (send to raw Zangi user):**
```json
{
  "zangiUserId": "zangi-uid-xxxx",
  "message"    : "Hello from Agent X"
}
```

**Body (send to raw Zangi channel):**
```json
{
  "zangiChannelId": "zangi-chan-xxxx",
  "message"       : "Channel message"
}
```

**Response:**
```json
{
  "ok"           : true,
  "agent"        : "content-generator",
  "zangiResponse": { ... }
}
```

---

### `POST /api/zangi/broadcast`

Broadcast to the shared group channel (all agents).

**Body:**
```json
{
  "message"           : "System restart in 60 seconds",
  "broadcastChannelId": "zangi-chan-override-xxxx"
}
```

---

### `POST /api/zangi/webhook`

Inbound webhook endpoint called by Zangi. Do **not** call this directly.

- Verifies HMAC signature (`X-Zangi-Signature: sha256=<hex>`) if
  `ZANGI_WEBHOOK_SECRET` is set.
- Responds `200 OK` immediately (< 5 s), then processes asynchronously.
- Dispatches resolved task packets to the target agent.

---

### `GET /api/zangi/agents`

List all agent mappings.

Query params:
- `includeInactive=true` — include inactive agents

**Response:**
```json
{
  "agents": [ { ... } ],
  "count" : 7
}
```

---

### `GET /api/zangi/agents/:agentId`

Get the mapping for a specific agent (by ID or name).

---

### `POST /api/zangi/agents`

Add or update a mapping.

**Body:**
```json
{
  "agentId"       : "my-new-agent",
  "agentName"     : "my-new-agent",
  "zangiUserId"   : "zangi-uid-xxxx",
  "zangiChannelId": "zangi-chan-xxxx",
  "capabilities"  : ["custom"],
  "active"        : true
}
```

---

### `DELETE /api/zangi/agents/:agentId`

Remove a mapping.

---

### `POST /api/zangi/webhook/register`

Register this server's webhook URL with the Zangi API so Zangi knows where to
POST inbound events.

**Body:**
```json
{
  "webhookUrl": "https://your-server.example.com/api/zangi/webhook",
  "events"    : ["message.received", "message.delivered"]
}
```

---

### `GET /api/zangi/webhooks`

List all webhooks registered with Zangi for this app.

---

## Webhook Setup

### 1. Register with Zangi

After deploying, call the registration endpoint once:

```bash
curl -X POST http://localhost:3000/api/zangi/webhook/register \
  -H 'Content-Type: application/json' \
  -d '{"webhookUrl": "https://YOUR_PUBLIC_HOST/api/zangi/webhook"}'
```

Or use the Zangi developer portal to set the webhook URL manually.

### 2. Configure HMAC secret

Set `ZANGI_WEBHOOK_SECRET` to the secret shown in the Zangi portal. The handler
validates every inbound request using HMAC-SHA256:

```
X-Zangi-Signature: sha256=<hex-digest-of-body>
```

If the secret is not set, verification is skipped (development mode only).

### 3. Event types handled

| Zangi event | Action |
|---|---|
| `message.received` | Resolve agent, dispatch task |
| `message.delivered` | Log acknowledgement |
| `message.read` | Log acknowledgement |
| Broadcast channel message | Dispatch to all active agents |
| Unknown | Log and ignore |

---

## Broadcast

To send a message to every active agent simultaneously:

```bash
curl -X POST http://localhost:3000/api/zangi/broadcast \
  -H 'Content-Type: application/json' \
  -d '{"message": "Entering maintenance mode"}'
```

This posts to the shared Zangi group channel (`ZANGI_BROADCAST_CHANNEL_ID`).
The `zangi-webhook-handler.js` also handles inbound messages on this channel
by dispatching a `zangi:broadcast` task to every active agent.

---

## Running the Standalone Listener

If you need a separate dedicated service for Zangi webhooks (e.g. different
public port, separate process isolation):

```bash
cd webhook-listener
ZANGI_LISTENER_PORT=3002 node zangi-listener.js
```

The standalone listener:
- Listens on port `ZANGI_LISTENER_PORT` (default: `3002`).
- Exposes `POST /webhook` and `POST /zangi/webhook`.
- Resolves the target agent using the shared `zangi-agent-map.js`.
- Forwards task packets to `AGENT_X_CORE_URL/v1/tasks` (default: `http://localhost:3000/v1/tasks`).

Endpoints:
- `GET  /health` — liveness check
- `GET  /agents` — view current mappings
- `POST /agents/reload` — reload map from disk without restart

---

## Adding a New Agent

### Step 1: Create the Zangi user and channel in the Zangi portal

Note down the `zangiUserId` and `zangiChannelId`.

### Step 2: Add the mapping via API

```bash
curl -X POST http://localhost:3000/api/zangi/agents \
  -H 'Content-Type: application/json' \
  -d '{
    "agentId"       : "my-revenue-agent",
    "agentName"     : "revenue-agent",
    "zangiUserId"   : "zangi-uid-revenue-xxxx",
    "zangiChannelId": "zangi-chan-revenue-xxxx",
    "capabilities"  : ["revenue", "strategy"],
    "active"        : true
  }'
```

The change is persisted to `data/zangi-agent-map.json` immediately.

### Step 3: Register an in-process handler (optional)

If the agent runs in the same Node.js process as `agent-x-core`, register a
handler so tasks are dispatched in-memory without an HTTP round-trip:

```js
const { registerAgentHandler } = require('./routes/zangi');

registerAgentHandler('my-revenue-agent', async (task) => {
  // task is a full Agent X packet (from packet-schema.js)
  console.log('Revenue agent received task:', task);
  // ... process the task
});
```

---

## Testing Without Zangi Credentials

You can exercise the routing logic end-to-end without a real Zangi account:

### Test inbound webhook routing

```bash
# Simulate a Zangi webhook event hitting the listener
curl -X POST http://localhost:3000/api/zangi/webhook \
  -H 'Content-Type: application/json' \
  -d '{
    "type"      : "message.received",
    "from"      : "zangi-uid-operator",
    "to"        : "zangi-uid-content-generator-xxxx",
    "channelId" : null,
    "message"   : "Draft a blog post",
    "metadata"  : { "messageType": "task" }
  }'
```

### Test outbound send (will fail without real credentials but exercises routing)

```bash
curl -X POST http://localhost:3000/api/zangi/send \
  -H 'Content-Type: application/json' \
  -d '{"agentId": "content-generator", "message": "Hello!"}'
```

### Test agent map

```bash
# List all mappings
curl http://localhost:3000/api/zangi/agents

# Get specific agent
curl http://localhost:3000/api/zangi/agents/content-generator

# Add a test mapping
curl -X POST http://localhost:3000/api/zangi/agents \
  -H 'Content-Type: application/json' \
  -d '{"agentId":"test-agent","zangiUserId":"uid-test","active":true}'
```

---

## Docker / Compose

The standalone Zangi listener can be added to `docker-compose.yml`:

```yaml
zangi-listener:
  build:
    context: .
    dockerfile: deployment/Dockerfile
  command: node webhook-listener/zangi-listener.js
  ports:
    - "3002:3002"
  environment:
    - ZANGI_API_KEY=${ZANGI_API_KEY}
    - ZANGI_API_SECRET=${ZANGI_API_SECRET}
    - ZANGI_APP_ID=${ZANGI_APP_ID}
    - ZANGI_WEBHOOK_SECRET=${ZANGI_WEBHOOK_SECRET}
    - ZANGI_BROADCAST_CHANNEL_ID=${ZANGI_BROADCAST_CHANNEL_ID}
    - ZANGI_LISTENER_PORT=3002
    - AGENT_X_CORE_URL=http://agent-x-core:3000
  depends_on:
    - agent-x-core
  restart: unless-stopped
```
