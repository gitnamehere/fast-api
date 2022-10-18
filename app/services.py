import database as Database
import models as Models

def create_table():
    return Database.Base.metadata.create_all(bind=Database.engine)

def get_db():
    db = Database.SessionLocal()
    try:
        yield db
    finally:
        db.close()