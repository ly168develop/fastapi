import os
import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError

from app.models.user_model import User
from app.schemas.users import UserCreate, UserResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.database import get_db

def get_all_user(db: Session):
    statement = select(User)
    result = db.scalars(statement).all()
    
    return result

def get_user_detail(db: Session, user_id = int):
    user = db.get(User, user_id)
    
    if user is None:
        return None;

    return user

def create_new_user(user: UserCreate, db: Session):
    
    existing = db.scalar(
        select(User).where(
            (User.email == user.email) |
            (User.username == user.username)
        )
    )
    
    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail="Email or username already exists"
        )

    new_user = User(
        fullname = user.fullname,
        email = user.email,
        username = user.username,
        password_hash = hash_password(user.password)
    )
    
    db.add(new_user)
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email or username already exists"
        )
        
    db.refresh(new_user)
    
    return new_user


    
def login_user(
    username: str,
    password: str,
    db: Session
):
    user = db.scalar(
        select(User).where(User.username == username)
    )

    if user is None or not verify_password(
        password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    error = HTTPException(
        status_code=401,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(
            token,
            os.environ["JWT_SECRET_KEY"],
            algorithms=["HS256"]
        )

        user_id = int(payload["sub"])

    except (InvalidTokenError, KeyError, ValueError, TypeError):
        raise error

    user = db.get(User, user_id)

    if user is None:
        raise error

    return user


def require_admin(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin permission required"
        )

    return current_user

def require_role(allowed_roles: list[str]):
    def check_role(
        current_user: User = Depends(get_current_user)
    ):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )

        return current_user

    return check_role