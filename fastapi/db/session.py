# db/session.py
from fastapi.db.database import SessionLocal  

def get_db():
    """
     Generator that provides a database session,
     and automatically closes it after use.

     Yields:
     db (Session): Database session.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        # Optional error handling: log the error
        print(f"Error during database session: {e}")
        raise
    finally:
        db.close()