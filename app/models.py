from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel, Field

class Task(BaseModel):
    id: str
    source: str
    target: str
    objective: str
    payload: dict[str, Any] = Field(default_factory=dict)
    priority: int = Field(default=50, ge=0, le=100)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AgentResult(BaseModel):
    task_id: str
    agent: str
    summary: str
    importance: int = Field(ge=0, le=100)
    data: dict[str, Any] = Field(default_factory=dict)
