'''
main.py for application (sets up and runs fastapi app)
'''


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import user_routes, chat_routes
from dotenv import load_dotenv
import os

load_dotenv()

# Create FastAPI instance
app = FastAPI()

# Needed for connecting to frontend and not blocking requests fron frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv('FRONTEND_APP_URL')],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# adding user routes to application
app.include_router(user_routes.router, prefix='/users')
app.include_router(chat_routes.router, prefix='/chat')