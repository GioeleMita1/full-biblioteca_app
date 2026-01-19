import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "email_service"))
sys.path.insert(0, str(Path.cwd() / "biblioteca_service"))

from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import users, libri, prenotazioni
from config.database import engine, Base
from pkg.api.email_controller import router as email_router
from pkg.services.sqs_consumer import start_sqs_worker_background

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app):
    ev = start_sqs_worker_background()
    if ev != None:
        app.state.sqs_worker_shutdown = ev
    yield
    if hasattr(app.state, "sqs_worker_shutdown"):
        app.state.sqs_worker_shutdown.set()

app = FastAPI(title="Biblioteca", lifespan=lifespan)

app.include_router(users.router)
app.include_router(libri.router)
app.include_router(prenotazioni.router)
app.include_router(email_router)

@app.get("/")
def root():
    return {"message": "Benvenuto alla Biblioteca API"}
