from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.schemas.satellite_schemas import SatelliteCreate, SatelliteUpdate, SatelliteResponse
from fastapi.services.satellite_services import SatelliteService
from fastapi.db.session import get_db
from typing import List

router = APIRouter(prefix="/satellites", tags=["Satellites"])

@router.get("/", response_model=List[SatelliteResponse])
def get_all_satellites(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    service = SatelliteService(db)
    return service.get_all_satellites(skip=skip, limit=limit)

@router.get("/{satellite_id}", response_model=SatelliteResponse)
def get_satellite_by_id(satellite_id: int, db: Session = Depends(get_db)):
    service = SatelliteService(db)
    satellite = service.get_satellite_by_id(satellite_id)
    if not satellite:
        raise HTTPException(status_code=404, detail="Satellite not found")
    return satellite

@router.post("/", response_model=SatelliteResponse)
def create_satellite(satellite_data: SatelliteCreate, db: Session = Depends(get_db)):
    service = SatelliteService(db)
    return service.create_satellite(satellite_data)

@router.put("/{satellite_id}", response_model=SatelliteResponse)
def update_satellite(satellite_id: int, satellite_data: SatelliteUpdate, db: Session = Depends(get_db)):
    service = SatelliteService(db)
    updated_satellite = service.update_satellite(satellite_id, satellite_data)
    if not updated_satellite:
        raise HTTPException(status_code=404, detail="Satellite not found")
    return updated_satellite

@router.delete("/{satellite_id}", status_code=204)
def delete_satellite(satellite_id: int, db: Session = Depends(get_db)):
    service = SatelliteService(db)
    if not service.delete_satellite(satellite_id):
        raise HTTPException(status_code=404, detail="Satellite not found")