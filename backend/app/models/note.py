"""
Pydantic models for Note operations in the FastAPI application.

This module contains models for creating, updating, and responding with Note data,
including necessary validation to ensure data integrity.
"""

from pydantic import BaseModel, Field, field_validator

class NoteRequest(BaseModel):
    """
    Pydantic model for creating a note.

    Attributes:
        title (str): The title of the note. Must be non-empty and between 1 and 100 characters.
        content (str): The content of the note. Must be non-empty.
    """
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)

    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title must not be empty')
        return v

    @field_validator('content')
    @classmethod
    def content_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Content must not be empty')
        return v

class NoteUpdateRequest(NoteRequest):
    """
    Pydantic model for updating a note.

    Inherits all fields and validators from NoteRequest.
    """
    pass

class NoteResponse(BaseModel):
    """
    Pydantic model for responding with note details.

    Attributes:
        id (str): The unique identifier of the note.
        title (str): The title of the note.
        subject (str): A brief subject or summary of the note.
        content (str): The content of the note.
        date (str): The date when the note was created or last updated.
    """
    id: str
    title: str
    subject: str
    content: str
    date: str

class NoteListResponse(BaseModel):
    """
    Pydantic model for listing notes with pagination.

    Attributes:
        total (int): The total number of notes.
        notes (list[NoteResponse]): A list of notes.
    """
    total: int
    notes: list[NoteResponse]
