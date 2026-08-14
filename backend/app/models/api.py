from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class AddEpisodeRequest(BaseModel):
    content: str
    group_id: Optional[str] = "default"

class SearchNodesRequest(BaseModel):
    query: str
    group_id: Optional[str] = None
    limit: Optional[int] = 50

class InvestigateRequest(BaseModel):
    entity_name: str
    depth: Optional[int] = 2
    group_id: Optional[str] = None
