import bcrypt
from sqlalchemy.orm import Session
from .user_database import engine, User
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

async def login_user(username, password):
    '''
    Logs in users using username and password.

    connects to postgresql instance to check credentials using bcrypt.
    '''

    try:

        with Session(engine) as session:
            user = session.query(User).filter(User.username == username).first()

            if not user:
                return 400, "User does not exist", None
            
            password_bytes = password.encode('utf-8')

            check_password_bytes = user.password.encode('utf-8')

            matched_password = bcrypt.checkpw(password_bytes, check_password_bytes)

            if matched_password:
                jwt_access_token = create_jwt_access_token(data={"sub": username})
                return 200, "User logged in successfully", jwt_access_token
            
            return 400, "Invalid password", None
    
    except:
        return 400, "Error logging in user", None
        


async def create_user(username, password):
    '''
    creates new user in progresql database using username and password.
    '''

    try:

        # using byscript to hash passwords
        s = bcrypt.gensalt()
        password_bytes = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password_bytes, s)

        hashed_password_str = hashed_password.decode('utf-8')

        new_user = User(username=username, password=hashed_password_str)
        
        with Session(engine) as session:

            existing_user = session.query(User).filter(User.username == username).first()

            if existing_user:
                return 400, "Username already exists"

            try:
                session.add(new_user)
                session.commit()
                return 200, "User created successfully" 
            
            except:
                return 400, "User creation failed"
            
    except:
        return 400, "Error creating user"


async def delete_user_account(jwt_token):
    '''
    deletes user from postgresql database using jwt token for authentication.
    '''

    try:   
        secret_key = os.getenv("JWT_SECRET_KEY")
        algorithm = os.getenv("JWT_ALGORITHM")

        decoded_jwt = jwt.decode(jwt_token, secret_key, algorithms=[algorithm])

        username = decoded_jwt.get("sub")

        if username is None:
            return 400, "Invalid token"
    

        with Session(engine) as session:
            user = session.query(User).filter(User.username == username).first()

            if user is None:
                return 400, "User does not exist"

            if user:
                session.delete(user)
                session.commit()
                return 200, "User deleted successfully"
            
            else:
                return 400, "User deletion failed"
    
    except:
        return 400, "Error deleting user"



async def get_user_data(jwt_token):
    '''
    getting user info from jwt token
    '''

    try:

        secret_key = os.getenv("JWT_SECRET_KEY")
        algorithm = os.getenv("JWT_ALGORITHM")

        decoded_jwt = jwt.decode(jwt_token, secret_key, algorithms=[algorithm])

        username = decoded_jwt.get("sub")

        if username is None:
            return 400, "Invalid token", None
        
        with Session(engine) as session:
            user = session.query(User).filter(User.username == username).first()

            if user is None:
                return 400, "User does not exist", None

            if user:
                
                user_data = {"username": user.username, "year_group": user.year_group}

                return 200, "User info retrieved successfully", user_data
            
            else:
                return 400, "User info retrieval failed", None
    
    except:

        return 400, "Error retrieving user info", None


def create_jwt_access_token(data):
    '''
    creating jwt access token for user auth
    '''
    to_encode = data.copy()

    secret_key = os.getenv("JWT_SECRET_KEY")
    algorithm = os.getenv("JWT_ALGORITHM")
    
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


async def update_user_year_group(jwt_token, year_group):

    try:
        secret_key = os.getenv("JWT_SECRET_KEY")
        algorithm = os.getenv("JWT_ALGORITHM")

        decoded_jwt = jwt.decode(jwt_token, secret_key, algorithms=[algorithm])

        username = decoded_jwt.get("sub")

        if username is None:
            return 400, "Invalid token"
        
        with Session(engine) as session:
            user = session.query(User).filter(User.username == username).first()
            if user is None:
                return 400, "User does not exist"
            user.year_group = year_group
            session.commit()
            return 200, "Year group updated successfully"
    
    except:
        return 400, "Error updating year group"
        