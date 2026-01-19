# service per User
from fastapi import HTTPException
from repositories.user_repository import UserRepository
from schemas.user_schemas import UserCreate, UserResponse

class UserService:
    @staticmethod
    def get_all_users(db):
        users = UserRepository.get_all(db)
        return [UserResponse.model_validate(user) for user in users]

    @staticmethod
    def get_user_by_id(db, user_id):
        user = UserRepository.get_by_id(db, user_id)
        if user == None:
            raise HTTPException(status_code=404, detail="Utente non trovato")
        return UserResponse.model_validate(user)

    @staticmethod
    def create_user(db, user_data):
        existing_user = UserRepository.get_by_email(db, user_data.email)
        if existing_user != None:
            raise HTTPException(status_code=400, detail="Email già esistente")
        created = UserRepository.create(db, user_data.model_dump())
        return UserResponse.model_validate(created)
