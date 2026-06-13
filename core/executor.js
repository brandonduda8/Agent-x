const fs = require("fs");

class Executor {
  constructor(agents) {
    this.agents = agents;
  }

  run(route) {
    const agent = this.agents[route.agent];

    if (!agent) {
      return { error: "Agent not found" };
    }

    const action = route.action;

    if (agent[action]) {
      return agent[action]();
    }

    return {
      error: "Action not supported",
      agent: route.agent,
      action
    };
  }
}

module.exports = Executor;
