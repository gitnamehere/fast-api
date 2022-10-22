#This file is used to create a model of the User table in the database
#TODO: add passwords/password hashing via OAuth2

import datetime as DateTime
import sqlalchemy as SQL

from sqlalchemy.orm import relationship

from database import Base

#Create a user class
class User(Base):
    __tablename__ = "users"
    id = SQL.Column(SQL.Integer, primary_key=True, index=True)
    username = SQL.Column(SQL.String, unique=True, index=True)
    hashed_password = SQL.Column(SQL.String)
    email = SQL.Column(SQL.String, unique=True, index=True)
    date_created = SQL.Column(SQL.DateTime, default=DateTime.datetime.utcnow)

    messages = relationship("Message", back_populates="owner")

class Message(Base):
    __tablename__ = "messages"
    id = SQL.Column(SQL.Integer, primary_key=True, index=True)
    text = SQL.Column(SQL.String, index=True)
    date_created = SQL.Column(SQL.DateTime, default=DateTime.datetime.utcnow)
    user_id = SQL.Column(SQL.Integer, SQL.ForeignKey("users.id"))

    owner = relationship("User", back_populates="messages")

