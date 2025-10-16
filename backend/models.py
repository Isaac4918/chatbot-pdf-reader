from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    """Structure of the POST request sent to /chat"""
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    """Base structure of a non-streaming chat response"""
    type: str
    content: str
