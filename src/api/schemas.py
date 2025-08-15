from pydantic import BaseModel
from typing import Optional, List

class ProtocolIn(BaseModel):
    title: str
    specialty: Optional[str] = None
    content: str

class ProtocolOut(BaseModel):
    id: int
    title: str
    specialty: Optional[str] = None
    content: str

class SuggestIn(BaseModel):
    symptoms: str
    specialty: Optional[str] = None
