from databases import Database
from sqlalchemy import create_engine, MetaData

from ..config import database_settings

DATABASE_URL = database_settings.db_url

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()
