# app/security/auth.py
import os

import dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, ExpiredSignatureError
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from app.api.database.dependency.db_instance import get_db
from app.api.database.models import User
# load the .env file
dotenv.load_dotenv()
SECRET_KEY = os.getenv("SECRETE_KEY")
# Password hashing
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_context.hash(password)[:6]


# Define a function to generate JWT tokens for users
def create_access_token(data: dict, secret_key: str, algorithm: str = "HS256"):
    import datetime
    from jwt import encode

    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


# Secret key for JWT tokens (replace with your own secret)

# OAuth2PasswordBearer for token retrieval
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Define a function to get the current user based on the JWT token
def get_current_user(token: str = Depends(oauth2_scheme), db_session: Session = Depends(get_db)):
    try:
        payload = decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        user = db_session.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")


# Define a function to get the current admin user based on the JWT token
def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="User is not authorized to perform this action")
    return current_user
