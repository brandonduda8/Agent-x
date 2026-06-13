# Agent X — Python/Node.js Stack Selection Fix

## Issue
Earlier scaffolding defaulted to Node.js Express, which conflicts with the request to produce Python/Node.js options and with the Python project path you shared.

## Resolved approach
Maintain two build-ready skeletons:
- Node: existing `agent-x-core/`, `digital-twin/`, `communication/`
- Python: new `python-skeleton/` with FastAPI sample

## Action
Add `python-skeleton/` with a minimal FastAPI service, then continue blueprint/deployment generation in parallel.
