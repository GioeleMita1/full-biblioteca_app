from fastapi import APIRouter, Depends
from config.database import get_db
from services.libro_service import LibroService
from schemas.libro_schemas import LibroCreate, LibroResponse

router = APIRouter(prefix="/libri", tags=["libri"])

@router.get("/")
def get_libri(db=Depends(get_db)):
    return LibroService.get_all_libri(db)

@router.get("/{libro_id}")
def get_libro(libro_id: int, db=Depends(get_db)):
    return LibroService.get_libro_by_id(db, libro_id)

@router.post("/", status_code=201)
def create_libro(libro_data: LibroCreate, db=Depends(get_db)):
    return LibroService.create_libro(db, libro_data)
