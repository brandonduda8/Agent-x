import asyncio
import json
from datetime import datetime
from typing import Callable, Dict, List

class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_log = []

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    async def publish(self, event: dict):
        event["timestamp"] = datetime.utcnow().isoformat() + "Z"
        self.event_log.append(event)
        print(f"📡 [EVENT BUS] {event['type']} from {event['source']} -> {event['target']}")
        
        callbacks = self.subscribers.get(event['type'], [])
        callbacks.extend(self.subscribers.get('*', []))
        
        for callback in callbacks:
            if asyncio.iscoroutinefunction(callback):
                await callback(event)
            else:
                callback(event)

bus = EventBus()
