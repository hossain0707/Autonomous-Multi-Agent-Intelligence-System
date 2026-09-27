import asyncio
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from .storage import store
from .orchestrator import orchestrator
from .config import settings

class Scheduler:
    def __init__(self): self.task=None
    def create(self,name,target,objective,payload,priority,interval_seconds):
        if interval_seconds < 60: raise ValueError("Minimum interval is 60 seconds")
        now=datetime.now(timezone.utc)
        item={"id":str(uuid4()),"name":name,"target":target,"objective":objective,"payload":payload or {},"priority":priority,"interval_seconds":interval_seconds,"next_run":now.isoformat()}
        store.add_schedule(item); return item
    async def tick(self):
        now=datetime.now(timezone.utc)
        for s in store.schedules(enabled_only=True):
            if datetime.fromisoformat(s["next_run"]) <= now:
                await orchestrator.submit(s["target"],s["objective"],s["payload"],s["priority"],source=f"schedule:{s['id']}")
                await orchestrator.process_one()
                store.mark_schedule_run(s["id"],(now+timedelta(seconds=s["interval_seconds"])).isoformat())
    async def loop(self):
        while True:
            try: await self.tick()
            except Exception as exc: store.add("scheduler_error","scheduler",str(exc),100,{})
            await asyncio.sleep(settings.scheduler_tick_seconds)
    def start(self):
        if settings.scheduler_enabled and (self.task is None or self.task.done()):
            self.task=asyncio.create_task(self.loop())
    async def stop(self):
        if self.task:
            self.task.cancel()
            try: await self.task
            except asyncio.CancelledError: pass

scheduler=Scheduler()
