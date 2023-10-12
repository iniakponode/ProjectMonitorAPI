# app/queries/certificates.py
from sqlalchemy.orm import Session
from app.api.database.models import Certificate
from app.api.schemas.certificate import CertificateCreate


async def get_certificate_by_id(db: Session, certificate_id: int):
    return db.query(Certificate).filter(Certificate.id == certificate_id).first()


async def get_certificates(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Certificate).offset(skip).limit(limit).all()


async def create_certificate(db: Session, certificate: CertificateCreate):
    db_certificate = Certificate(**certificate.model_dump())
    db.add(db_certificate)
    db.commit()
    db.refresh(db_certificate)
    return db_certificate


# async def update_certificate(db: Session, certificate_id: int, certificate: CertificateUpdate):
#     db_certificate = get_certificate_by_id(db, certificate_id)
#     if db_certificate:
#         for key, value in certificate.dict().items():
#             setattr(db_certificate, key, value)
#         db.commit()
#         db.refresh(db_certificate)
#     return db_certificate


async def delete_certificate(db: Session, certificate_id: int):
    db_certificate = get_certificate_by_id(db, certificate_id)
    if db_certificate:
        db.delete(db_certificate)
        db.commit()
    return db_certificate
