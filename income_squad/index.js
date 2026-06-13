const fs = require("fs");
const path = require("path");

const OUT = path.join(__dirname, "../generated");

module.exports = {
  execute: async (task) => {
    console.log("[INCOME SQUAD] monetizing:", task.goal);

    const file = path.join(OUT, `product-${Date.now()}.json`);

    const product = {
      title: `AI Product: ${task.goal}`,
      price: 9 + Math.floor(Math.random() * 91),
      funnel: "sink-mock",
      status: "ready",
      intent: task.intent
    };

    fs.writeFileSync(file, JSON.stringify(product, null, 2));

    return {
      ok: true,
      file,
      checkout: "http://localhost:3002/checkout/mock",
      product
    };
  }
};
