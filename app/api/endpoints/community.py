# app/api/community.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.database.base import Base, engine
from app.api.database.models import User
from app.api.database.dependency.db_instance import get_db
from app.api.security.auth import get_current_user
from app.api.database.queries.community import (
    get_comments_by_project_id,
    create_comment,
    get_images_by_project_id,
    create_image,
)
from app.api.schemas.community import CommentCreate, Comment, ImageCreate, Image
Base.metadata.create_all(bind=engine)
router = APIRouter()


@router.get("/projects/{project_id}/comments", response_model=list[Comment], summary="Retrieve comments for a project")
async def retrieve_comments_for_project(
        project_id: int,
        db: Session = Depends(get_db)
):
    try:
        comments = await get_comments_by_project_id(db, project_id)
        return comments
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/projects/{project_id}/comments", response_model=Comment, summary="Create a new comment for a project")
async def create_comment_for_project(
        project_id: int,
        comment_create: CommentCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    try:
        created_comment = await create_comment(db, comment_create.text, project_id, current_user.id)
        return created_comment
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/projects/{project_id}/images", response_model=list[Image], summary="Retrieve images for a project")
async def retrieve_images_for_project(
        project_id: int,
        db: Session = Depends(get_db)
):
    try:
        images = await get_images_by_project_id(db, project_id)
        return images
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/projects/{project_id}/images", response_model=Image, summary="Upload a new image for a project")
async def upload_image_for_project(
        project_id: int,
        image_create: ImageCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    try:
        created_image = await create_image(db, image_create.image_url, image_create.description, project_id,
                                           current_user.id)
        return created_image
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
