# app/schemas/project.py
from pydantic import BaseModel
from datetime import datetime
from typing import List


class ProjectBase(BaseModel):
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    budget: float
    status: str
    user_id: int


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
