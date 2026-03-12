from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, String, Integer, text
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector

load_dotenv()

Base = declarative_base()

engine = create_engine(os.getenv( 'POSTGRESQL_URL' ))

with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    conn.commit()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    username = Column(String, unique = True, nullable = False)
    password = Column(String, nullable = False)
    year_group = Column(Integer, nullable = True)
    class_context = Column(String, nullable = True)
    condensed_chat_history = Column(String, nullable = True)
    full_chat_history = Column(String, nullable = True)



class SupportFiles(Base):
    __tablename__ = 'support_files'
    id = Column(Integer, primary_key = True)
    username = Column(String, unique = True, nullable = False)
    filename = Column(String, nullable = True)
    content = Column(String, nullable = True)
    embedding = Column(Vector(768))



class ReferenceOutputs(Base):
    __tablename__ = 'reference_outputs'
    id = Column(Integer, primary_key = True)
    username = Column(String, nullable = False)
    tool_id = Column(String, nullable = False)
    content = Column(String, nullable = False)
    filename = Column(String, nullable = False)


Base.metadata.create_all(engine)
