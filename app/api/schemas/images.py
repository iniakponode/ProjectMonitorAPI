from pydantic import BaseModel
from datetime import datetime

class ImageBase(BaseModel):
    image_url: str
    description: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int
    user_id: int
    project_id: int
    timestamp: datetime

    class Config:
        orm_mode = True
