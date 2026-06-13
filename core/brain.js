class Brain {
  constructor(agents = {}) {
    this.agents = agents;
  }

  route(input = "") {
    const text = input.toLowerCase();

    // ---------------- SYSTEM OPS ----------------
    if (text.includes("status") || text.includes("health")) {
      return { agent: "ops", action: "status" };
    }

    if (text.includes("scan") || text.includes("files")) {
      return { agent: "dev", action: "scan" };
    }

    if (text.includes("revenue") || text.includes("money")) {
      return { agent: "revenue", action: "report" };
    }

    if (text.includes("pm2") || text.includes("restart")) {
      return { agent: "ops", action: "pm2" };
    }

    // ---------------- BUILD INTENT ----------------
    if (text.includes("build") || text.includes("create") || text.includes("make")) {
      return { agent: "dev", action: "build" };
    }

    // ---------------- STRIPE / BUSINESS ----------------
    if (text.includes("stripe") || text.includes("checkout") || text.includes("sell")) {
      return { agent: "revenue", action: "stripe" };
    }

    // ---------------- DEFAULT ----------------
    return {
      agent: "dev",
      action: "unknown",
      message: "I couldn't map this command. Try: build, scan, revenue, status"
    };
  }
}

module.exports = Brain;
