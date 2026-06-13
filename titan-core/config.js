module.exports = {
  MODE: process.env.MODE || "FREE",

  FREE_MODE: true,

  OPENROUTER_MODEL: "openai/gpt-4o-mini",

  MOCK_RESPONSE: {
    type: "automation system blueprint",
    intent: "monetize",
    price: 0,
    funnel: "mock",
    strategy: "offline simulation",
    priority: 1
  }
};
