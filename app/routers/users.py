from fastapi import APIRouter, HTTPException, status, Depends
from app.services import user_service
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.users import UserCreate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    all_users = user_service.get_all_user(db)
    return all_users

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_detail = user_service.get_user_detail(db, user_id)
    if user_detail is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user_detail

@router.post("/", status_code=status.HTTP_200_OK)
def post(user: UserCreate, db: Session = Depends(get_db)):
    user = user_service.create_new_user(user, db)
    return user