'''
Holds user account functionality
'''

import bcrypt
from sqlalchemy.orm import Session
from .user_database import engine, User
import jwt
from dotenv import load_dotenv
import os
from ..data_storage.s3_functionality import delete_user_s3_data

load_dotenv()

async def login_user(username: str, password: str):
    '''
    inputs:
    username: str - login attempt username
    password: str - login attempt password

    Logs in users using username and password.

    connects to postgresql instance to check credentials using bcrypt.
    '''

    try:
        # make a session with sqlalchemy
        with Session(engine) as session:
            user = session.query(User).filter(User.username == username).first()

            if not user:
                return {'status': 400, 'message': 'User does not exist', 'jwt_token': None}
                
            # as passwords are encrypted, checks password bytes using bycrypt
            password_bytes = password.encode('utf-8')

            check_password_bytes = user.password.encode('utf-8')

            matched_password = bcrypt.checkpw(password_bytes, check_password_bytes)

            if matched_password:
                jwt_access_token = create_jwt_access_token(data={'sub': username})
                return {'status': 200, 'message': 'User logged in successfully', 'jwt_token': jwt_access_token}
            
            return {'status': 400, 'message': 'Invalid password', 'jwt_token': None}
    
    except:
        return {'status': 400, 'message': 'Error logging in user', 'jwt_token': None}
        


async def create_user(username: str, password: str):
    '''
    inputs:
    username: str - create user username
    password: str - create user password

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
            
            # checks to see if user already exists
            existing_user = session.query(User).filter(User.username == username).first()

            if existing_user:
                return {'status': 400, 'message': 'Username already exists'}

            try:
                session.add(new_user)
                session.commit()
                return {'status': 200, 'message': 'User created successfully'}
            
            except:
                return {'status': 400, 'message': 'Error creating user'}
            
    except:
        return {'status': 400, 'message': 'Error creating user'}



async def delete_user_account(jwt_token: str):
    '''
    inputs:
    jwt_token: str - jwtr token for delete user (connected to users username)

    deletes user from postgresql database using jwt token for authentication.
    '''

    try:
        # gets jwt key and algorithm form .env file
        secret_key = os.getenv('JWT_SECRET_KEY')
        algorithm = os.getenv('JWT_ALGORITHM')

        # decodes the inputted jwt token and gets the username
        decoded_jwt = jwt.decode(jwt_token, secret_key, algorithms=[algorithm])

        username = decoded_jwt.get('sub')

        if username is None:
            return {'status': 400, 'message': 'Invalid token'}
    
        # creates sqlalchemy session and deletes account from table
        with Session(engine) as session:
            user = session.query(User).filter(User.username == username).first()

            if user is None:
                return {'status': 400, 'message': 'User does not exist'}

            if user:
                session.delete(user)
                session.commit()
                # also removes user's s3 files
                await delete_user_s3_data(username)

                return {'status': 200, 'message': 'User deleted successfully'}
            
            else:
                return {'status': 400, 'message': 'Error deleting user'}
    
    except:
        return {'status': 400, 'message': 'Error deleting user'}


async def get_class_context_and_year(username: str):
    '''
    inputs:
    username: str - users username
    
    getting user class context and year group from username
    '''

    try:

        if username is None:
            return {'status': 400, 'message': 'Invalid username', 'user_data': None}
        
        with Session(engine) as session:
            user = session.query(User).filter(User.username == username).first()

            if user is None:
                return {'status': 400, 'message': 'User does not exist', 'user_data': None}

            if user:
                
                user_data = {'year_group': user.year_group, 'class_context': user.class_context}

                return {'status': 200, 'message': 'User data retreived successfully', 'user_data': user_data}
            
            else:
                return {'status': 400, 'message': 'User info retreival failed', 'user_data': None}
    
    except:

        return {'status': 400, 'message': 'Error retreiving user info', 'user_data': None}



async def get_user_data(jwt_token: str):
    '''
    inputs:
    jwt_token: str - jwtr token for delete user (connected to users username)

    getting user info from jwt token
    '''

    try:

        secret_key = os.getenv('JWT_SECRET_KEY')
        algorithm = os.getenv('JWT_ALGORITHM')

        decoded_jwt = jwt.decode(jwt_token, secret_key, algorithms=[algorithm])

        username = decoded_jwt.get('sub')

        if username is None:
            return {'status': 400, 'message': 'Invalid jwt token', 'user_data': None}
        
        with Session(engine) as session:
            user = session.query(User).filter(User.username == username).first()

            if user is None:
                return {'status': 400, 'message': 'User does not exist', 'user_data': None}

            if user:
                
                user_data = {'username': user.username, 'year_group': user.year_group, 'class_context': user.class_context}

                return {'status': 200, 'message': 'User data retreived successfully', 'user_data': user_data}
            
            else:
                return {'status': 400, 'message': 'User info retreival failed', 'user_data': None}
    
    except:

        return {'status': 400, 'message': 'Error retreiving user info', 'user_data': None}


def create_jwt_access_token(data: str):
    '''
    inputs:
    data: str - the data that you want to create jwt token for

    creating jwt access token for user auth
    '''
    to_encode = data.copy()

    secret_key = os.getenv('JWT_SECRET_KEY')
    algorithm = os.getenv('JWT_ALGORITHM')
    
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


async def update_user_year_group(jwt_token: str, year_group: int):
    '''
    inputs:
    jwt_token: str - jwt token linked to users username
    year_group: int - new year group
    '''

    try:
        secret_key = os.getenv('JWT_SECRET_KEY')
        algorithm = os.getenv('JWT_ALGORITHM')

        decoded_jwt = jwt.decode(jwt_token, secret_key, algorithms=[algorithm])

        username = decoded_jwt.get('sub')

        if username is None:
            return {'status': 400, 'message': 'Invalid JWT token'}
        
        if not isinstance(year_group, int):
            return {'status': 400, 'message': 'Year group must be Integer (whole number)'}

        if int(year_group) <= 0 or int(year_group) > 6:
            return {'status': 400, 'message': 'Year group must be between 1 and 6'}
        
        with Session(engine) as session:
            user = session.query(User).filter(User.username == username).first()
            if user is None:
                return {'status': 400, 'message': 'User does not exist'}
            
            user.year_group = year_group
            session.commit()
            return {'status': 200, 'message': 'year group updated successfully'}
    
    except:
        return {'status': 400, 'message': 'Error updating year group'}
    



async def update_user_class_context(jwt_token: str, class_context: str):
    '''
    inputs:
    jwt_token: str - jwt token linked to users username
    class_context: int - new class context
    '''

    try:
        secret_key = os.getenv('JWT_SECRET_KEY')
        algorithm = os.getenv('JWT_ALGORITHM')

        decoded_jwt = jwt.decode(jwt_token, secret_key, algorithms=[algorithm])

        username = decoded_jwt.get('sub')

        if username is None:
            return {'status': 400, 'message': 'Error with JWT token'}

        
        with Session(engine) as session:
            user = session.query(User).filter(User.username == username).first()
            if user is None:
                return {'status': 400, 'message': 'User does not exist'}
            user.class_context = class_context
            session.commit()
            return {'status': 200, 'message': 'Class context updated'}
    
    except:
        return {'status': 400, 'message': 'Error updating class context'}
        


async def get_username_from_jwt_token(jwt_token: str):
    '''
    inputs:
    jwt_token: str - jwt token

    deletes user from postgresql database using jwt token for authentication.
    '''

    try:  
        # getting env variables for jwt tokens
        secret_key = os.getenv('JWT_SECRET_KEY')
        algorithm = os.getenv('JWT_ALGORITHM')

        decoded_jwt = jwt.decode(jwt_token, secret_key, algorithms=[algorithm])

        username = decoded_jwt.get('sub')

        if username is None:
            return None
    

        with Session(engine) as session:
            user = session.query(User).filter(User.username == username).first()

            if user is None:
                return None

            if user:
                return user.username
            
            else:
                return None
    
    except:
        return None



async def get_user_chat_history(username: str, full_history: bool):
    '''
    inputs:
    username: str - users username
    full_history: bool - true or false for full history return or not

    returning a users chat history
    '''
    try:
        with Session(engine) as session:
            user = session.query(User).filter(User.username == username).first()
            
            if full_history:
                chat_history = user.full_chat_history

            else:
                chat_history = user.condensed_chat_history

            return {'status': 200, 'message': 'success getting chat history', 'chat_history': chat_history}
    
    except:
        return {'status': 400, 'message': 'Error clearing chat history', 'chat_history': None}
            
    

async def set_chat_history(username: str, chat_history: str, full_history: bool):
    '''
    inputs:
    username: str - users username
    chat_history: str - new chat history
    full_history: bool - bool for if full chat history or not


    sets a users chat history
    '''

    with Session(engine) as session:
        user = session.query(User).filter(User.username == username).first()

        if full_history:
            user.full_chat_history = chat_history

        else:
            user.condensed_chat_history = chat_history

        session.commit()


async def clear_user_chat(username: str):
    '''
    inputs:
    username: str - users username

    sets a users chat history
    '''

    try:

        with Session(engine) as session:
            user = session.query(User).filter(User.username == username).first()

            user.full_chat_history = ''
            user.condensed_chat_history = ''
            session.commit()

            return {'status': 200, 'message': 'Chat History Cleared'}
        
    except:
        return {'status': 400, 'message': 'Error clearing History Cleared'}
