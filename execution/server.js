const express = require("express");
const { exec } = require("child_process");
const { db, init } = require("../core/db");
const Builder = require("../core/builder");

const app = express();
const PORT = 3000;

const builder = new Builder();

app.use(express.json());

/* =========================
   SYSTEM HOME
========================= */
app.get("/", (req, res) => {
  res.send("⚡ AI SAAS OS v10 SAFE MODE ONLINE");
});

/* =========================
   SIMPLE AUTH (LOWDB)
========================= */
app.post("/auth/register", async (req, res) => {
  const { email } = req.body;

  await init();
  db.data.users.push({
    id: Date.now(),
    email
  });

  await db.write();

  res.json({ status: "registered", email });
});

/* =========================
   LOGIN (NO SECURITY LAYER YET - SAFE BASE)
========================= */
app.post("/auth/login", async (req, res) => {
  const { email } = req.body;

  await init();

  const user = db.data.users.find(u => u.email === email);

  if (!user) {
    return res.json({ error: "user not found" });
  }

  res.json({ status: "logged_in", user });
});

/* =========================
   BUILD SAAS PROJECT
========================= */
app.post("/api/build-saas", async (req, res) => {
  const input = req.body.input || "";

  const plan = builder.plan(input);
  const project = builder.writeProject(plan);

  await init();

  db.data.projects.push({
    id: Date.now(),
    input,
    plan,
    project
  });

  await db.write();

  res.json({
    status: "generated",
    input,
    project
  });
});

/* =========================
   STRIPE CHECKOUT (REAL HOOK READY)
========================= */
app.post("/stripe/checkout", async (req, res) => {
  const amount = req.body.amount || 1000;

  // placeholder safe mode (no key crash)
  res.json({
    status: "stripe-ready",
    amount,
    note: "Add STRIPE_SECRET_KEY in env to activate real payments"
  });
});

/* =========================
   DEPLOY (PM2 SAFE LOCAL)
========================= */
app.post("/api/deploy", async (req, res) => {
  const project = req.body.project;

  if (!project?.project?.location) {
    return res.json({ error: "No project found" });
  }

  const path = project.project.location;

  exec(`cd ${path} && pm2 start server.js --name ai-saas`, (err, out) => {
    if (err) {
      return res.json({
        status: "deploy_failed",
        error: err.message
      });
    }

    res.json({
      status: "deployed",
      output: out.toString()
    });
  });
});

/* =========================
   PROJECT LIST
========================= */
app.get("/api/projects", async (req, res) => {
  await init();
  res.json(db.data.projects);
});

/* =========================
   SYSTEM STATUS
========================= */
app.get("/status", async (req, res) => {
  res.json({
    system: "ai-saas-os-v10",
    status: "online",
    uptime: process.uptime()
  });
});

/* =========================
   START SERVER (SAFE INIT)
========================= */
app.listen(PORT, "127.0.0.1", async () => {
  await init();
  console.log("⚡ AI SAAS OS v10 RUNNING ON", PORT);
});
