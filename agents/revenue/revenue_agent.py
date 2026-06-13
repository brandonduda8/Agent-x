import os
import asyncio
from core.event_bus import bus
from core.llm_client import llm
from tools.code_tools import write_file

class RevenueAgent:
    def __init__(self, name="Revenue-Agent"):
        self.name = name
        # Listen for successful build results
        bus.subscribe("result", self.on_build_complete)

    async def on_build_complete(self, event: dict):
        if event['source'] != 'builder' or event['payload'].get('status') != 'success':
            return
            
        artifacts = event['payload'].get('artifacts', [])
        html_files = [f for f in artifacts if f.endswith('.html')]
        
        if not html_files:
            return
            
        html_file = html_files[0]
        print(f"💰 [{self.name}] Analyzing {html_file} for monetization opportunities...")
        
        try:
            with open(html_file, 'r') as f:
                current_code = f.read()
        except Exception:
            return

        # Ask LLM to generate a monetization snippet
        prompt = f"""Here is a landing page code:\n{current_code[:1000]}...\n
Generate a short, modern HTML/CSS snippet to add a monetization hook. 
Choose ONE: 
1. A "Get Early Access" email capture form.
2. A "Pricing" section with a Stripe-style checkout button.
Output ONLY the raw HTML/CSS snippet. No markdown, no explanations."""

        try:
            snippet = await llm.generate(prompt, "You are an expert conversion rate optimization specialist.", max_tokens=1000)
            clean_snippet = snippet.replace("```html", "").replace("```", "").strip()
            
            # Inject the snippet before the closing </body> tag
            if "</body>" in current_code:
                new_code = current_code.replace("</body>", f"\n<!-- Monetization Hook Added by Revenue Agent -->\n{clean_snippet}\n</body>")
                write_file(html_file, new_code)
                print(f"✅ [{self.name}] Successfully injected monetization hook into {html_file}!")
            else:
                print(f"⚠️ [{self.name}] Could not find </body> tag to inject code.")
        except Exception as e:
            print(f"❌ [{self.name}] Failed to inject revenue hook: {e}")

revenue_agent = RevenueAgent()
