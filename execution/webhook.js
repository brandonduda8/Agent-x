const express = require("express");
const path = require("path");
const Memory = require("../core/memory");

require("dotenv").config({
  path: path.resolve(__dirname, "../.env")
});

const app = express();
const memory = new Memory();

app.use(express.json());

// HEALTH CHECK
app.get("/", (req, res) => {
  res.send("AI Income Engine Running");
});

// WEBHOOK ENDPOINT
app.post("/webhook", (req, res) => {
  try {
    console.log("[WEBHOOK]", req.body);

    const event = req.body || {};

    // SAFE MEMORY WRITE (prevents crash if method missing)
    if (typeof memory.recordEvent === "function") {
      memory.recordEvent("stripe_event", event);
    }

    res.json({ ok: true });
  } catch (err) {
    console.log("WEBHOOK ERROR:", err.message);
    res.status(500).json({ error: "failed" });
  }
});

// FORCE BIND (THIS IS CRITICAL)
const PORT = 3000;

const server = app.listen(PORT, "127.0.0.1", () => {
  console.log("⚡ AI Income Engine running on port", PORT);
});

server.on("error", (err) => {
  console.log("SERVER ERROR:", err.message);
});
