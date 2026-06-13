class Engine {
  constructor(memory) {
    this.memory = memory;
  }

  run() {
    const db = this.memory.db;

    const orders = db.orders.length;
    const revenue = db.strategy.totalRevenue;

    const winRate = orders === 0 ? 0 : revenue / orders;

    db.strategy.winRate = winRate;

    let recommendation = "STABLE";

    if (winRate > 25) {
      recommendation = "SCALE WINNERS";
    } else if (winRate < 10) {
      recommendation = "CHANGE OFFER";
    }

    db.strategy.recommendation = recommendation;

    this.memory.save();

    return {
      orders,
      revenue,
      winRate,
      recommendation
    };
  }
}

module.exports = Engine;
