from typing import Dict, Optional, List
from datetime import datetime
from pydantic import BaseModel

class Document(BaseModel):
    id: str
    group_key: Optional[str] = None
    metadata: Optional[Dict] = {}
    text: Optional[List] = []
    chunks: Optional[List] = []
    embeddings: Optional[List] = []


class News:
    headline: str
    summary: str
    content: str
    date: datetime