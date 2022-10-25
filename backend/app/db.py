import databases
import ormar
import sqlalchemy

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    email: str = ormar.String(max_length=128, unique=True, nullable=False)
    active: bool = ormar.Boolean(default=True, nullable=False)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)

#CREATES PYDANTIC MODEL AND SQL-ALCHEMY TABLE. 
#ormar USES SQLA FOR DATABASES/TABLES AND DB QUERIES, DB FOR EXECUTING QUERIES ASYNC, AND PYDANTIC FOR DATA VALADATION. 
#ALL PYDANTYIC METHODS ARE AVAILABLE ON A MODEL. DATA MIGRATION VIA ALEMBIC. 
