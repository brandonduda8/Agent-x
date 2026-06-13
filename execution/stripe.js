const Stripe = require("stripe");
const Memory = require("../core/memory");

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
const memory = new Memory();

// CREATE CHECKOUT SESSION (REAL MONEY ENTRY POINT)
async function createCheckoutSession(price = 29.99) {
  const session = await stripe.checkout.sessions.create({
    payment_method_types: ["card"],
    mode: "payment",
    line_items: [
      {
        price_data: {
          currency: "usd",
          product_data: {
            name: "AI Income System Access"
          },
          unit_amount: Math.round(price * 100)
        },
        quantity: 1
      }
    ],
    success_url: "http://localhost:3000/success",
    cancel_url: "http://localhost:3000/cancel"
  });

  return session.url;
}

// HANDLE WEBHOOK EVENTS
async function handleStripeEvent(event) {
  const type = event.type;

  // PAYMENT SUCCESS
  if (type === "checkout.session.completed") {
    const session = event.data.object;

    const amount = session.amount_total / 100;

    memory.addRevenue(amount, {
      source: "stripe_checkout",
      sessionId: session.id
    });

    console.log("[REVENUE]", amount);
  }

  // SAVE EVENT HISTORY
  memory.db.events.push({
    type,
    time: Date.now(),
    raw: event
  });

  memory.save();
}

module.exports = {
  createCheckoutSession,
  handleStripeEvent
};
