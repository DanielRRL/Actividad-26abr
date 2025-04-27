from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from fastapi.db.database import Base


class Planet(Base):
    """
    Database model to represent a planet.
    """
    __tablename__ = "planets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)  # Added unique constraint
    description = Column(String(255), nullable=True)

    # One-to-many relationship with Satellite
    satellites = relationship(
        "Satellite",
        back_populates="planet",
        cascade="all, delete-orphan"  # Remove related satellites when deleting a planet
    )