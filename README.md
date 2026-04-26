## TASK-backend

T - Teacher
A - Assistant
S - Side
K - Kick

# to run

install dependancies using command:

pip install -r requirements.txt

run postgreSQL server or have postgreSQL server to connect to for user account storage

To run command:

uvicorn app.main:app

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
