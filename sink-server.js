const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = 3002;

const catalogPath = path.join(__dirname, "stripe-catalog/config.json");
const logPath = path.join(__dirname, "logs/sink.log");

function log(data) {
  fs.mkdirSync(path.dirname(logPath), { recursive: true });
  fs.appendFileSync(logPath, JSON.stringify(data) + "\n");
}

function loadCatalog() {
  return JSON.parse(fs.readFileSync(catalogPath, "utf8"));
}

function saveCatalog(catalog) {
  fs.writeFileSync(catalogPath, JSON.stringify(catalog, null, 2));
}

const server = http.createServer((req, res) => {
  if (req.method !== "POST") {
    res.writeHead(200);
    return res.end("Agent X Sink Server Running");
  }

  let body = "";

  req.on("data", chunk => (body += chunk));

  req.on("end", () => {
    try {
      const data = JSON.parse(body);

      const catalog = loadCatalog();

      const productId = data?.payload?.name || "unknown-product";

      const checkoutUrl = `http://localhost:${PORT}/checkout/${productId}`;

      const event = {
        ok: true,
        received: data,
        checkout_url: checkoutUrl,
        timestamp: new Date().toISOString()
      };

      log(event);

      // attach sink result into catalog history
      if (!catalog.events) catalog.events = [];
      catalog.events.push(event);
      saveCatalog(catalog);

      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify(event));
    } catch (err) {
      res.writeHead(500);
      res.end(JSON.stringify({ ok: false, error: err.message }));
    }
  });
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`[SINK] running on http://0.0.0.0:${PORT}`);
});
