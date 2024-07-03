from datetime import datetime
import ulid
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
import logging
from app.solid_integration.solid_client import SolidClient
from app.models.note import NoteRequest, NoteUpdateRequest, NoteResponse, NoteListResponse

class Settings(BaseSettings):
    """ Settings class """
    solid_username: str
    solid_password: str
    solid_community_url: str
    solid_pod_url: str
    solid_account_url: str
    token_url: str

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
    settings.solid_account_url,
    settings.solid_pod_url,
    settings.token_url,
    "notes/"  # Assuming notes/ is the container
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/notes/", response_model=NoteResponse, response_description="Create a note")
async def create_note(note: NoteRequest):
    """ Create a note """
    date = datetime.now().isoformat()
    subject = note.content[:100]
    note_id = str(ulid.new())
    
    note_created = await solid_client.create_note_in_solid(note_id, note.title, subject, note.content, date)
    if note_created:
        return {"id": note_id, "title": note.title, "subject": subject, "content": note.content, "date": date}
    else:
        raise HTTPException(status_code=500, detail="Failed to create note")

@app.get("/notes/", response_model=NoteListResponse)
async def read_notes(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1)):
    """ Read notes with pagination """
    notes = await solid_client.get_notes_from_solid()
    paginated_notes = notes[skip: skip + limit]
    return {"total": len(notes), "notes": paginated_notes}

@app.put("/notes/{note_id}", response_model=NoteResponse, response_description="Update a note")
async def update_note(note_id: str, note: NoteUpdateRequest):
    """ Update a note """
    date = datetime.now().isoformat()
    subject = note.content[:100]
    success = await solid_client.update_note_in_solid(note_id, note.title, subject, note.content, date)
    if success:
        return {"id": note_id, "title": note.title, "subject": subject, "content": note.content, "date": date}
    else:
        raise HTTPException(status_code=500, detail="Failed to update note")

@app.delete("/notes/{note_id}", response_description="Delete a note")
async def delete_note(note_id: str):
    """ Delete a note """
    success = await solid_client.delete_note_in_solid(note_id)
    if success:
        return {"message": "Note deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete note")
