const fs = require("fs");

class EventBus {
  constructor(memory) {
    this.memory = memory;
  }

  emit(event, payload = {}) {
    console.log("[EVENT]", event, payload);

    switch (event) {
      case "order_created":
        return this.onOrderCreated(payload);

      case "payment_received":
        return this.onPaymentReceived(payload);

      case "conversion_failed":
        return this.onFailure(payload);

      case "content_posted":
        return this.onContent(payload);

      default:
        return { status: "ignored_event", event };
    }
  }

  onOrderCreated(order) {
    const db = this.memory.load();

    db.orders.push({
      id: Date.now(),
      status: "pending",
      ...order
    });

    this.memory.save(db);

    return {
      status: "order_logged",
      order
    };
  }

  onPaymentReceived({ orderId, amount }) {
    const db = this.memory.load();

    db.revenue.push({
      id: Date.now(),
      orderId,
      amount
    });

    const order = db.orders.find(o => o.id === orderId);
    if (order) order.status = "paid";

    db.learning.totalRevenue += amount;
    db.learning.totalOrders = db.orders.length;

    const paid = db.orders.filter(o => o.status === "paid").length;
    db.learning.winRate = paid / db.orders.length;

    this.memory.save(db);

    return {
      status: "revenue_logged",
      winRate: db.learning.winRate
    };
  }

  onFailure({ orderId }) {
    const db = this.memory.load();

    const order = db.orders.find(o => o.id === orderId);
    if (order) order.status = "failed";

    const paid = db.orders.filter(o => o.status === "paid").length;
    db.learning.winRate = db.orders.length ? paid / db.orders.length : 0;

    this.memory.save(db);

    return {
      status: "failure_logged",
      winRate: db.learning.winRate
    };
  }

  onContent(content) {
    const db = this.memory.load();

    db.runs.push({
      type: "content",
      ...content,
      timestamp: Date.now()
    });

    this.memory.save(db);

    return {
      status: "content_logged"
    };
  }
}

module.exports = EventBus;
