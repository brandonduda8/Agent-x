const Memory = require('./core/memory');
const EventBus = require('./core/eventBus');

const m = new Memory();
const bus = new EventBus(m);

const db = m.load();
const order = db.orders[db.orders.length - 1];

if (!order) {
  console.log('No orders found');
  process.exit(0);
}

bus.emit('payment_received', {
  orderId: order.id,
  amount: 19.99
});

console.log('Revenue triggered for order:', order.id);
