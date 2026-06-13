const fs = require("fs");
const path = require("path");

class Builder {
  plan(input = "") {
    const t = input.toLowerCase();

    if (t.includes("stripe") || t.includes("saas")) {
      return {
        type: "stripe-saas",
        files: [
          "server.js",
          "public/index.html",
          "routes/checkout.js"
        ]
      };
    }

    if (t.includes("landing") || t.includes("website")) {
      return {
        type: "landing-page",
        files: [
          "public/index.html",
          "public/style.css"
        ]
      };
    }

    if (t.includes("api") || t.includes("backend")) {
      return {
        type: "node-api",
        files: [
          "server.js",
          "routes/api.js"
        ]
      };
    }

    return {
      type: "generic",
      files: [
        "server.js"
      ]
    };
  }

  generateFile(file) {
    const templates = {
      "server.js": `
const express = require("express");
const app = express();

app.get("/", (req,res)=>{
  res.send("AI GENERATED SERVER");
});

app.listen(3000, ()=>console.log("server running"));
      `,

      "public/index.html": `
<html>
<head><title>AI Build</title></head>
<body>
<h1>AI BUILDER OUTPUT</h1>
</body>
</html>
      `,

      "routes/checkout.js": `
module.exports = (app) => {
  app.post("/checkout", (req,res)=>{
    res.json({ status: "stripe-placeholder" });
  });
};
      `,

      "public/style.css": `
body { font-family: Arial; background:#111; color:white; }
      `
    };

    return templates[file] || "// auto-generated file";
  }

  writeProject(plan, baseDir = "./generated_project") {
    if (!fs.existsSync(baseDir)) {
      fs.mkdirSync(baseDir);
    }

    plan.files.forEach((file) => {
      const fullPath = path.join(baseDir, file);

      fs.mkdirSync(path.dirname(fullPath), { recursive: true });

      fs.writeFileSync(fullPath, this.generateFile(file));
    });

    return {
      status: "project generated",
      type: plan.type,
      location: baseDir,
      files: plan.files
    };
  }
}

module.exports = Builder;
