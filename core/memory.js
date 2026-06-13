const fs = require("fs");
const path = require("path");

const DB_PATH = path.resolve(__dirname, "../memory.json");

class Memory {
  load() {
    try {
      return JSON.parse(fs.readFileSync(DB_PATH, "utf-8"));
    } catch (e) {
      return this._init();
    }
  }

  _init() {
    const db = {
      orders: [],
      revenue: [],
      learning: {
        totalRevenue: 0,
        totalOrders: 0
      }
    };

    fs.writeFileSync(DB_PATH, JSON.stringify(db, null, 2));
    return db;
  }

  save(db) {
    fs.writeFileSync(DB_PATH, JSON.stringify(db, null, 2));
  }

  addOrder(order) {
    const db = this.load();
    db.orders.push(order);
    db.learning.totalOrders = db.orders.length;
    this.save(db);
  }

  addRevenue(amount, orderId) {
    const db = this.load();

    db.revenue.push({
      id: Date.now(),
      amount,
      orderId
    });

    db.learning.totalRevenue += amount;

    this.save(db);
  }
}

module.exports = Memory;
