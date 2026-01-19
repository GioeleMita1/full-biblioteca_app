from fastapi import APIRouter, Depends
from config.database import get_db
from services.user_service import UserService
from schemas.user_schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def get_users(db=Depends(get_db)):
    return UserService.get_all_users(db)

@router.get("/{user_id}")
def get_user(user_id: int, db=Depends(get_db)):
    return UserService.get_user_by_id(db, user_id)

@router.post("/", status_code=201)
def create_user(user_data: UserCreate, db=Depends(get_db)):
    return UserService.create_user(db, user_data)
