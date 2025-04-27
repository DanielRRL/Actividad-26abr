from fastapi import APIRouter
from api.planet_routes import router as planet_router
from api.satellite_routes import router as satellite_router

main_router = APIRouter()
main_router.include_router(planet_router)
main_router.include_router(satellite_router)