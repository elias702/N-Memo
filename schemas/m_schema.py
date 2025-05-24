from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


# Shared properties for creation and update
class SMemoBase(BaseModel):
    title: str
    content: str


# Used for creating a new memo
class SMemoCreate(SMemoBase):
    pass


# Used when creating memo (POST)
class SMemoCreateResponse(SMemoBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SMemoUpdate(SMemoBase):
    pass


class SMemoPartialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


# Update response
class SMemoUpdateResponse(SMemoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
