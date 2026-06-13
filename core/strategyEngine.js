class StrategyEngine {
  constructor(memory) {
    this.memory = memory;
  }

  analyze() {
    const db = this.memory.load();

    const orders = db.orders.length;
    const revenue = db.learning.totalRevenue || 0;
    const winRate = db.learning.winRate || 0;

    let stage = "EXPLORATION";
    let recommendation = "Collect more data";

    // 🧠 LOGIC TREE (V15 INTELLIGENCE)

    if (orders < 5) {
      stage = "EARLY_TESTING";
      recommendation = "Test multiple offers and hooks";
    }

    if (orders >= 5 && winRate < 0.2) {
      stage = "LOW_CONVERSION";
      recommendation = "Improve offer clarity or reduce price";
    }

    if (winRate >= 0.2 && winRate < 0.5) {
      stage = "GROWTH";
      recommendation = "Scale winning content + duplicate best funnel";
    }

    if (winRate >= 0.5) {
      stage = "WINNING_PATTERN";
      recommendation = "Increase price or scale traffic";
    }

    if (revenue > 100) {
      stage = "MONETIZED_SYSTEM";
      recommendation = "Optimize retention and upsells";
    }

    return {
      stage,
      metrics: {
        orders,
        revenue,
        winRate
      },
      recommendation,
      next_actions: this.generateActions(stage, winRate)
    };
  }

  generateActions(stage, winRate) {
    const actions = [];

    if (stage === "EARLY_TESTING") {
      actions.push("Create 3 new hooks");
      actions.push("Test 2 new products");
    }

    if (stage === "LOW_CONVERSION") {
      actions.push("Rewrite offer positioning");
      actions.push("Lower friction checkout");
    }

    if (stage === "GROWTH") {
      actions.push("Duplicate best-performing content");
      actions.push("Increase posting frequency");
    }

    if (stage === "WINNING_PATTERN") {
      actions.push("Increase ad spend / traffic");
      actions.push("Raise price 10-20%");
    }

    if (stage === "MONETIZED_SYSTEM") {
      actions.push("Add upsell products");
      actions.push("Build email retention loop");
    }

    return actions;
  }
}

module.exports = StrategyEngine;
