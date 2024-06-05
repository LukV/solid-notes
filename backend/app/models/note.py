""" Pydantic models for Note """
from pydantic import BaseModel

class NoteRequest(BaseModel):
    """ Pydantic model for creating a note """
    title: str
    content: str

class NoteUpdateRequest(BaseModel):
    title: str
    content: str
