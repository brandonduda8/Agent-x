const express = require('express');
const app = express();
app.use(express.json({ limit: '10mb' }));
const PORT = 4000;

const received = [];

app.post('/ingest', (req, res) => {
  const entry = { at: new Date().toISOString(), body: req.body };
  received.push(entry);
  res.status(200).json({ ok: true, received: entry });
});

app.get('/received', (req, res) => {
  res.json({ count: received.length, items: received });
});

app.listen(PORT, () => console.log(`[WEBHOOK LISTENER] http://0.0.0.0:${PORT}`));
