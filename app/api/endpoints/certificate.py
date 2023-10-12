# app/api/certificate.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.database.base import Base, engine
from app.api.database.models import User
from app.api.database.dependency.db_instance import get_db  # Import an asynchronous database session
from app.api.security.auth import get_current_user
from app.api.database.queries.certificate import (
    get_certificate_by_id,
    create_certificate,
    # update_certificate,
    delete_certificate,
)
from app.api.schemas.certificate import CertificateCreate, Certificate
Base.metadata.create_all(bind=engine)
router = APIRouter()


@router.post("/certificates", response_model=Certificate, summary="Create a new certificate")
async def create_certificate(
        certificate: CertificateCreate,
        current_user: User = Depends(get_current_user),  # Authorization check
        db: Session = Depends(get_db)  # Use an asynchronous database session
):
    """
    Create a new certificate.

    This endpoint allows users to create a new certificate.

    Args:
        - certificate (CertificateCreate): Certificate information to create.

    Returns:
        - Certificate: Created certificate information.
    """
    # Implement authorization logic if needed
    # For example, you can check if the current_user has the necessary permissions
    # Here, current_user will contain the authenticated user based on the JWT token
    if not current_user:
        raise HTTPException(status_code=401, detail="User is not logged in")  # You can check if the user is logged in

    # Create the certificate in the database
    created_certificate = await create_certificate(db, certificate)

    return created_certificate


@router.get("/certificates/{certificate_id}", response_model=Certificate, summary="Retrieve a certificate")
async def read_certificate(
        certificate_id: int,
        db: Session = Depends(get_db)  # Use an asynchronous database session
):
    """
    Retrieve a certificate by its ID.

    Args:
        - certificate_id (int): Certificate's unique identifier.

    Returns:
        - Certificate: Retrieved certificate information.
    """
    certificate = await get_certificate_by_id(db, certificate_id)
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return certificate


# @router.put("/certificates/{certificate_id}", response_model=Certificate, summary="Update a certificate")
# async def update_certificate_endpoint(
#         certificate_id: int,
#         certificate_update: CertificateUpdate,
#         current_user: User = Depends(get_current_user),  # Authorization check
#         db: Session = Depends(get_db)  # Use an asynchronous database session
# ):
#     """
#     Update a certificate by its ID.
#
#     This endpoint allows users to update an existing certificate.
#
#     Args:
#         - certificate_id (int): Certificate's unique identifier.
#         - certificate_update (CertificateCreate): Updated certificate information.
#
#     Returns:
#         - Certificate: Updated certificate information.
#     """
#     db_certificate = await get_certificate_by_id(db, certificate_id)
#     if not db_certificate:
#         raise HTTPException(status_code=404, detail="Certificate not found")
#
#     # Implement authorization logic if needed
#     # For example, you can check if the current_user has the necessary permissions
#
#     updated_certificate = await update_certificate(db, certificate_id, certificate_update)
#     return updated_certificate


@router.delete("/certificates/{certificate_id}", summary="Delete a certificate")
async def delete_certificate_endpoint(
        certificate_id: int,
        current_user: User = Depends(get_current_user),  # Authorization check
        db: Session = Depends(get_db)  # Use an asynchronous database session
):
    """
    Delete a certificate by its ID.

    This endpoint allows users to delete an existing certificate.

    Args:
        - certificate_id (int): Certificate's unique identifier.

    Returns:
        - dict: A message confirming successful deletion.
    """
    db_certificate = await get_certificate_by_id(db, certificate_id)
    if not db_certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")

    # Implement authorization logic if needed
    # For example, you can check if the current_user has the necessary permissions

    await delete_certificate(db, certificate_id)
    return {"message": "Certificate deleted successfully"}
