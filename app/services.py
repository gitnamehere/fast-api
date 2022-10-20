#This file is used to handle database requests and responses

import database as Database
import models as Models

#Create a table (if it doesn't exist) based on the models.py file

#Band aid fix for the database not being created on startup
Database.Base.metadata.create_all(bind=Database.engine)

#Access the database
def get_db():
    db = Database.SessionLocal()
    try:
        yield db
    finally:
        db.close()