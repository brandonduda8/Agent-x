const readline = require("readline");
const DevAgent = require("./agents/dev-agent");

const dev = new DevAgent();

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function menu() {
  console.log(`
=====================
AGENT-X OS v3
=====================
1. System Status
2. Scan Project
3. Revenue
4. Next Step AI
5. Exit
`);
}

function loop() {
  menu();

  rl.question("Select: ", (ans) => {
    switch(ans.trim()) {
      case "1":
        console.log(dev.status());
        break;

      case "2":
        console.log(dev.scan());
        break;

      case "3":
        console.log(dev.revenue());
        break;

      case "4":
        console.log(dev.suggestNextStep());
        break;

      case "5":
        process.exit(0);
    }

    setTimeout(loop, 500);
  });
}

loop();
