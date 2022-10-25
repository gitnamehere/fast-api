import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')

settings = Settings() #DEFINED SETTINGS CLASS WITH DB_URL ATTRIBUTE. CREATE INSTANCE OF SETTINGS VARIABLE == DB_URL AUTOMATICALLY LOADED.
