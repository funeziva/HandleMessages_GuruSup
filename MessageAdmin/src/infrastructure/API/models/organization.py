from pydantic import BaseModel

class OrganizationBase(BaseModel):
    organization: str

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    class Config:
        from_attributes = True 