from pathlib import Path
from fastapi import FastAPI
from .models import ChatRequest, ChatResponse
from .kb import KnowledgeBase
from .agent import SupportAgent

BASE=Path(__file__).resolve().parents[1]
app=FastAPI(title='AI Customer Support Agent',version='1.0.0')
agent=SupportAgent(KnowledgeBase(str(BASE/'data'/'kb')))

@app.get('/health')
def health(): return {'status':'ok'}

@app.post('/v1/support/chat', response_model=ChatResponse)
def chat(req: ChatRequest): return agent.run(req)
