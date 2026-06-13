# Agent X — Autonomous Income Infrastructure

## Structure
- `agent-x-core/` — command center (Node.js + Express)
- `digital-twin/` — execution layer with pipelines + artifacts
- `communication/` — shared sender logic + packet schema
- `blueprints/` — reusable revenue modules
- `deployment/` — service manifests for Termux / Linux

## Quick start
1. `cd agent-x-core && node index.js`
2. `cd digital-twin && node index.js`
3. Send task: `POST http://localhost:3000/v1/tasks`

## Status
Status file: `agent-x/STATUS-ARCHITECTURE.md`
