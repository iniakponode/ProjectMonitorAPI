# app/queries/community.py
from sqlalchemy.orm import Session
from app.api.database.models import Comment, Images
from app.api.database.models import User


def get_comments_by_project_id(db: Session, project_id: int):
    return db.query(Comment).filter(Comment.project_id == project_id).all()


def create_comment(db: Session, comment_text: str, project_id: int, user_id: int):
    db_comment = Comment(text=comment_text, project_id=project_id, user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_images_by_project_id(db: Session, project_id: int):
    return db.query(Images).filter(Images.project_id == project_id).all()


def create_image(db: Session, image_url: str, description: str, project_id: int, user_id: int):
    db_image = Images(image_url=image_url, description=description, project_id=project_id, user_id=user_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image
