from pydantic import BaseModel
from typing import Optional

class MessageBase(BaseModel):
    PID: str
    sender: str
    subject: str
    body: str
    organization: str
    thread_id: Optional[str] = None

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    class Config:
        from_attributes = True 