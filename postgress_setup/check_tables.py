'''
file for viewing all current tables in postrgress instance
'''

from sqlalchemy import inspect
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv( 'POSTGRESQL_URL' ))

inspector = inspect(engine)

# gets all existing tagbles and prints out
existing_tables = inspector.get_table_names()

print(f'Tables in database: {existing_tables}')
