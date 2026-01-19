# Repository per User
from sqlalchemy.orm import Session
from models.user import User

class UserRepository:

    @staticmethod
    def get_all(db):
        return db.query(User).all()

    @staticmethod
    def get_by_id(db, user_id):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(db, email):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(db, user_data):
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
