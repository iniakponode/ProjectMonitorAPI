# app/schemas/contract.py
from pydantic import BaseModel


class ContractBase(BaseModel):
    name: str
    details: str  # Add the details field
    project_id: int
    # Define other fields as needed


class ContractCreate(ContractBase):
    pass


class Contract(ContractBase):
    id: int
    project_id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
