#Example models.py
#TODO: add passwords/password hashing via OAuth2

import datetime as DateTime
import sqlalchemy as SQL

from database import Base

class User(Base):
    __tablename__ = "users"
    id = SQL.Column(SQL.Integer, primary_key=True, index=True)
    username = SQL.Column(SQL.String, unique=True, index=True)
    email = SQL.Column(SQL.String, unique=True, index=True)
    date_created = SQL.Column(SQL.DateTime, default=DateTime.datetime.utcnow)
