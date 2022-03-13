import databases
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.config import settings


engine = create_engine(settings.DATABASE_URL)
database = databases.Database(settings.DATABASE_URL)
metadata = sqlalchemy.MetaData()