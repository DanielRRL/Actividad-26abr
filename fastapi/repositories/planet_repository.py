from sqlalchemy.orm import Session
from fastapi.models.planet import Planet
from sqlalchemy.exc import IntegrityError


class PlanetRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_planets(self, skip: int = 0, limit: int = 10):
        """Retrieve all planets from the database with pagination."""
        return self.db.query(Planet).offset(skip).limit(limit).all()

    def get_planet_by_id(self, planet_id: int):
        """Retrieve a planet by its ID."""
        return self.db.query(Planet).filter(Planet.id == planet_id).first()

    def create_planet(self, planet: Planet):
        """Create a new planet in the database."""
        try:
            self.db.add(planet)
            self.db.commit()
            self.db.refresh(planet)
            return planet
        except IntegrityError:
            self.db.rollback()
            raise ValueError("A planet with this name already exists.")

    def update_planet(self, planet_id: int, updated_data: dict):
        """Update an existing planet."""
        planet = self.get_planet_by_id(planet_id)
        if not planet:
            return None
        for key, value in updated_data.items():
            setattr(planet, key, value)
        self.db.commit()
        self.db.refresh(planet)
        return planet

    def delete_planet(self, planet_id: int):
        """Delete a planet by its ID."""
        planet = self.get_planet_by_id(planet_id)
        if not planet:
            return None
        self.db.delete(planet)
        self.db.commit()
        return planet