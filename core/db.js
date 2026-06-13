const { Low } = require("lowdb");
const { JSONFile } = require("lowdb/node");
const path = require("path");

const file = path.join(__dirname, "../data/db.json");
const adapter = new JSONFile(file);

// ✅ REQUIRED: default data (THIS FIXES YOUR ERROR)
const defaultData = {
  users: [],
  projects: [],
  revenue: []
};

// ✅ PASS DEFAULT DATA HERE
const db = new Low(adapter, defaultData);

async function init() {
  await db.read();

  // ensure structure always exists
  db.data ||= defaultData;

  await db.write();
}

module.exports = { db, init };
