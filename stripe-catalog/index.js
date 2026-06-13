const express = require('express');
const app = express();
app.use(express.json({ limit: '10mb' }));

const PORT = 3002;

const catalog = require('./index');

app.use(cors());
app.use(express.json());

// List products
app.get('/v1/products', (req, res) => {
  const products = [
    {
      id: 'ai-automation-playbook',
      name: 'AI Automation Playbook for Founders',
      description: 'Step-by-step guide to building autonomous income workflows with AI agents',
      price_cents: 4900,
      currency: 'usd',
      tags: ['automation', 'business', 'ai']
    },
    {
      id: 'social-templates',
      name: 'Social Media Template Pack',
      description: '50+ templates for LinkedIn, Twitter, Instagram growth',
      price_cents: 2900,
      currency: 'usd',
      tags: ['social', 'templates']
    },
    {
      id: 'newsletter-swipes',
      name: 'Newsletter Swipe File',
      description: 'High-converting email subject lines and CTAs',
      price_cents: 1900,
      currency: 'usd',
      tags: ['email', 'copywriting']
    }
  ];
  res.json({ ok: true, products });
});

// Create checkout session
app.post('/v1/checkout', (req, res) => {
  const productId = req.body?.productId;
  if (!productId) return res.status(400).json({ ok: false, error: 'productId required' });
  const sessionId = 'cs_mock_' + Math.random().toString(36).slice(2, 10);
  console.log(`Checkout created: ${sessionId}`);
  res.json({
    ok: true,
    mode: 'mock',
    sessionId,
    product: productId,
    credits: 1,
    status: 'paid_simulated'
  });
});

app.get('/v1/checkout/mock-success', (req, res) => {
  const sid = req.query.sessionId;
  res.send(`
    <html>
      <body style="font-family: system-ui; max-width: 600px; margin: 40px auto; text-align: center;">
        <h1 style="color: #22c55e;">Mock payment successful</h1>
        <p>Session: <code>${sid || ''}</code></p>
        <p>In production, this is where Stripe redirects the buyer after payment.</p>
      </body>
    </html>
  `);
});

// Delivery
app.get('/v1/fulfill/:sessionId', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.send(JSON.stringify({
    ok: true,
    mode: 'mock',
    delivery: {
      status: 'queued',
      channel: 'download',
      issuedAt: new Date().toISOString(),
      note: 'In live mode, this would return the digital asset or a download link.'
    }
  }, null, 2));
});

const listener = app.listen(PORT, () => {
  console.log(`[STRIPE CATALOG] online http://0.0.0.0:${PORT}`);
});

process.on('SIGTERM', () => listener.close(() => process.exit(0)));
process.on('SIGINT', () => listener.close(() => process.exit(0)));
