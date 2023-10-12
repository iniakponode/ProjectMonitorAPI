from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Email address")
    full_name: str = Field(..., description="Full name")
    active: bool = Field(True, description="User's active status")


class UserCreate(UserBase):
    password: str = Field(..., description="Password")


class UserUpdate(BaseModel):
    email: EmailStr = Field(None, description="Updated email address (optional)")
    full_name: str = Field(None, description="Updated full name (optional)")
    password: str = Field(None, description="Updated password (optional)")


class User(UserBase):
    id: int = Field(..., description="User's unique identifier")
    roles: list = Field([], description="List of roles (e.g., Admin, Contractor, Community Member, etc.)")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
