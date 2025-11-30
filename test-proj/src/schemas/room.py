from datetime import datetime

from pydantic import BaseModel


class RoomCreate(BaseModel):
    other_user_id: str


class RoomMemberResponse(BaseModel):
    model_config = {"from_attributes": True}

    user_id: str
    joined_at: datetime


class RoomResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    created_at: datetime
    members: list[RoomMemberResponse] = []
