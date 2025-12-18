
from pydantic import BaseModel
from typing import List, Optional

class Source(BaseModel):
    document: str
    page: int

class ChatResponse(BaseModel):
    answer: str
    sources: Optional[List[Source]] = []
    images: Optional[List[str]] = []
    used_rag: bool