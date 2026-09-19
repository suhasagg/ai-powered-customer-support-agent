from pydantic import BaseModel, Field
from typing import Any

class ChatRequest(BaseModel):
    customer_id: str
    message: str
    conversation_id: str = "default"
    allow_actions: bool = False

class Source(BaseModel):
    title: str
    score: float
    excerpt: str

class ToolResult(BaseModel):
    tool: str
    ok: bool
    output: dict[str, Any]

class ChatResponse(BaseModel):
    answer: str
    intent: str
    sources: list[Source] = Field(default_factory=list)
    tools: list[ToolResult] = Field(default_factory=list)
    requires_approval: bool = False
