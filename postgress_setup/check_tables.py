from sqlalchemy import inspect
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv( "POSTGRESQL_URL" ))

# Create an inspector object
inspector = inspect(engine)

# Get list of table names
existing_tables = inspector.get_table_names()

print(f"Tables in database: {existing_tables}")
