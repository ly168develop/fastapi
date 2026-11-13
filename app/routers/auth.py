from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.schemas.users import UserCreate, UserResponse
from app.services import user_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return user_service.create_new_user(user, db)


class LoginRequest(BaseModel):
    username: str = Field(min_length=6)
    password: str = Field(min_length=6)

@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    return user_service.login_user(
        data.username,
        data.password,
        db
    )
    
@router.get("/me", response_model=UserResponse)
def get_profile(
    current_user: User = Depends(user_service.get_current_user)
):
    return current_user
