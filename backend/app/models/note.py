""" Pydantic models for Note """
from pydantic import BaseModel

class NoteCreate(BaseModel):
    """ Pydantic model for creating a note """
    title: str
    content: str
