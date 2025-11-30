from datetime import datetime

from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1)


class MessageResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    room_id: str
    sender_id: str | None
    content: str
    created_at: datetime
