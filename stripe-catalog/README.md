# Stripe Express Catalog

Run:
```bash
cd ~/agent-x/stripe-catalog
cp .env.example .env
npm install express cors uuid dotenv
npm start
```

Required env vars:
- STRIPE_SECRET_KEY
- STRIPE_WEBHOOK_SECRET
- PORT=3002

Endpoints:
- GET /v1/products
- POST /v1/checkout
- POST /v1/webhooks/stripe
- GET /v1/fulfill/:sessionId
