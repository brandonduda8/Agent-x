const fs = require("fs");

class DevCopilot {
  analyzeProject() {
    console.log("🔍 Analyzing Project...");
    const files = fs.readdirSync(".");
    files.forEach(f => console.log("•", f));
  }

  showRevenue() {
    try {
      const revenue = JSON.parse(
        fs.readFileSync("./data/revenue.json")
      );

      console.log("💰 Revenue Records:", revenue.length);
    } catch {
      console.log("No revenue records found");
    }
  }

  status() {
    console.log("⚡ Agent-X Dev Copilot Online");
    console.log("Node:", process.version);
  }
}

module.exports = DevCopilot;
