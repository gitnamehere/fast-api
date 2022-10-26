#This file is used to reference the database and create a session

import sqlalchemy as SQL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings as Settings

#Change (USER) to your username, (PASSWORD) to password, (HOST) to host, and (DATABASE NAME) to your database name 
#If you are using Docker, change (HOST) to the Database container name, such as "database" as specified in the docker-compose.yml file.
#DATABASE_URL = "postgresql://(USER):(PASSWORD)@(HOST):5432/(DB NAME)"

#If using config.py, use the environment variable DATABASE_URL

DATABASE_URL = Settings.database_url

engine = SQL.create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#Access the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()