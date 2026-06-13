const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json({ limit: '10mb' }));

const PRODUCTS_DIR = path.join(__dirname, 'catalog');
const DELIVERABLES_DIR = path.join(__dirname, 'deliverables');
const STATE_DIR = path.join(__dirname, 'state');

function ensureDirs() {
  [PRODUCTS_DIR, DELIVERABLES_DIR, STATE_DIR].forEach(dir => {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  });
}

ensureDirs();

// Load product catalog
function loadProducts() {
  try {
    return JSON.parse(fs.readFileSync(path.join(PRODUCTS_DIR, 'catalog.json'), 'utf8'));
  } catch (e) {
    return [];
  }
}

// Save product catalog
function saveProducts(products) {
  fs.writeFileSync(path.join(PRODUCTS_DIR, 'catalog.json'), JSON.stringify(products, null, 2), 'utf8');
}

app.get('/health', (req, res) => {
  res.json({ service: 'agent-x-products', uptime: process.uptime(), products: loadProducts().length });
});

app.get('/v1/products', (req, res) => {
  const products = loadProducts();
  res.json({ ok: true, count: products.length, products });
});

app.get('/v1/products/:id', (req, res) => {
  const product = loadProducts().find(p => p.id === req.params.id);
  if (!product) return res.status(404).json({ error: 'Product not found' });
  res.json({ ok: true, product });
});

app.post('/v1/products', (req, res) => {
  const { name, description, price_cents, type, tags } = req.body || {};
  if (!name || !price_cents || !type) {
    return res.status(400).json({ ok: false, error: 'name, price_cents, and type are required' });
  }

  const products = loadProducts();
  const product = {
    id: `prod_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 8)}`,
    name,
    description: description || '',
    price_cents: typeof price_cents === 'number' ? price_cents : parseInt(price_cents, 10),
    currency: 'usd',
    type,
    tags: Array.isArray(tags) ? tags : [],
    createdAt: new Date().toISOString(),
    status: 'active'
  };
  products.push(product);
  saveProducts(products);

  res.status(201).json({ ok: true, product });
});

app.delete('/v1/products/:id', (req, res) => {
  const id = req.params.id;
  let products = loadProducts();
  const before = products.length;
  products = products.filter(p => p.id !== id);
  if (products.length === before.length) {
    return res.status(404).json({ error: 'Product not found' });
  }
  saveProducts(products);
  res.json({ ok: true, deleted: id });
});

// Deliver downloadable product (mock fulfillment)
app.get('/v1/deliver/:orderId', (req, res) => {
  const orderFile = path.join(STATE_DIR, 'orders.json');
  if (!fs.existsSync(orderFile)) {
    return res.status(404).json({ error: 'Order not found' });
  }
  const orders = JSON.parse(fs.readFileSync(orderFile, 'utf8'));
  const order = orders.find(o => o.id === req.params.orderId || o.productId === req.params.orderId);
  if (!order) {
    return res.status(404).json({ error: 'Order not found' });
  }
  res.json({
    ok: true,
    order,
    download: {
      url: `/v1/deliver/${order.id}/file`,
      expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
    }
  });
});

app.get('/v1/deliver/:orderId/file', (req, res) => {
  const orderFile = path.join(STATE_DIR, 'orders.json');
  const orders = JSON.parse(fs.readFileSync(orderFile, 'utf8'));
  const order = orders.find(o => o.id === req.params.orderId);
  if (!order) {
    return res.status(404).json({ error: 'Order not found' });
  }

  const product = loadProducts().find(p => p.id === order.productId);
  if (!product) {
    return res.status(404).json({ error: 'Product not found' });
  }

  const deliverablePath = path.join(DELIVERABLES_DIR, `${order.id}.json`);
  if (!fs.existsSync(deliverablePath)) {
    return res.status(404).json({ error: 'Deliverable not ready' });
  }

  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Content-Disposition', `attachment; filename="${product.id}-deliverable.json"`);
  res.send(fs.readFileSync(deliverablePath, 'utf8'));
});

const PORT = process.env.PORT || 3003;
app.listen(PORT, () => {
  console.log(`[PRODUCTS] online http://0.0.0.0:${PORT}`);
});
