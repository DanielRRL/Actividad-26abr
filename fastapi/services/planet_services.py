from fastapi.schemas.planet_schemas import PlanetCreate, PlanetUpdate, PlanetResponse
from fastapi.repositories.planet_repository import PlanetRepository
from sqlalchemy.orm import Session
from typing import List, Optional


class PlanetService:
    def __init__(self, db: Session):
        """
        Initializes the service with a database session.
        """
        self.repository = PlanetRepository(db)

    def get_all_planets(self, skip: int = 0, limit: int = 10) -> List[PlanetResponse]:
        """
        Retrieves all planets with pagination.
        """
        planets = self.repository.get_all_planets(skip=skip, limit=limit)
        return [PlanetResponse.from_orm(planet) for planet in planets]

    def get_planet_by_id(self, planet_id: int) -> Optional[PlanetResponse]:
        """
        Retrieves a planet by its ID.
        """
        planet = self.repository.get_planet_by_id(planet_id)
        if not planet:
            return None
        return PlanetResponse.from_orm(planet)

    def create_planet(self, planet_data: PlanetCreate) -> PlanetResponse:
        """
        Creates a new planet.
        """
        new_planet = self.repository.create_planet(Planet(**planet_data.dict()))
        return PlanetResponse.from_orm(new_planet)

    def update_planet(self, planet_id: int, planet_data: PlanetUpdate) -> Optional[PlanetResponse]:
        """
        Updates an existing planet.
        """
        updated_planet = self.repository.update_planet(planet_id, planet_data.dict(exclude_unset=True))
        if not updated_planet:
            return None
        return PlanetResponse.from_orm(updated_planet)

    def delete_planet(self, planet_id: int) -> bool:
        """
        Deletes a planet by its ID.
        """
        deleted_planet = self.repository.delete_planet(planet_id)
        return deleted_planet is not None