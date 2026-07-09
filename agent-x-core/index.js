/**
 * agent-x-core/index.js
 * =============================================================================
 * Agent X — Command Center (Port 3000)
 *
 * Express API server that mounts all subsystem routers and starts
 * background agents (Hermes job-discovery, registry heartbeat monitor, etc.)
 * =============================================================================
 */

"use strict";

require("dotenv").config({ path: require("path").resolve(__dirname, "..", ".env") });

const express = require("express");
const cors    = require("cors");
const path    = require("path");

const app  = express();
const PORT = process.env.PORT || 3000;

// ---------------------------------------------------------------------------
// Middleware
// ---------------------------------------------------------------------------
app.use(cors());
app.use(express.json({ limit: "2mb" }));
app.use(express.urlencoded({ extended: true }));

// ---------------------------------------------------------------------------
// Routes
// ---------------------------------------------------------------------------

// Registry & heartbeat
try {
  const registryApi = require("./registry/registry-api");
  app.use("/v1/registry", registryApi);
  console.log("[Core] Mounted: /v1/registry");
} catch (e) {
  console.warn("[Core] registry-api not loaded:", e.message);
}

// Agent upgrade & config versioning
try {
  const upgradeApi = require("./routes/upgrade");
  app.use("/v1/upgrade", upgradeApi);
  console.log("[Core] Mounted: /v1/upgrade");
} catch (e) {
  console.warn("[Core] upgrade route not loaded:", e.message);
}

// Zangi communication layer
try {
  const zangiApi = require("./routes/zangi");
  app.use("/v1/zangi", zangiApi);
  console.log("[Core] Mounted: /v1/zangi");
} catch (e) {
  console.warn("[Core] zangi route not loaded:", e.message);
}

// Agent management (generic)
try {
  const agentsApi = require("./routes/agents");
  app.use("/v1/agents", agentsApi);
  console.log("[Core] Mounted: /v1/agents");
} catch (e) {
  console.warn("[Core] agents route not loaded:", e.message);
}

// ── Hermes Job Discovery & Matching ────────────────────────────────────────
const hermesRouter = require("./routes/hermes");
app.use("/api/hermes", hermesRouter);
console.log("[Core] Mounted: /api/hermes");

// ---------------------------------------------------------------------------
// Health / root
// ---------------------------------------------------------------------------
app.get("/", (_req, res) => {
  res.json({
    service : "agent-x-core",
    version : require("./package.json").version || "1.0.0",
    status  : "ok",
    uptime  : process.uptime(),
    routes  : [
      "GET  /",
      "GET  /health",
      "GET  /v1/registry/agents",
      "POST /v1/registry/agents/register",
      "POST /v1/registry/agents/:id/heartbeat",
      "DELETE /v1/registry/agents/:id",
      "GET  /api/hermes/health",
      "GET  /api/hermes/jobs",
      "POST /api/hermes/jobs",
      "GET  /api/hermes/jobs/:id",
      "PATCH /api/hermes/jobs/:id",
      "DELETE /api/hermes/jobs/:id",
      "GET  /api/hermes/jobs/:id/rank",
      "POST /api/hermes/scan",
      "POST /api/hermes/match",
      "GET  /api/hermes/stats",
    ],
  });
});

app.get("/health", (_req, res) => {
  res.json({ status: "ok", uptime: process.uptime(), ts: new Date().toISOString() });
});

// ---------------------------------------------------------------------------
// Global error handler
// ---------------------------------------------------------------------------
// eslint-disable-next-line no-unused-vars
app.use((err, _req, res, _next) => {
  console.error("[Core] Unhandled error:", err);
  res.status(500).json({ ok: false, error: err.message || "Internal server error" });
});

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------
app.listen(PORT, () => {
  console.log(`\n[Core] Agent X Core running on port ${PORT}\n`);

  // Start Agent Hermes after the server is up
  try {
    const hermes = require("../hermes/hermes-agent");
    hermes.start();
    console.log("[Core] Agent Hermes started.");
  } catch (e) {
    console.warn("[Core] Could not start Agent Hermes:", e.message);
  }
});

module.exports = app; // for testing
