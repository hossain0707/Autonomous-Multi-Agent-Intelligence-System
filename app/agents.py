from dataclasses import dataclass
import asyncio
from .models import Task, AgentResult
from .provider import generate

@dataclass
class Agent:
    key:str; name:str; specialty:str
    async def run(self,task:Task)->AgentResult:
        summary=await asyncio.to_thread(generate,self.name,self.specialty,task.objective,task.payload)
        return AgentResult(task_id=task.id,agent=self.key,summary=summary,importance=min(100,max(task.priority,20)),data={"specialty":self.specialty})

AGENTS={
"a1":Agent("a1","AI / LLM Research","models, training, inference"),"a2":Agent("a2","Research Papers","literature and scientific analysis"),
"a3":Agent("a3","GitHub Monitor","repositories, issues, releases"),"a4":Agent("a4","Career Intelligence","roles and career signals"),
"a5":Agent("a5","Market Intelligence","competitive signals"),"a6":Agent("a6","GPU / Infrastructure","compute, serving, reliability"),
"a7":Agent("a7","Project Manager","planning, dependencies, delivery"),"a8":Agent("a8","Email / Documents","communication and documents"),
"a9":Agent("a9","Knowledge Research","research and synthesis"),"a10":Agent("a10","Security Monitor","security and operational risk")}
