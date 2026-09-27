from dataclasses import dataclass
import asyncio, json
from .models import Task, AgentResult
from .provider import generate
from .tools import registry

@dataclass(frozen=True)
class Agent:
    key: str
    name: str
    specialty: str
    tools: tuple[str, ...] = ()
    async def run(self, task: Task) -> AgentResult:
        tool_results = []
        requested = task.payload.get("tool_calls", []) if isinstance(task.payload, dict) else []
        for call in requested:
            name = call.get("name", "")
            if name not in self.tools:
                raise ValueError(f"{self.key} is not permitted to use {name}")
            tool = registry.get(name)
            if tool.mode != "read":
                raise ValueError("Write tools require approval workflow")
            result = await tool.handler(call.get("args", {}))
            tool_results.append({"tool": name, "result": result})
        payload = dict(task.payload or {})
        if tool_results:
            payload["tool_results"] = tool_results
        summary = await asyncio.to_thread(generate, self.name, self.specialty, task.objective, payload)
        return AgentResult(task_id=task.id, agent=self.key, summary=summary, importance=min(100, max(task.priority, 20)), data={"specialty": self.specialty, "tools": tool_results})

AGENTS = {
"a1": Agent("a1","AI / LLM Research","models, training, inference",("http.fetch_json",)),
"a2": Agent("a2","Research Papers","literature and scientific analysis",("http.fetch_json",)),
"a3": Agent("a3","GitHub Monitor","repositories, issues, releases",("github.repo_activity",)),
"a4": Agent("a4","Career Intelligence","roles and career signals",("http.fetch_json",)),
"a5": Agent("a5","Market Intelligence","competitive signals",("http.fetch_json",)),
"a6": Agent("a6","GPU / Infrastructure","compute, serving, reliability",("http.fetch_json","system.health")),
"a7": Agent("a7","Project Manager","planning, dependencies, delivery",()),
"a8": Agent("a8","Email / Documents","communication and documents",()),
"a9": Agent("a9","Knowledge Research","research and synthesis",("http.fetch_json",)),
"a10": Agent("a10","Security Monitor","security and operational risk",("github.repo_activity","system.health")),
}
