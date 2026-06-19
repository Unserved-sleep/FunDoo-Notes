from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base
from app.models.note_label import note_labels

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    description = Column(Text, nullable=True)

    is_archived = Column(Boolean, default=False)

    is_trashed = Column(Boolean, default=False)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="notes"
    )

    labels = relationship(
        "Label",
        secondary=note_labels,
        back_populates="notes"
    )