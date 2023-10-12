# app/queries/project.py
from sqlalchemy.orm import Session, joinedload
from app.api.database.models import Project, Comment, Images


def create_project(db: Session, project_data: dict):
    """
    Create a new project.

    Args:
        - db (Session): Database session.
        - project_data (dict): Project information to create.

    Returns:
        - Project: Created project.
    """
    project = Project(**project_data)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def get_project_by_id(db: Session, project_id: int):
    """
    Retrieve a project by ID with associated users and other related entities.

    Args:
        - db (Session): Database session.
        - project_id (int): Project's unique identifier.

    Returns:
        - Project: Retrieved project with associated users and related entities.
    """
    return db.query(Project). \
        filter(Project.id == project_id). \
        options(
            joinedload(Project.contractors),  # Eager load contractors
            joinedload(Project.ministry_contact_officers),  # Eager load ministry contact officers
            # Add eager loads for other related entities as needed
        ). \
        first()

def update_project(db: Session, project_id: int, project_data: dict):
    """
    Update a project.

    Args:
        - db (Session): Database session.
        - project_id (int): Project's unique identifier.
        - project_data (dict): Updated project information.

    Returns:
        - Project: Updated project.
    """
    project = get_project_by_id(db, project_id)
    if project:
        for key, value in project_data.items():
            setattr(project, key, value)
        db.commit()
        db.refresh(project)
    return project


def delete_project(db: Session, project_id: int):
    """
    Delete a project.

    Args:
        - db (Session): Database session.
        - project_id (int): Project's unique identifier.
    """
    project = get_project_by_id(db, project_id)
    if project:
        db.delete(project)
        db.commit()


def create_comment_for_project(db: Session, comment_data: dict):
    """
    Create a comment for a project.

    Args:
        - db (Session): Database session.
        - comment_data (dict): Comment information to create.

    Returns:
        - Comment: Created comment.
    """
    comment = Comment(**comment_data)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comments_for_project(db: Session, project_id: int):
    """
    Retrieve comments for a project.

    Args:
        - db (Session): Database session.
        - project_id (int): Project's unique identifier.

    Returns:
        - List[Comment]: List of comments for the project.
    """
    return db.query(Comment).filter(Comment.project_id == project_id).all()


def create_image_for_project(db: Session, image_data: dict):
    """
    Create an image for a project.

    Args:
        - db (Session): Database session.
        - image_data (dict): Image information to create.

    Returns:
        - Image: Created image.
    """
    image = Images(**image_data)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


def get_images_for_project(db: Session, project_id: int):
    """
    Retrieve images for a project.

    Args:
        - db (Session): Database session.
        - project_id (int): Project's unique identifier.

    Returns:
        - List[Image]: List of images for the project.
    """
    return db.query(Images).filter(Images.project_id == project_id).all()
