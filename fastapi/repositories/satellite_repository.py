from sqlalchemy.orm import Session
from fastapi.models.satellite import Satellite
from sqlalchemy.exc import IntegrityError


class SatelliteRepository:
    def __init__(self, db: Session):
        """
        Initializes the repository with a database session.
        """
        self.db = db

    def get_all_satellites(self, skip: int = 0, limit: int = 10):
        """
        Retrieves all satellites from the database with pagination.
        """
        return self.db.query(Satellite).offset(skip).limit(limit).all()

    def get_satellite_by_id(self, satellite_id: int):
        """
        Retrieves a satellite by its ID.
        """
        return self.db.query(Satellite).filter(Satellite.id == satellite_id).first()

    def create_satellite(self, satellite: Satellite):
        """
        Creates a new satellite in the database.
        """
        try:
            self.db.add(satellite)
            self.db.commit()
            self.db.refresh(satellite)
            return satellite
        except IntegrityError:
            self.db.rollback()
            raise ValueError("A satellite with this name already exists.")

    def update_satellite(self, satellite_id: int, updated_data: dict):
        """
        Updates an existing satellite.
        """
        satellite = self.get_satellite_by_id(satellite_id)
        if not satellite:
            return None
        for key, value in updated_data.items():
            setattr(satellite, key, value)
        self.db.commit()
        self.db.refresh(satellite)
        return satellite

    def delete_satellite(self, satellite_id: int):
        """
        Deletes a satellite by its ID.
        """
        satellite = self.get_satellite_by_id(satellite_id)
        if not satellite:
            return None
        self.db.delete(satellite)
        self.db.commit()
        return satellite