# Repository per Libro
from sqlalchemy.orm import Session
from models.libro import Libro

class LibroRepository:

    @staticmethod
    def get_all(db):
        return db.query(Libro).all()

    @staticmethod
    def get_by_id(db, libro_id):
        return db.query(Libro).filter(Libro.id == libro_id).first()

    @staticmethod
    def get_by_isbn(db, isbn):
        return db.query(Libro).filter(Libro.isbn == isbn).first()

    @staticmethod
    def create(db, libro_data):
        libro = Libro(**libro_data)
        db.add(libro)
        db.commit()
        db.refresh(libro)
        return libro

    @staticmethod
    def update(db, libro):
        db.commit()
        db.refresh(libro)
        return libro
