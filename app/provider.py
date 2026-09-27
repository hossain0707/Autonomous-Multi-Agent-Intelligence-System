import json, urllib.request
from .config import settings

SYSTEM="You are a specialist autonomous agent. Return concise, factual output. Never claim an external action happened unless a tool actually performed it."

def generate(agent_name,specialty,objective,payload):
    if not settings.openai_api_key:
        return f"{agent_name} analyzed the task: {objective}. Configure OPENAI_API_KEY for model-generated intelligence."
    body=json.dumps({"model":settings.openai_model,"input":[{"role":"system","content":SYSTEM},{"role":"user","content":f"Role: {agent_name}\nSpecialty: {specialty}\nTask: {objective}\nContext: {json.dumps(payload)}"}]}).encode()
    req=urllib.request.Request("https://api.openai.com/v1/responses",data=body,headers={"Authorization":f"Bearer {settings.openai_api_key}","Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=45) as r: data=json.loads(r.read())
    if data.get("output_text"): return data["output_text"]
    texts=[]
    for item in data.get("output",[]):
        for c in item.get("content",[]): 
            if c.get("type")=="output_text": texts.append(c.get("text",""))
    return "\n".join(texts) or "Model returned no text."
