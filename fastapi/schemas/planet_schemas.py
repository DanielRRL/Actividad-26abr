from pydantic import BaseModel, Field
from typing import List, Optional


class SatelliteBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)


class PlanetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)


class PlanetCreate(PlanetBase):
    pass


class PlanetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)


class PlanetResponse(PlanetBase):
    id: int
    satellites: List[SatelliteBase] = []

    class Config:
        orm_mode = True