from sqlalchemy import Table, Column, Integer, ForeignKey
from app.config.database import Base

note_labels = Table(
    "note_labels",
    Base.metadata,

    Column(
        "note_id",
        Integer,
        ForeignKey("notes.id", ondelete="CASCADE"),
        primary_key=True
    ),

    Column(
        "label_id",
        Integer,
        ForeignKey("labels.id", ondelete="CASCADE"),
        primary_key=True
    )
)