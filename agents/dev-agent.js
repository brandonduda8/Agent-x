const fs = require("fs");
const path = require("path");
const Agent = require("../core/agent");

class DevAgent extends Agent {
  constructor() {
    super("DEV_AGENT");
  }

  status() {
    this.log("Checking system...");

    return {
      node: process.version,
      cwd: process.cwd(),
      hasServer: fs.existsSync("execution/server.js"),
      hasRevenue: fs.existsSync("data/revenue.json")
    };
  }

  scan() {
    this.log("Scanning project...");

    return fs.readdirSync(process.cwd());
  }

  revenue() {
    try {
      const data = JSON.parse(
        fs.readFileSync("data/revenue.json")
      );

      const total = data.reduce((a, b) => a + (b.amount || 0), 0);

      return {
        count: data.length,
        total: total / 100
      };

    } catch {
      return { count: 0, total: 0 };
    }
  }

  suggestNextStep() {
    const status = this.status();

    if (!status.hasServer) {
      return "Build Express server with Stripe checkout";
    }

    if (!status.hasRevenue) {
      return "Create revenue tracking system";
    }

    return "Add dashboard + product system + automation layer";
  }
}

module.exports = DevAgent;
