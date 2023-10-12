# app/queries/contact.py
from sqlalchemy.orm import Session
from app.api.database.models import Project, User


def get_contractors_for_project(db: Session, project_id: int):
    """
    Retrieve contractors associated with a specific project.

    Args:
        - db (Session): Database session.
        - project_id (int): Project's unique identifier.

    Returns:
        - List[User]: List of contractor users associated with the project.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        return project.contractors
    return []


def get_ministry_contact_officers_for_project(db: Session, project_id: int):
    """
    Retrieve ministry contact officers associated with a specific project.

    Args:
        - db (Session): Database session.
        - project_id (int): Project's unique identifier.

    Returns:
        - List[User]: List of ministry contact officer users associated with the project.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        return project.ministry_contact_officers
    return []
