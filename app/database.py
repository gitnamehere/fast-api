#This file is used to reference the database and create a session

import sqlalchemy as SQL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Change (USER) to your username, (PASSWORD) to password, and (DATABASE NAME) to your database name 
DATABASE_URL = "postgresql://(USER):(PASSWORD)@localhost:5432/(DATABASE NAME)"

engine = SQL.create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
