from pydantic import BaseModel, constr
from uuid import UUID
from datetime import datetime
from typing import Optional

class CreateNotes(BaseModel):
    title: constr(min_length=3)
    content: constr(min_length=10)

class UpdateNotes(CreateNotes):
    pass

class GetNotes(BaseModel):
    id: UUID
    title: str
    content: str
    ai_summary: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True