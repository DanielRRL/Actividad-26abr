from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from fastapi.db.database import Base


class Satellite(Base):
    __tablename__ = "satellites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)  # Added length and nullable constraint
    description = Column(String(255), nullable=True)  # Added length constraint
    planet_id = Column(Integer, ForeignKey("planets.id"), nullable=False)  # Added nullable constraint

    # Reverse relationship with Planet
    planet = relationship("Planet", back_populates="satellites")