# app/api/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.database.base import engine, Base
from app.api.database.dependency.db_instance import get_db
from app.api.security.auth import get_current_user, get_current_admin_user
from app.api.schemas.user import UserCreate, User as u
from app.api.database.models import User
from app.api.database.queries.user import (
    create_user,
    login_user,
    get_user_by_id,
    update_user,
    delete_user, get_user_by_username,
)

Base.metadata.create_all(bind=engine)
router = APIRouter()


@router.post("/register", response_model=u, summary="Create a new user")
async def create_new_user(
        user: UserCreate,
        db: Session = Depends(get_db)
):
    """
      Create a new user.

      This endpoint allows users to create a new user account.

      - **user**: User information to create.

      Returns:
      - Created user information if registration is successful.
      - An appropriate error message if the user already exists.
      """
    existing_user = get_user_by_username(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this username already exists")

    created_user = create_user(db, user.email, user.password, user.full_name, 0)
    return created_user


@router.post("/login", response_model=u, summary="User authentication")
async def login_existing_user(
        username: str,
        password: str,
        db: Session = Depends(get_db)
):
    """
    User authentication.

    This endpoint allows users to authenticate using their username and password.

    - **username**: User's username.
    - **password**: User's password.

    Returns:
    - Authenticated user information.
    """
    user = login_user(db, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user


@router.get("/users/{user_id}", response_model=u, summary="Retrieve user information")
async def retrieve_user_info(
        user_id: int,
        current_user: User = Depends(get_current_user),  # Authorization check
        db: Session = Depends(get_db)
):
    """
    Retrieve user information by ID.

    - **user_id**: User's unique identifier.

    Returns:
    - Retrieved user information.
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=u, summary="Update user information")
async def update_user_info(
        user_id: int,
        user: UserCreate,
        current_user: User = Depends(get_current_admin_user),  # Authorization check (admin)
        db: Session = Depends(get_db)
):
    """
    Update user information.

    - **user_id**: User's unique identifier.
    - **user**: Updated user information.

    Returns:
    - Updated user information.
    """
    updated_user = await update_user(db, user_id, user.dict())
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/users/{user_id}", summary="Delete user account")
async def delete_user_account(
        user_id: int,
        current_user: User = Depends(get_current_admin_user),  # Authorization check (admin)
        db: Session = Depends(get_db)
):
    """
    Delete user account.

    - **user_id**: User's unique identifier.
    """
    delet = await delete_user(db, user_id)
    return dict(message="User account deleted successfully", data=delet)
