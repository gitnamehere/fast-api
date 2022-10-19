#This file is used to create a model of the User table in the database
#TODO: add passwords/password hashing via OAuth2

import datetime as DateTime
import sqlalchemy as SQL

from database import Base

#Create a user class
class User(Base):
    __tablename__ = "users"
    id = SQL.Column(SQL.Integer, primary_key=True, index=True)
    username = SQL.Column(SQL.String, unique=True, index=True)
    email = SQL.Column(SQL.String, unique=True, index=True)
    date_created = SQL.Column(SQL.DateTime, default=DateTime.datetime.utcnow)
