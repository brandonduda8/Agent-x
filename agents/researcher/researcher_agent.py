import asyncio
import httpx
from bs4 import BeautifulSoup
from core.event_bus import bus
from core.llm_client import llm

class ResearcherAgent:
    def __init__(self, name="Researcher"):
        self.name = name
        bus.subscribe("task", self.on_task_received)

    async def search_ddg(self, query: str) -> str:
        print(f"🔍 [{self.name}] Scraping DuckDuckGo for: {query}")
        url = "https://html.duckduckgo.com/html/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data={"q": query}, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            results = []
            # Extract the text snippets from the search results
            for a in soup.find_all("a", class_="result__snippet"):
                results.append(a.get_text(strip=True))
            return "\n".join(results[:5]) if results else "No results found."

    async def on_task_received(self, event: dict):
        if event['target'] != 'researcher':
            return
            
        query = event['payload']['objective']
        print(f"🔍 [{self.name}] Researching: {query}")
        
        # 1. Perform real web search using pure Python
        try:
            context = await self.search_ddg(query)
        except Exception as e:
            context = f"Web search failed: {e}. Relying on internal knowledge."

        # 2. Synthesize findings with the LLM
        system_prompt = "You are a market researcher. Summarize the findings into a concise 3-point strategy for building a product."
        summary = await llm.generate(f"Search results:\n{context}\n\nQuery: {query}", system_prompt)
        print(f"📊 [{self.name}] Synthesized Strategy: {summary[:100]}...")

        # 3. Hand off to Builder
        await bus.publish({
            "id": f"build_{event['id']}",
            "source": "researcher",
            "target": "builder",
            "type": "task",
            "payload": {"objective": f"Build a prototype based on this strategy: {summary}"}
        })

researcher = ResearcherAgent()
