from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db

from app.models.label import Label
from app.models.note import Note

from app.schemas.label_schema import (
    LabelCreate,
    LabelResponse
)

router = APIRouter(
    prefix="/labels",
    tags=["Labels"]
)

@router.post(
    "/",
    response_model=LabelResponse
)
def create_label(
        label: LabelCreate,
        db: Session = Depends(get_db)
):

    existing = db.query(Label).filter(
        Label.name == label.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Label already exists"
        )

    new_label = Label(
        name=label.name
    )

    db.add(new_label)
    db.commit()
    db.refresh(new_label)

    return new_label


@router.get(
    "/",
    response_model=list[LabelResponse]
)
def get_labels(
        db: Session = Depends(get_db)
):

    return db.query(Label).all()

@router.delete("/{label_id}")
def delete_label(
        label_id: int,
        db: Session = Depends(get_db)
):

    label = db.query(Label).filter(
        Label.id == label_id
    ).first()

    if not label:
        raise HTTPException(
            status_code=404,
            detail="Label not found"
        )

    db.delete(label)

    db.commit()

    return {
        "message": "Label deleted"
    }


@router.post(
    "/{label_id}/notes/{note_id}"
)
def assign_label(
        label_id: int,
        note_id: int,
        db: Session = Depends(get_db)
):

    label = db.query(Label).filter(
        Label.id == label_id
    ).first()

    note = db.query(Note).filter(
        Note.id == note_id
    ).first()

    if not label:
        raise HTTPException(
            404,
            "Label not found"
        )

    if not note:
        raise HTTPException(
            404,
            "Note not found"
        )

    if label in note.labels:
        return {
            "message":
                "Label already assigned"
        }

    note.labels.append(label)

    db.commit()

    return {
        "message":
            "Label assigned successfully"
    }


@router.delete(
    "/{label_id}/notes/{note_id}"
)
def remove_label(
        label_id: int,
        note_id: int,
        db: Session = Depends(get_db)
):

    label = db.query(Label).filter(
        Label.id == label_id
    ).first()

    note = db.query(Note).filter(
        Note.id == note_id
    ).first()

    if not label or not note:
        raise HTTPException(
            404,
            "Not Found"
        )

    if label not in note.labels:
        return {
            "message":
                "Label not assigned"
        }

    note.labels.remove(label)

    db.commit()

    return {
        "message":
            "Label removed"
    }