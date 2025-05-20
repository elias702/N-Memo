from typing import Optional
from pydantic import BaseModel, ConfigDict, computed_field
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


# Used for all other responses
class SMemoResponse(SMemoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def updated_at_msg(self) -> str:
        return (
            "Not updated yet"
            if self.updated_at is None
            else self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        )


# Update response
class SMemoUpdateResponse(SMemoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
