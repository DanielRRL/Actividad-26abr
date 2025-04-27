from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship, declarative_base
import os

#Configuracion de la base de datos
#Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@mysql:3306/mydatabase")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocomit= False, autoflush= False, bind= engine)
Base = declarative_base()

#Modelos
#Models
class Planet(Base):
    _tablename_ = "planets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

    #Relacion de uno a muchos con Satelite
    #One-to-many relationship with Satellite
    satellites = relationship("Satellite", back_populates="planet")

class Satellite(Base):
    _tablename_ = "satellites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    planet_id = Column(Integer, ForeignKey("planets.id"))

    #Relacion inversa con Planeta
    #Reverse relationship with Planet
    planet = relationship("Planet", back_populates="satellites")

#Crear tablas
#Create tables
app = FastAPI(
    title="Planet and Satellites API",
    root_path="/api",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "persistAuthorization": True,
    },
)

#Dependencia para obtener la sesion de la base de datos
#Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to my API"}

#CRUD for Planets
@app.get("/planets/")
def read_planets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    planets = db.query(Planet).offset(skip).limit(limit).all()
    return planets

@app.post("/planets/", status_code=201)
def create_planet(name: str, description: str = None, db: Session = Depends(get_db)):
    planet = Planet(name=name, description=description)
    db.add(planet)
    db.commit()
    db.refresh(planet)
    return planet

@app.delete("/planets/{planet_id}")
def delete_planet(planet_id: int, db: Session = Depends(get_db)):
    planet = db.query(Planet).filter(Planet.id == planet_id).first()
    if planet is None:
        raise HTTPException(status_code=404, detail="Planet not found")
    db.delete(planet)
    db.commit()
    return {"message": "Planet deleted successfully"}

@app.get("/planets/{planet_id}/satellites")
def get_satellites_of_planet(planet_id: int, db: Session = Depends(get_db)):
    planet = db.query(Planet).filter(Planet.id == planet_id).first()
    if not planet:
        raise HTTPException(status_code=404, detail="Planet not found")
    return planet.satellites

#CRUD for satellite
@app.post("/planets/{planet_id}/satellites/", status_code=201)
def create_satellite(planet_id: int, name: str, description: str = None, db: Session = Depends(get_db)):
    planet = db.query(Planet).filter(Planet.id == planet_id).first()
    if not planet:
        raise HTTPException(status_code=404, detail="Planet not found")
    satellite = Satellite(name=name, description=description, planet_id=planet_id)
    db.add(satellite)
    db.commit()
    db.refresh(satellite)
    return satellite

@app.get("/satellites/{satellite_id}")
def read_satellite(satellite_id: int, db: Session = Depends(get_db)):
    satellite = db.query(Satellite).filter(Satellite.id == satellite_id).first()
    if satellite is None:
        raise HTTPException(status_code=404, detail="Satellite not found")
    return satellite

@app.delete("/satellites/{satellite_id}")
def delete_satellite(satellite_id: int, db: Session = Depends(get_db)):
    satellite = db.query(Satellite).filter(Satellite.id == satellite_id).first()
    if satellite is None:
        raise HTTPException(status_code=404, detail="Satellite not found")
    db.delete(satellite)
    db.commit()
    return {"message": "Satellite deleted successfully"}