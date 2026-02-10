
'''
Centralized database connection for connecting to PorstgreSQL

Contains models for PostGreSQL so that it is centralised
'''

from sqlmodel import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base

load_dotenv()
    
# connection to PostgreSQL database to be imported when used
DATABASE_URL = os.getenv('POSTGRESQL_URL')
engine = create_engine(DATABASE_URL)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    year_group = Column(Integer, nullable=True)
    class_context = Column(String, nullable=True)
    chat_history = Column(String, nullable=True)

