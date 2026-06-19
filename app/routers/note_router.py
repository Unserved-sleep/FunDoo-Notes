from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.auth import get_current_user

from app.config.database import get_db
from app.models.note import Note
from app.models.user import User
from app.schemas.note_schema import (
    NoteCreate,
    NoteUpdate,
    NoteResponse
)

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)
@router.post("/")
def create_note(
        note: NoteCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):

    new_note = Note(
        title=note.title,
        description=note.description,
        user_id=current_user.id
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


@router.get(
    "/",
    response_model=list[NoteResponse]
)
@router.get(
    "/",
    response_model=list[NoteResponse]
)
def get_notes(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):

    return db.query(Note).filter(
        Note.user_id == current_user.id
    ).all()
@router.get("/{note_id}")
def get_note(
        note_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return note


@router.put("/{note_id}")
def update_note(
        note_id: int,
        note_data: NoteUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    if note_data.title is not None:
        note.title = note_data.title

    if note_data.description is not None:
        note.description = note_data.description

    if note_data.is_archived is not None:
        note.is_archived = note_data.is_archived

    if note_data.is_trashed is not None:
        note.is_trashed = note_data.is_trashed

    db.commit()
    db.refresh(note)

    return note


@router.delete("/{note_id}")
def delete_note(
        note_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    db.delete(note)
    db.commit()

    return {
        "message": "Note deleted successfully"
    }


@router.patch("/{note_id}/archive")
def archive_note(
        note_id: int,
        db: Session = Depends(get_db)
):

    note = db.query(Note).filter(
        Note.id == note_id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    note.is_archived = True

    db.commit()

    return {
        "message": "Note archived"
    }


@router.patch("/{note_id}/trash")
def trash_note(
        note_id: int,
        db: Session = Depends(get_db)
):

    note = db.query(Note).filter(
        Note.id == note_id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    note.is_trashed = True

    db.commit()

    return {
        "message": "Note moved to trash"
    }