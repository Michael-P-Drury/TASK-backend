## TASK-backend

T - Teaching
A - Assistant
S - Side
K - Kick

# to setup

create and enter venv

install dependancies using command:

pip install -r requirements.txt

run postgreSQL server with vector storage or have postgreSQL server

create .env file seen below

run pandoc install.py in testing code to install needed pypandoc executable

run postgress_create_tables.py in postgress_setup to create postgress tables

# to run

enter venv

uvicorn app.main:app

to run with reload:

uvicorn app.main:app --reload

# .env file

FRONTEND_APP_URL="http://localhost:3000"

POSTGRESQL_URL=""

JWT_ALGORITHM="HS256"

JWT_SECRET_KEY=""

S3_URL = ""

AWS_ACCESS_KEY_ID = ""

AWS_SECRET_ACCESS_KEY = ""

CEREBRAS_API_KEY = ""

OPENROUTER_API_KEY = ""
