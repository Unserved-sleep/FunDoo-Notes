from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.models.note_label import note_labels


class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(50), nullable=False, unique=True)

    notes = relationship(
        "Note",
        secondary=note_labels,
        back_populates="labels"
    )