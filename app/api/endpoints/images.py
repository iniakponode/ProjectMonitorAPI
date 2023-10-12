from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.database.dependency.db_instance import get_db
from app.api.schemas.user import User
from app.api.security.auth import get_current_user
from app.api.schemas.images import Image, ImageCreate
from app.api.database.queries.images import create_image, get_image_by_id, get_images_for_project

router = APIRouter()


@router.post("/images", response_model=Image, summary="Upload an image")
def upload_image(
        image: ImageCreate,
        current_user: User = Depends(get_current_user),  # Authorization check
        db: Session = Depends(get_db)
):
    """
    Upload an image.

    This endpoint allows users to upload an image.

    - **image**: Image information to upload.

    Returns:
    - Uploaded image information.
    """
    image_data = image.dict()
    image_data["user_id"] = current_user.id
    uploaded_image = create_image(db, image_data)
    return uploaded_image


@router.get("/images/{image_id}", response_model=Image, summary="Retrieve an image")
def retrieve_image(
        image_id: int,
        db: Session = Depends(get_db)
):
    """
    Retrieve an image by ID.

    - **image_id**: Image's unique identifier.

    Returns:
    - Retrieved image information.
    """
    image = get_image_by_id(db, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@router.get("/projects/{project_id}/images", response_model=List[Image], summary="Retrieve images for a project")
def retrieve_images_for_project(
        project_id: int,
        db: Session = Depends(get_db)
):
    """
    Retrieve images for a project.

    - **project_id**: Project's unique identifier.

    Returns:
    - List of images for the project.
    """
    images = get_images_for_project(db, project_id)
    return images
