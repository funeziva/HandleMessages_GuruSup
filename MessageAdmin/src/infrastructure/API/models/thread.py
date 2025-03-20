from pydantic import BaseModel
from typing import List

class ThreadBase(BaseModel):
    FID: str
    organization: str
    messages: List[str] = []

class ThreadCreate(ThreadBase):
    pass

class Thread(ThreadBase):
    class Config:
        from_attributes = True 