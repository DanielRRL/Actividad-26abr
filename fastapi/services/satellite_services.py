from fastapi.schemas.satellite_schemas import SatelliteCreate, SatelliteUpdate, SatelliteResponse
from fastapi.repositories.satellite_repository import SatelliteRepository
from sqlalchemy.orm import Session
from typing import List, Optional


class SatelliteService:
    def __init__(self, db: Session):
        """
        Initializes the service with a database session.
        """
        self.repository = SatelliteRepository(db)

    def get_all_satellites(self, skip: int = 0, limit: int = 10) -> List[SatelliteResponse]:
        """
        Retrieves all satellites with pagination.
        """
        satellites = self.repository.get_all_satellites(skip=skip, limit=limit)
        return [SatelliteResponse.from_orm(satellite) for satellite in satellites]

    def get_satellite_by_id(self, satellite_id: int) -> Optional[SatelliteResponse]:
        """
        Retrieves a satellite by its ID.
        """
        satellite = self.repository.get_satellite_by_id(satellite_id)
        if not satellite:
            return None
        return SatelliteResponse.from_orm(satellite)

    def create_satellite(self, satellite_data: SatelliteCreate) -> SatelliteResponse:
        """
        Creates a new satellite.
        """
        new_satellite = self.repository.create_satellite(Satellite(**satellite_data.dict()))
        return SatelliteResponse.from_orm(new_satellite)

    def update_satellite(self, satellite_id: int, satellite_data: SatelliteUpdate) -> Optional[SatelliteResponse]:
        """
        Updates an existing satellite.
        """
        updated_satellite = self.repository.update_satellite(satellite_id, satellite_data.dict(exclude_unset=True))
        if not updated_satellite:
            return None
        return SatelliteResponse.from_orm(updated_satellite)

    def delete_satellite(self, satellite_id: int) -> bool:
        """
        Deletes a satellite by its ID.
        """
        deleted_satellite = self.repository.delete_satellite(satellite_id)
        return deleted_satellite is not None