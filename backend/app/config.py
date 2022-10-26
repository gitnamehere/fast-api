import os

from pydantic import BaseSettings

#Create a .env file in the project directory of the project (./backend/app)
#Add the following lines to the .env file:

#DATABASE_URL='your database url' (Ex: postgresql://postgres:password@database:5432/postgres)
#SECRET_KEY='your_secret_key' (Hint: in bash, run the command: openssl rand -hex 32)

class Settings(BaseSettings):
    #Example environment variables
    database_url: str = 'postgresql://postgres:password@database:5432/fastapi_db'
    secret_key: str = "SECRET_KEY"

    class Config:
        env_file = ".env"

settings = Settings() #DEFINED SETTINGS CLASS WITH DB_URL ATTRIBUTE. CREATE INSTANCE OF SETTINGS VARIABLE == DB_URL AUTOMATICALLY LOADED.
