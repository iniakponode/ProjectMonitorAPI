# app/api/project.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.database.base import engine, Base
from app.api.database.dependency.db_instance import get_db
from app.api.security.auth import get_current_user, get_current_admin_user
from app.api.database.models import User
from app.api.schemas.project import ProjectCreate, Project
from app.api.schemas.community import CommentCreate, Image, ImageCreate, Comment
from app.api.database.models import Images
from app.api.database.queries.project import (
    create_project,
    get_project_by_id,
    update_project,
    delete_project,
    create_comment_for_project,
    get_comments_for_project,
    create_image_for_project,
    get_images_for_project,
)
from typing import List
Base.metadata.create_all(bind=engine)
router = APIRouter()


@router.post("/projects", response_model=Project, summary="Create a new project")
def create_new_project(
        project: ProjectCreate,
        current_user: User = Depends(get_current_user),  # Authorization check
        db: Session = Depends(get_db)
):
    """
    Create a new project.

    This endpoint allows users to create a new project.

    - **project**: Project information to create.

    Returns:
    - Created project information.
    """
    created_project = create_project(db, project.dict())
    return created_project


@router.get("/projects/{project_id}", response_model=Project, summary="Retrieve a project")
def retrieve_project(
        project_id: int,
        current_user: User = Depends(get_current_user),  # Authorization check
        db: Session = Depends(get_db)
):
    """
    Retrieve a project by ID.

    - **project_id**: Project's unique identifier.

    Returns:
    - Retrieved project information.
    """
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/projects/{project_id}", response_model=Project, summary="Update a project")
def update_existing_project(
        project_id: int,
        project: ProjectCreate,
        current_user: User = Depends(get_current_admin_user),  # Authorization check (admin)
        db: Session = Depends(get_db)
):
    """
    Update a project.

    - **project_id**: Project's unique identifier.
    - **project**: Updated project information.

    Returns:
    - Updated project information.
    """
    updated_project = update_project(db, project_id, project.dict())
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project


@router.delete("/projects/{project_id}", summary="Delete a project")
def delete_existing_project(
        project_id: int,
        current_user: User = Depends(get_current_admin_user),  # Authorization check (admin)
        db: Session = Depends(get_db)
):
    """
    Delete a project.

    - **project_id**: Project's unique identifier.
    """
    delete_project(db, project_id)
    return {"message": "Project deleted successfully"}


@router.post("/projects/{project_id}/comments", response_model=Comment, summary="Create a comment for a project")
def create_comment_for_project(
        project_id: int,
        comment: CommentCreate,
        current_user: User = Depends(get_current_user),  # Authorization check
        db: Session = Depends(get_db)
):
    """
    Create a comment for a project.

    - **project_id**: Project's unique identifier.
    - **comment**: Comment information to create.

    Returns:
    - Created comment information.
    """
    comment_data = comment.dict()
    comment_data["project_id"] = project_id
    created_comment = create_comment_for_project(db, comment_data)
    return created_comment


@router.get("/projects/{project_id}/comments", response_model=List[Comment], summary="Retrieve comments for a project")
def retrieve_comments_for_project(
        project_id: int,
        current_user: User = Depends(get_current_user),  # Authorization check
        db: Session = Depends(get_db)
):
    """
    Retrieve comments for a project.

    - **project_id**: Project's unique identifier.

    Returns:
    - List of comments for the project.
    """
    comments = get_comments_for_project(db, project_id)
    return comments


@router.post("/projects/{project_id}/images", response_model=Image, summary="Upload an image for a project")
def upload_image_for_project(
        project_id: int,
        image: ImageCreate,
        current_user: User = Depends(get_current_user),  # Authorization check
        db: Session = Depends(get_db)
):
    """
    Upload an image for a project.

    - **project_id**: Project's unique identifier.
    - **image**: Image information to upload.

    Returns:
    - Uploaded image information.
    """
    image_data = image.model_dump()
    image_data["project_id"] = project_id
    uploaded_image = create_image_for_project(db, image_data)
    return uploaded_image


@router.get("/projects/{project_id}/images", response_model=List[Image], summary="Retrieve images for a project")
def retrieve_images_for_project(
        project_id: int,
        current_user: User = Depends(get_current_user),  # Authorization check
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
