from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .config import settings
from .agents import AGENTS
from .orchestrator import orchestrator
from .storage import store
from .scheduler import scheduler
from .tools import registry

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    await scheduler.stop()

app=FastAPI(title=settings.app_name,version="2.0.0",lifespan=lifespan)

class SubmitRequest(BaseModel):
    target:str; objective:str; payload:dict=Field(default_factory=dict); priority:int=Field(default=50,ge=0,le=100)
class CollaborationRequest(BaseModel):
    requester:str; helper:str; objective:str; priority:int=Field(default=60,ge=0,le=100)
class ScheduleRequest(BaseModel):
    name:str; target:str; objective:str; payload:dict=Field(default_factory=dict); priority:int=Field(default=50,ge=0,le=100); interval_seconds:int=Field(default=3600,ge=60)
class ApprovalRequest(BaseModel):
    agent:str; tool:str; arguments:dict=Field(default_factory=dict); reason:str
class DecisionRequest(BaseModel):
    approve:bool

@app.get("/health")
async def health(): return {"status":"ok","agents":len(AGENTS),"queued":orchestrator.queue.qsize(),"scheduler":settings.scheduler_enabled}
@app.get("/api/agents")
async def agents(): return [{"id":a.key,"name":a.name,"specialty":a.specialty,"tools":registry.describe(a.tools)} for a in AGENTS.values()]
@app.post("/api/tasks")
async def submit(req:SubmitRequest):
    try:
        task=await orchestrator.submit(req.target,req.objective,req.payload,req.priority)
        return {"task":task,"result":await orchestrator.process_one()}
    except ValueError as e: raise HTTPException(400,str(e))
@app.post("/api/collaborate")
async def collaborate(req:CollaborationRequest):
    try:
        task=await orchestrator.collaborate(req.requester,req.helper,req.objective,req.priority)
        return {"task":task,"result":await orchestrator.process_one()}
    except ValueError as e: raise HTTPException(400,str(e))
@app.get("/api/notifications")
async def notifications(): return orchestrator.notifications[-50:]
@app.get("/api/history")
async def history(limit:int=50): return store.recent(max(1,min(limit,200)))
@app.post("/api/schedules")
async def create_schedule(req:ScheduleRequest):
    try: return scheduler.create(req.name,req.target,req.objective,req.payload,req.priority,req.interval_seconds)
    except ValueError as e: raise HTTPException(400,str(e))
@app.get("/api/schedules")
async def schedules(): return store.schedules()
@app.post("/api/approvals")
async def request_approval(req:ApprovalRequest):
    try: return orchestrator.request_approval(req.agent,req.tool,req.arguments,req.reason)
    except ValueError as e: raise HTTPException(400,str(e))
@app.get("/api/approvals")
async def approvals(status:str="pending"): return store.approvals(status)
@app.post("/api/approvals/{approval_id}/decision")
async def decide(approval_id:str,req:DecisionRequest):
    status="approved" if req.approve else "rejected"
    if not store.decide_approval(approval_id,status): raise HTTPException(404,"Pending approval not found")
    store.add("approval_decision","system",status,80,{"approval_id":approval_id})
    return {"id":approval_id,"status":status}
