from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class Step(BaseModel):
    t: int
    agent: str
    action: str
    obs: Optional[str] = None
    error: Optional[str] = None

class Record(BaseModel):
    id: str
    query: str
    steps: List[Step]
    final_status: str
    label: Optional[Dict[str, Any]] = None  # {"agent": str, "step": int}
