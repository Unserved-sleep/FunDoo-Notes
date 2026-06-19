from fastapi import FastAPI
from app.config.database import Base, engine

from app.models.user import User
from app.models.note import Note
from app.models.label import Label
from app.models.note_label import note_labels
from app.routers.label_router import (
    router as label_router
)
from app.routers.user_router import router as user_router
from app.routers.note_router import router as note_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fundoo Notes API"
)

app.include_router(user_router)
app.include_router(note_router)
app.include_router(label_router)


@app.get("/")
def home():
    return {
        "message": "Fundoo Notes API Running"
    }