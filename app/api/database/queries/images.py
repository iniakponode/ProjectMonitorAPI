from sqlalchemy.orm import Session
from app.api.database.models import Images


def create_image(db: Session, image_data: dict):
    new_image = Images(**image_data)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image


def get_image_by_id(db: Session, image_id: int):
    return db.query(Images).filter(Images.id == image_id).first()


def get_images_for_project(db: Session, project_id: int):
    return db.query(Images).filter(Images.project_id == project_id).all()
