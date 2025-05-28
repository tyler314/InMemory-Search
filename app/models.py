from pydantic import BaseModel
from typing import List


class Document(BaseModel):
    content: str


class DocumentIdList(BaseModel):
    status: int
    total: int
    document_ids: List[str]
