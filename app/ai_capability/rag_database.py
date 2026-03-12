from sqlmodel import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector

load_dotenv()

# connection to PostgreSQL database to be imported when used
DATABASE_URL = os.getenv('POSTGRESQL_URL')
postgres_engine = create_engine(DATABASE_URL)

Base = declarative_base()

# rag database structure to be used for SQLAlchemy for rag capability
class SupportFiles(Base):
    __tablename__ = 'support_files'
    id = Column(Integer, primary_key = True)
    username = Column(String, unique = True, nullable = False)
    filename = Column(String, nullable = True)
    content = Column(String, nullable = True)
    embedding = Column(Vector(768))