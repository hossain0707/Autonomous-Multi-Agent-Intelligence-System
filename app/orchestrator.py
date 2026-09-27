import asyncio
from uuid import uuid4
from .agents import AGENTS
from .models import Task
from .config import settings
from .storage import store

class Orchestrator:
    def __init__(self):
        self.queue=asyncio.Queue(); self.notifications=[]; self.worker=None
    async def submit(self,target,objective,payload=None,priority=50,source="user"):
        if target not in AGENTS: raise ValueError(f"Unknown agent: {target}")
        task=Task(id=str(uuid4()),source=source,target=target,objective=objective,payload=payload or {},priority=priority)
        await self.queue.put(task); store.add("task",target,objective,priority,{"task_id":task.id,"source":source}); return task
    async def process_one(self):
        task=await self.queue.get()
        try:
            result=await AGENTS[task.target].run(task); store.add("result",result.agent,result.summary,result.importance,{"task_id":result.task_id})
            if result.importance>=settings.notify_threshold: self.notifications.append(result)
            return result
        finally: self.queue.task_done()
    async def collaborate(self,requester,helper,objective,priority=60):
        if requester not in AGENTS or helper not in AGENTS: raise ValueError("Unknown agent")
        if requester==helper: raise ValueError("Requester and helper must differ")
        return await self.submit(helper,objective,{"requested_by":requester},priority,requester)

orchestrator=Orchestrator()
