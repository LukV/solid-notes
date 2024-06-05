""" Main module of the application """
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from app.solid_integration.solid_client import SolidClient
from app.models.note import NoteRequest, NoteUpdateRequest

class Settings(BaseSettings):
    """ Settings class """
    solid_username: str
    solid_password: str
    solid_community_url: str
    solid_pod_url: str

    class Config:
        """ Config class """
        env_file = ".env"
        extra = "forbid"

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

@app.post("/notes/", response_description="Create a note")
async def create_note(note: NoteRequest):
    """ Create a note """
    date = datetime.now().isoformat()
    subject = note.content[:100]
    success = solid_client.create_note_in_solid(note.title, subject, note.content, date)
    if success:
        return {"message": "Note created successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to create note")

@app.get("/notes/")
async def read_notes():
    """ Read notes """
    notes = solid_client.get_notes_from_solid()
    return notes

@app.put("/notes/{note_id}", response_description="Update a note")
async def update_note(note_id: str, note: NoteUpdateRequest):
    """ Update a note """
    date = datetime.now().isoformat()
    subject = note.content[:100]
    success = solid_client.update_note_in_solid(note_id, note.title, subject, note.content, date)
    if success:
        return {"message": "Note updated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to update note")

@app.delete("/notes/{note_id}", response_description="Delete a note")
async def delete_note(note_id: str):
    """ Delete a note """
    success = solid_client.delete_note_in_solid(note_id)
    if success:
        return {"message": "Note deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete note")