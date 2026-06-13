const Memory = require("../core/memory");
const EventBus = require("../core/eventBus");
const StrategyEngine = require("../core/strategyEngine");

class Orchestrator {
  constructor() {
    this.memory = new Memory();
    this.events = new EventBus(this.memory);
    this.strategy = new StrategyEngine(this.memory);
  }

  run(goal) {
    console.log("[AI BUSINESS OS START]", goal);

    const offer = this.generateOffer(goal);

    const order = this.events.emit("order_created", {
      product: offer.product,
      price: offer.price
    });

    const strategy = this.strategy.analyze();

    const output = {
      system: "AI_BUSINESS_OS_v1",
      goal,
      offer,
      event: order,
      strategy
    };

    console.log("[OUTPUT]", JSON.stringify(output, null, 2));
    return output;
  }

  generateOffer(goal) {
    return {
      product: `AI tool for: ${goal}`,
      price: 29.99,
      funnel: "content → dm → checkout"
    };
  }
}

module.exports = Orchestrator;
