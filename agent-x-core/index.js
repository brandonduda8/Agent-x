require('dotenv').config();
const express = require('express');
const cors = require('cors');
const axios = require('axios');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json({ limit: '10mb' }));

const TASKS_FILE = path.join(__dirname, 'tasks.json');
const PRODUCTS_FILE = path.join(__dirname, '..', 'products', 'catalog', 'catalog.json');

function readTasks() {
  try {
    if (!fs.existsSync(TASKS_FILE)) return [];
    return JSON.parse(fs.readFileSync(TASKS_FILE, 'utf8'));
  } catch (e) {
    console.error('Failed to read tasks:', e.message);
    return [];
  }
}

function readProducts() {
  try {
    if (!fs.existsSync(PRODUCTS_FILE)) return [];
    const raw = JSON.parse(fs.readFileSync(PRODUCTS_FILE, 'utf8'));
    return Array.isArray(raw.catalog) ? raw.catalog : [];
  } catch (e) {
    console.error('Failed to read products:', e.message);
    return [];
  }
}

function writeTasks(tasks) {
  try {
    fs.writeFileSync(TASKS_FILE, JSON.stringify(tasks, null, 2), 'utf8');
  } catch (e) {
    console.error('Failed to write tasks:', e.message);
  }
}

function appendEvent(taskId, event) {
  const tasks = readTasks();
  const task = tasks.find(t => t.id === taskId);
  if (!task) return;
  task.events.push({ ...event, ts: new Date().toISOString() });
  task.status = event.status || task.status;
  task.updatedAt = new Date().toISOString();
  writeTasks(tasks);
}

const OVERMIND_URL = process.env.OVERMIND_URL || 'http://localhost:3010';

async function postToOvermind(event) {
  try {
    await axios.post(`${OVERMIND_URL}/events`, event, { timeout: 5000 });
  } catch (e) {
    // non-fatal: Overmind may be restarting
  }
}

app.get('/health', (req, res) => {
  res.json({
    service: 'agent-x-command-center',
    version: '1.0.0',
    uptime: process.uptime(),
    tasks: readTasks().length
  });
});

app.post('/v1/tasks', async (req, res) => {
  const task = {
    id: uuidv4(),
    type: req.body.type || 'generic',
    payload: req.body.payload || {},
    status: 'queued',
    priority: req.body.priority || 'normal',
    webhook: req.body.webhook || null,
    createdById: req.body.createdById || 'system',
    events: [{ type: 'created', detail: 'Task queued for execution' }],
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    completedAt: null,
    result: null
  };

  const tasks = readTasks();
  tasks.push(task);
  writeTasks(tasks);

  console.log('[TASK]', task.id, task.type, task.status);

  setImmediate(() => executeTask(task));
  res.status(202).json({ taskId: task.id, status: task.status });
});

app.get('/v1/products', (req, res) => {
  const products = readProducts();
  res.json({ products });
});

app.get('/v1/tasks/:id', (req, res) => {
  const tasks = readTasks();
  const task = tasks.find(t => t.id === req.params.id);
  if (!task) return res.status(404).json({ error: 'Task not found' });
  res.json(task);
});

app.get('/v1/tasks', (req, res) => {
  const tasks = readTasks();
  const limit = parseInt(req.query.limit || '50');
  const offset = parseInt(req.query.offset || '0');
  const type = req.query.type;
  let filtered = type ? tasks.filter(t => t.type === type) : tasks;
  res.json(filtered.slice(offset, offset + limit));
});

async function executeTask(task) {
  const tasks = readTasks();
  const idx = tasks.findIndex(t => t.id === task.id);
  if (idx === -1) return;
  tasks[idx].status = 'running';
  tasks[idx].events.push({ type: 'started' });
  writeTasks(tasks);
  postToOvermind({ type: 'agent_x_task_started', taskId: task.id, source: 'agent-x-core' });

  try {
    const result = await callDigitalTwin(task);
    tasks[idx].status = 'completed';
    tasks[idx].result = result;
    tasks[idx].events.push({ type: 'completed', detail: result?.summary || 'Task finished' });
    tasks[idx].completedAt = new Date().toISOString();
    writeTasks(tasks);
    postToOvermind({ type: 'agent_x_task_completed', taskId: task.id, source: 'agent-x-core', result });

    if (task.webhook) {
      await axios.post(task.webhook, {
        taskId: task.id,
        status: 'completed',
        result
      }).catch(e => console.error('[WEBHOOK FAIL]', e.message));
    }
  } catch (err) {
    tasks[idx].status = 'failed';
    tasks[idx].events.push({ type: 'error', detail: err.message });
    tasks[idx].updatedAt = new Date().toISOString();
    writeTasks(tasks);
    postToOvermind({ type: 'agent_x_task_failed', taskId: task.id, source: 'agent-x-core', error: err.message });

    if (task.webhook) {
      await axios.post(task.webhook, {
        taskId: task.id,
        status: 'failed',
        error: err.message
      }).catch(e => console.error('[WEBHOOK FAIL]', e.message));
    }
  }
}

async function callDigitalTwin(task) {
  const twinUrl = process.env.DIGITAL_TWIN_URL || 'http://localhost:3001';
  const response = await axios.post(`${twinUrl}/execute`, {
    taskId: task.id,
    type: task.type,
    payload: task.payload
  }, { timeout: 120_000 });
  return response.data;
}

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`[AGENT X CORE] online http://0.0.0.0:${PORT}`);
  console.log(`[TWIN INTEGRATION] target ${process.env.DIGITAL_TWIN_URL || 'http://localhost:3001'}`);
});
