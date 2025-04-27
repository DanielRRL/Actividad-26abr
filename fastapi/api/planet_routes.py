from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.schemas.planet_schemas import PlanetCreate, PlanetUpdate, PlanetResponse
from fastapi.services.planet_services import PlanetService
from fastapi.db.session import get_db
from typing import List

router = APIRouter(prefix="/planets", tags=["Planets"])

@router.get("/", response_model=List[PlanetResponse])
def get_all_planets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    service = PlanetService(db)
    return service.get_all_planets(skip=skip, limit=limit)

@router.get("/{planet_id}", response_model=PlanetResponse)
def get_planet_by_id(planet_id: int, db: Session = Depends(get_db)):
    service = PlanetService(db)
    planet = service.get_planet_by_id(planet_id)
    if not planet:
        raise HTTPException(status_code=404, detail="Planet not found")
    return planet

@router.post("/", response_model=PlanetResponse)
def create_planet(planet_data: PlanetCreate, db: Session = Depends(get_db)):
    service = PlanetService(db)
    return service.create_planet(planet_data)

@router.put("/{planet_id}", response_model=PlanetResponse)
def update_planet(planet_id: int, planet_data: PlanetUpdate, db: Session = Depends(get_db)):
    service = PlanetService(db)
    updated_planet = service.update_planet(planet_id, planet_data)
    if not updated_planet:
        raise HTTPException(status_code=404, detail="Planet not found")
    return updated_planet

@router.delete("/{planet_id}", status_code=204)
def delete_planet(planet_id: int, db: Session = Depends(get_db)):
    service = PlanetService(db)
    if not service.delete_planet(planet_id):
        raise HTTPException(status_code=404, detail="Planet not found")