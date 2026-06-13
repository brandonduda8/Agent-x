class Agent {
  constructor(name, tools = {}) {
    this.name = name;
    this.tools = tools;
  }

  log(msg) {
    console.log(`[${this.name}] ${msg}`);
  }

  async run(task) {
    throw new Error("run() must be implemented");
  }
}

module.exports = Agent;
