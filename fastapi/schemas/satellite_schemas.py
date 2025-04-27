from pydantic import BaseModel, Field
from typing import Optional


class SatelliteBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    planet_id: int


class SatelliteCreate(SatelliteBase):
    pass


class SatelliteUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)


class SatelliteResponse(SatelliteBase):
    id: int

    class Config:
        orm_mode = True