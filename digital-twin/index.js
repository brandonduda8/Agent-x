require("dotenv").config();
const express = require("express");
const cors = require("cors");
const axios = require("axios");
const fs = require("fs");
const path = require("path");

const OVERMIND_URL = process.env.OVERMIND_URL || "http://localhost:3010";

async function postToOvermind(event) {
  try {
    await axios.post(`${OVERMIND_URL}/events`, event, { timeout: 5000 });
  } catch (e) {
    // non-fatal
  }
}

const app = express();
app.use(cors());
app.use(express.json({ limit: "10mb" }));

const STATE_DIR = path.join(__dirname, "state");
const ARTIFACTS_DIR = path.join(__dirname, "artifacts");

function ensureDirs() {
  if (!fs.existsSync(STATE_DIR)) fs.mkdirSync(STATE_DIR, { recursive: true });
  if (!fs.existsSync(ARTIFACTS_DIR)) fs.mkdirSync(ARTIFACTS_DIR, { recursive: true });
}

/* -----------------------------
   STATE MANAGEMENT
------------------------------*/

function recordExecution(exec) {
  ensureDirs();
  const file = path.join(STATE_DIR, `${exec.taskId}.json`);
  fs.writeFileSync(file, JSON.stringify(exec, null, 2));
}

function loadExecution(taskId) {
  const file = path.join(STATE_DIR, `${taskId}.json`);
  if (!fs.existsSync(file)) return null;
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

/* -----------------------------
   ARTIFACT SYSTEM
------------------------------*/

function saveArtifact(taskId, kind, payload) {
  ensureDirs();
  const file = path.join(ARTIFACTS_DIR, `${taskId}-${kind}.json`);
  fs.writeFileSync(file, JSON.stringify(payload, null, 2));
  return file;
}

/* -----------------------------
   PIPELINES (MINIMAL SAFE STUBS)
------------------------------*/

async function pipelineContent({ taskId, payload }) {
  const draft = {
    title: payload?.topic || "Untitled",
    audience: payload?.audience || "general",
    body: "Auto-generated content draft from Digital Twin.",
    created: new Date().toISOString(),
  };

  const artifact = saveArtifact(taskId, "content-draft", draft);

  return {
    ok: true,
    type: "content",
    artifact,
    draft,
  };
}

async function pipelineData({ taskId, payload }) {
  return {
    ok: true,
    type: "data",
    message: "Data pipeline executed",
    received: payload,
  };
}

async function pipelineCustom({ taskId, payload }) {
  return {
    ok: true,
    type: "custom",
    message: "Custom task executed",
    payload,
  };
}

/* -----------------------------
   EXECUTION ROUTE
------------------------------*/

app.post("/execute", async (req, res) => {
  const { taskId, type, payload } = req.body;

  console.log("[DIGITAL TWIN]", taskId, type);

  const exec = {
    taskId,
    type,
    receivedAt: new Date().toISOString(),
    status: "processing",
    steps: [],
    artifacts: [],
    output: null,
  };

  recordExecution(exec);

  try {
    let result;

    if (["content-generation", "article", "post"].includes(type)) {
      result = await pipelineContent({ taskId, payload });
    } else if (["data-ingest", "aggregate", "sync"].includes(type)) {
      result = await pipelineData({ taskId, payload });
    } else {
      result = await pipelineCustom({ taskId, payload });
    }

    exec.status = "completed";
    exec.output = result;

    recordExecution(exec);

    await postToOvermind({
      source: "digital-twin",
      taskId,
      result,
    });

    res.json({
      ok: true,
      taskId,
      result,
    });
  } catch (err) {
    exec.status = "failed";
    exec.error = err.message;

    recordExecution(exec);

    res.status(500).json({
      ok: false,
      error: err.message,
    });
  }
});

/* -----------------------------
   HEALTH CHECK
------------------------------*/

app.get("/", (req, res) => {
  res.send("Digital Twin Online");
});

const PORT = process.env.PORT || 3001;

app.listen(PORT, "0.0.0.0", () => {
  console.log(`[DIGITAL TWIN] online http://0.0.0.0:${PORT}`);
});
