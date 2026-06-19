from pydantic import BaseModel
from typing import Optional


class NoteCreate(BaseModel):
    title: str
    description: Optional[str] = None


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_archived: Optional[bool] = None
    is_trashed: Optional[bool] = None


class NoteResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_archived: bool
    is_trashed: bool
    user_id: int

    class Config:
        from_attributes = True