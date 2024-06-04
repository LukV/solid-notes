from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.models.note import NoteCreate
from app.solid_integration.solid_client import SolidClient
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    solid_username: str
    solid_password: str
    solid_community_url: str
    solid_pod_url: str

    class Config:
        env_file = ".env"

settings = Settings()

app = FastAPI()

origins = [
    "http://localhost:8080", 
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

solid_client = SolidClient(
    settings.solid_username,
    settings.solid_password,
    settings.solid_community_url,
    settings.solid_pod_url
    )

@app.post("/notes/")
async def create_note(note: NoteCreate):
    date = datetime.now().isoformat()
    subject = note.content[:100]
    success = solid_client.create_note_in_solid(note.title, subject, note.content, date)
    if success:
        return {"message": "Note created successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to create note")

@app.get("/notes/")
async def read_notes():
    notes = solid_client.get_notes_from_solid()
    return notes
