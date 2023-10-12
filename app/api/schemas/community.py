# app/models/community.py
from datetime import datetime
from pydantic import BaseModel


class CommentBase(BaseModel):
    text: str
    timestamp: datetime


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    user_id: int
    project_id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ImageBase(BaseModel):
    image_url: str
    description: str
    timestamp: datetime


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    id: int
    user_id: int
    project_id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True