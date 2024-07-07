from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class PostResponse(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
