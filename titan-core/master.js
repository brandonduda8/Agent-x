require("dotenv").config();

const Memory = require("../core/memory");
const EventBus = require("../core/eventBus");

class Titan {
  constructor() {
    this.memory = new Memory();
    this.events = new EventBus(this.memory);
  }

  run(goal) {
    console.log("[TITAN ONLINE]", goal);

    const order = this.events.emit("order_created", {
      product: "AI system: " + goal,
      price: 19.99
    });

    const db = this.memory.load();

    const output = {
      system: "TITAN_RESTORED_V13",
      goal,
      orders: db.orders.length,
      revenue: db.learning.totalRevenue,
      winRate: db.learning.winRate,
      event: order
    };

    console.log("[OUTPUT]", output);
    return output;
  }
}

new Titan().run(process.argv[2] || "test system");
