# service del libro
from fastapi import HTTPException
from repositories.libro_repository import LibroRepository
from schemas.libro_schemas import LibroCreate, LibroResponse

class LibroService:
    @staticmethod
    def get_all_libri(db):
        libri = LibroRepository.get_all(db)
        return [LibroResponse.model_validate(libro) for libro in libri]

    @staticmethod
    def get_libro_by_id(db, libro_id):
        libro = LibroRepository.get_by_id(db, libro_id)
        if libro == None:
            raise HTTPException(status_code=404, detail="Libro non trovato")
        return LibroResponse.model_validate(libro)

    @staticmethod
    def create_libro(db, libro_data):
        existing_libro = LibroRepository.get_by_isbn(db, libro_data.isbn)
        if existing_libro != None:
            raise HTTPException(status_code=400, detail="ISBN già esistente")
        created = LibroRepository.create(db, libro_data.model_dump())
        return LibroResponse.model_validate(created)
