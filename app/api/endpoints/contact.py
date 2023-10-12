# app/api/contact.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.database.base import Base, engine
from app.api.database.dependency.db_instance import get_db
from app.api.security.auth import get_current_user
from app.api.database.queries.contact import get_contractors_for_project, get_ministry_contact_officers_for_project
from app.api.schemas.user import User
from app.api.schemas.project import Project

from typing import List
Base.metadata.create_all(bind=engine)
router = APIRouter()


@router.get("/projects/{project_id}/contractors", response_model=List[User],
            summary="Retrieve contractors for a project")
async def retrieve_contractors_for_project(
        project_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    Retrieve contractors associated with a specific project.

    - **project_id**: Project's unique identifier.

    Returns:
    - List of contractor users associated with the project.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if the current user has permission to access the project information
    # (You may implement authorization logic here)

    contractors = get_contractors_for_project(db, project_id)
    return contractors


@router.get("/projects/{project_id}/ministry-contact-officers", response_model=List[User],
            summary="Retrieve ministry contact officers for a project")
async def retrieve_ministry_contact_officers_for_project(
        project_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    Retrieve ministry contact officers associated with a specific project.

    - **project_id**: Project's unique identifier.

    Returns:
    - List of ministry contact officer users associated with the project.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if the current user has permission to access the project information
    # (You may implement authorization logic here)

    ministry_contact_officers = get_ministry_contact_officers_for_project(db, project_id)
    return ministry_contact_officers
