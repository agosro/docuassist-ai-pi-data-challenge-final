from typing import TypedDict, Optional, List, Dict

class ChatState(TypedDict):
    question: str
    filters: Dict[str, str]          
    is_generic: bool                 
    intent: Optional[str]
    answer: Optional[str]
    sources: Optional[List[Dict]]
    images: Optional[List[str]]
    used_rag: Optional[bool]
