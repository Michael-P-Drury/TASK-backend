import os
import asyncio
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Integer, select
from sqlalchemy.orm import declarative_base, Session

# 1. Setup Environment and Connection
load_dotenv()
DATABASE_URL = os.getenv('POSTGRESQL_URL')

if not DATABASE_URL:
    print("ERROR: POSTGRESQL_URL not found in .env file.")
    exit()

engine = create_engine(DATABASE_URL)
Base = declarative_base()

# 2. Define Model locally to avoid import errors
class ReferenceOutputs(Base):
    __tablename__ = 'reference_outputs'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    tool_id = Column(String, nullable=False)
    content = Column(String, nullable=False)
    filename = Column(String, nullable=False)

def check_references(target_username=None):
    print("\n" + "="*80)
    print(f"DATABASE INSPECTOR: reference_outputs table")
    print("="*80)

    try:
        with Session(engine) as session:
            query = session.query(ReferenceOutputs)
            
            if target_username:
                query = query.filter(ReferenceOutputs.username == target_username)
                print(f"Filtering for user: {target_username}")
            else:
                print("Showing all entries in table...")

            results = query.all()

            if not results:
                print("\n[!] No references found.")
                return

            # Formatting headers
            header = f"{'ID':<4} | {'Username':<12} | {'Tool ID':<25} | {'Filename':<30} | {'Content Preview'}"
            print("\n" + header)
            print("-" * len(header))

            for row in results:
                # Clean up content preview (remove newlines and truncate)
                clean_content = row.content.replace('\n', ' ')[:40]
                print(f"{row.id:<4} | {row.username:<12} | {row.tool_id:<25} | {row.filename:<30} | {clean_content}...")
            
            print("="*80 + "\n")

    except Exception as e:
        print(f"DATABASE ERROR: {e}")

if __name__ == "__main__":
    # If you want to filter for a specific user, put their name here
    # Otherwise, leave it as None to see everything
    user_to_check = None 
    
    check_references(user_to_check)