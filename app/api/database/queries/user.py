# app/queries/user.py
from sqlalchemy.orm import Session
from app.api.database.models import User
from app.api.security.auth import get_password_hash


def create_user(db: Session, em: str, passw: str, fullname: str, act: bool):
    """
    Create a new user.

    Args:
        - db (Session): Database session.
        - user_data (dict): User data to create.

    Returns:
        - User: Created user.
    """
    encryptedPass = get_password_hash(passw)
    user_data = User(email=em, password=encryptedPass[:6], full_name=fullname, active=act)

    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data


def get_user_by_username(db: Session, email: str):
    """
    Retrieve a user by username.

    Args:
        - db (Session): Database session.
        - username (str): Username of the user to retrieve.

    Returns:
        - User: User details if found, or None if the user does not exist.
    """
    return db.query(User).filter(User.email == email).first()


def login_user(db: Session, username: str, password: str):
    """
    Authenticate a user.

    Args:
        - db (Session): Database session.
        - username (str): User's username.
        - password (str): User's password.

    Returns:
        - User: Authenticated user.
    """
    user = db.query(User).filter(User.email == username).first()

    encryptedPass = get_password_hash(password)

    if user and user.password == encryptedPass:
        return user
    return None


def get_user_by_id(db: Session, user_id: int):
    """
    Retrieve a user by ID.

    Args:
        - db (Session): Database session.
        - user_id (int): User's unique identifier.

    Returns:
        - User: Retrieved user.
    """
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, user_data: dict):
    """
    Update user information.

    Args:
        - db (Session): Database session.
        - user_id (int): User's unique identifier.
        - user_data (dict): Updated user data.

    Returns:
        - User: Updated user.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in user_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user


def delete_user(db: Session, user_id: int):
    """
    Delete user account.

    Args:
        - db (Session): Database session.
        - user_id (int): User's unique identifier.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
