const fs = require("fs");

module.exports = {
  status() {
    return {
      node: process.version,
      server: fs.existsSync("execution/server.js"),
      revenue: fs.existsSync("data/revenue.json")
    };
  },

  scan() {
    return fs.readdirSync(".");
  },

  revenue() {
    try {
      const data = JSON.parse(fs.readFileSync("data/revenue.json"));

      const total = data.reduce((a, b) => a + (b.amount || 0), 0);

      return {
        transactions: data.length,
        total: total / 100
      };
    } catch {
      return { transactions: 0, total: 0 };
    }
  },

  nextStep() {
    if (!fs.existsSync("execution/server.js")) {
      return "Build server.js";
    }

    if (!fs.existsSync("data/revenue.json")) {
      return "Create revenue tracking system";
    }

    return "Add Stripe checkout + product system + traffic system";
  }
};
