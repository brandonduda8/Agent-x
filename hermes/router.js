require("dotenv").config();
const axios = require("axios");

class Hermes {
  constructor() {
    this.key = process.env.OPENROUTER_API_KEY;

    if (!this.key) throw new Error("Missing OPENROUTER_API_KEY");
  }

  async call(model, messages) {
    const res = await axios.post(
      "https://openrouter.ai/api/v1/chat/completions",
      { model, messages, temperature: 0.4 },
      {
        headers: {
          Authorization: `Bearer ${this.key}`,
          "Content-Type": "application/json",
          "HTTP-Referer": "http://localhost",
          "X-Title": "income-os-v3"
        }
      }
    );

    return res.data.choices?.[0]?.message?.content;
  }

  async route(goal) {
    try {
      // 🧠 Step 1: fast classifier (cheap brain)
      const gpt = await this.call("openai/gpt-4o-mini", [
        {
          role: "system",
          content: "Return ONLY JSON. classify business intent."
        },
        {
          role: "user",
          content: `Goal: ${goal}

Return:
{
  "intent": "build|monetize|grow|research",
  "complexity": "low|medium|high",
  "best_model": "gpt|claude|gemini"
}`
        }
      ]);

      const decision = JSON.parse(gpt);

      // 🧠 Step 2: model routing (multi-brain system)
      let model = "openai/gpt-4o-mini";

      if (decision.best_model === "claude") {
        model = "anthropic/claude-3-haiku";
      }

      if (decision.best_model === "gemini") {
        model = "google/gemini-flash-1.5";
      }

      // 🧠 Step 3: final reasoning pass
      const final = await this.call(model, [
        {
          role: "system",
          content: "You are a monetization architect. Return structured JSON."
        },
        {
          role: "user",
          content: `
Goal: ${goal}

Using this intent:
${JSON.stringify(decision)}

Return:
{
  "product": "what to build",
  "offer": "what to sell",
  "audience": "who buys",
  "price": number,
  "funnel": "stripe|tiktok|dm",
  "content_hook": "viral short-form hook"
}
`
        }
      ]);

      return JSON.parse(final);
    } catch (e) {
      return {
        error: "Hermes v3 failed",
        message: e.message
      };
    }
  }
}

module.exports = Hermes;
