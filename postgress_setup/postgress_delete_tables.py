from typing import Optional
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base

load_dotenv() 

Base = declarative_base()

engine = create_engine(os.getenv( 'POSTGRESQL_URL' ))

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    year_group = Column(Integer, nullable=True)
    class_context = Column(String, nullable=True)
    chat_history = Column(String, nullable=True)


Base.metadata.drop_all(engine)