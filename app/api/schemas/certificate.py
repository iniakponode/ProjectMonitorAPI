# app/models/certificate.py
from datetime import datetime
from pydantic import BaseModel


class CertificateBase(BaseModel):
    title: str
    description: str
    date_issued: datetime
    issuer: str


class CertificateCreate(CertificateBase):
    pass


class Certificate(CertificateBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
