from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from .config import settings
from .agents import AGENTS
from .orchestrator import orchestrator

app=FastAPI(title=settings.app_name,version="1.0.0")

class SubmitRequest(BaseModel):
    target:str
    objective:str
    payload:dict=Field(default_factory=dict)
    priority:int=Field(default=50,ge=0,le=100)

class CollaborationRequest(BaseModel):
    requester:str
    helper:str
    objective:str
    priority:int=Field(default=60,ge=0,le=100)

@app.get("/health")
async def health(): return {"status":"ok","agents":len(AGENTS),"queued":orchestrator.queue.qsize()}

@app.get("/api/agents")
async def agents(): return [{"id":a.key,"name":a.name,"specialty":a.specialty} for a in AGENTS.values()]

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

@app.get("/",response_class=HTMLResponse)
async def dashboard(): return DASHBOARD

DASHBOARD="""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Multi-Agent Intelligence</title>
<style>*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 50% 25%,#13254b,#050916 55%);color:#eaf2ff;font-family:system-ui}header{text-align:center;padding:28px}h1{color:#68e5ff;margin:0}.sub{color:#8294b7;margin:8px}.controls{text-align:center;margin:10px}button{background:#112344;color:#fff;border:1px solid #385a8b;border-radius:10px;padding:10px 16px;cursor:pointer}.stage{position:relative;max-width:1150px;height:720px;margin:20px auto;border:1px solid #1e355c;border-radius:24px;background:#071022aa}.node{position:absolute;padding:12px;border:1px solid #31517d;border-radius:14px;background:#0d1932;text-align:center;width:150px}.agent{transition:.3s}.active{box-shadow:0 0 30px #59e7ff;border-color:#59e7ff;transform:scale(1.05)}.core{left:50%;top:42%;transform:translate(-50%,-50%);width:260px;border-color:#8b72ff}.bus{left:50%;top:59%;transform:translateX(-50%);width:350px}.memory{left:50%;top:70%;transform:translateX(-50%);width:230px}.you{left:50%;top:4%;transform:translateX(-50%);width:190px}.notify{left:50%;top:18%;transform:translateX(-50%);width:210px}.log{position:absolute;right:2%;bottom:3%;width:220px;height:150px;overflow:auto;font:11px monospace;color:#77ffc4}.small{font-size:10px;color:#8294b7}.dot{color:#63f2ad}</style></head>
<body><header><h1>Autonomous Multi-Agent Intelligence System</h1><div class="sub">10 specialists • orchestration • shared memory • intelligent alerts</div></header><div class="controls"><button onclick="runTask()">⚡ Trigger Task</button><button onclick="collab()">↔ Agent Collaboration</button></div>
<div class="stage" id="stage"><div class="node you">👤<br><b>YOU</b></div><div class="node notify">🔔<br><b>Notification Intelligence</b><div class="small">filter • rank • summarize</div></div><div class="node core">🧠<br><b>CENTRAL ORCHESTRATOR</b><div class="small">routing • permissions • priority</div></div><div class="node bus">⚡ <b>EVENT / MESSAGE BUS</b></div><div class="node memory">💾<br><b>SHARED MEMORY</b></div><div class="log" id="log"></div></div>
<script>const names=["AI / LLM Research","Research Papers","GitHub Monitor","Career Intelligence","Market Intelligence","GPU / Infrastructure","Project Manager","Email / Documents","Knowledge Research","Security Monitor"],pos=[[4,17],[19,17],[70,17],[84,17],[4,31],[19,31],[70,31],[84,31],[20,82],[64,82]],stage=document.getElementById("stage");names.forEach((n,i)=>{let d=document.createElement("div");d.className="node agent";d.id="a"+(i+1);d.style.left=pos[i][0]+"%";d.style.top=pos[i][1]+"%";d.innerHTML="🤖<br><b>A"+(i+1)+"</b><div class=small>"+n+"</div><div class=dot>● IDLE</div>";stage.appendChild(d)});function msg(x){document.getElementById("log").innerHTML="› "+x+"<br>"+document.getElementById("log").innerHTML}async function runTask(){let n=1+Math.floor(Math.random()*10),e=document.getElementById("a"+n);e.classList.add("active");msg("A"+n+" task dispatched");let r=await fetch("/api/tasks",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({target:"a"+n,objective:"Autonomous intelligence check",priority:75})}),j=await r.json();msg(j.result?.summary||"Task complete");setTimeout(()=>e.classList.remove("active"),1000)}async function collab(){let a=1+Math.floor(Math.random()*10),b=1+Math.floor(Math.random()*10);if(a===b)b=b%10+1;msg("A"+a+" requests A"+b);let r=await fetch("/api/collaborate",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({requester:"a"+a,helper:"a"+b,objective:"Cross-agent intelligence request",priority:70})}),j=await r.json();msg(j.result?.summary||"Collaboration complete")}</script></body></html>"""
