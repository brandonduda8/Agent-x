# Agent X Worker Agents

Each agent is a standalone stdio JSON process. Use it directly or wrap it with a router.

## Usage protocol
Send one envelope per line over stdin:
```json
{"action":"draft","requestId":"abc123","payload":{"topic":"test","audience":"founders","variant":"long"}}
```
Expected response:
```json
{"ok":true,"requestId":"abc123","result":{...}}
```

## Agents
- `api-socket.js` — outbound HTTP GET/POST with headers and timeout control.
- `infrastructure.js` — service lifecycle, env sanity checks, network probes.
- `content-generator.js` — drafts copy, posts, and emails for monetization.
- `data-aggregator.js` — fetches datasets, summarizes health, returns artifacts.

## Revenue purpose
- `content-generator` → outreach templates, affiliate briefs, publisher-ready drafts.
- `data-aggregator` → lead sources, price signals, market summaries.

## Usage patterns
Problem: running an agent detached in software and waiting for no exit breaks stdio feedback.
Solution: one-shot launch patterns that preserve lifecycle visibility.

Examples matching your exact environment:
* api-socket: `printf '%s' '{"action":"get","requestId":"t1","payload":{"url":"https://httpbin.org/get"}}' | node ~/agent-x/agent-x-core/agents/api-socket.js`
* content-generator: `printf '%s' '{"action":"draft","requestId":"c1","payload":{"topic":"automation","audience":"founders","variant":"short"}}' | node ~/agent-x/agent-x-core/agents/content-generator.js`
* data-aggregator: `printf '%s' '{"action":"aggregate","requestId":"d1","payload":{"sourceUrls":["https://example.com"],"timeWindow":"24h"}}' | node ~/agent-x/agent-x-core/agents/data-aggregator.js`

Success criteria:
- stdout contains `{"ok":true,"requestId":"...","result":{...}}`
- no detached process left running by default
- failures return `{"ok":false,"error":"..."}`

Deployment notes:
- use the launch examples above for debug
- use a router or orchestrator for production pipelines
- run `node --check` against agent files in `~/agent-x/agent-x-core/agents` before shipping
