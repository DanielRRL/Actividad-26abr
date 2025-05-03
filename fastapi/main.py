from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.main_router import main_router
from fastapi.db.database import engine, Base
import logging

# Initialize the app
app = FastAPI(
    title="Microservices API",
    description="API for managing planets and satellites in a microservices architecture.",
    version="1.0.0",
    docs_url="/documentation",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Include the main router
app.include_router(main_router)

# Events
@app.on_event("startup")
async def startup_event():
    try:
        logger.info("Application is starting...")
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application is shutting down...")

# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    try:
        # Verifica la conexión a la base de datos
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return {"status": "ok", "database": "connected"}
    except Exception:
        return {"status": "error", "database": "disconnected"}


# lol