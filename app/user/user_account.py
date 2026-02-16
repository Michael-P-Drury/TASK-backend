import bcrypt
from sqlalchemy.orm import Session
from .user_database import engine, User
import jwt
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
                return {'status': 400, 'message': 'User does not exist', 'jwt_token': None}
            
            password_bytes = password.encode('utf-8')

            check_password_bytes = user.password.encode('utf-8')

            matched_password = bcrypt.checkpw(password_bytes, check_password_bytes)

            if matched_password:
                jwt_access_token = create_jwt_access_token(data={'sub': username})
                return {'status': 200, 'message': 'User logged in successfully', 'jwt_token': jwt_access_token}
            
            return {'status': 400, 'message': 'Invalid password', 'jwt_token': None}
    
    except:
        return {'status': 400, 'message': 'Error logging in user', 'jwt_token': None}
        


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
                return {'status': 400, 'message': 'Username already exists'}

            try:
                session.add(new_user)
                session.commit()
                return {'status': 200, 'message': 'User created successfully'}
            
            except:
                return {'status': 400, 'message': 'Error creating user'}
            
    except:
        return {'status': 400, 'message': 'Error creating user'}



async def delete_user_account(jwt_token):
    '''
    deletes user from postgresql database using jwt token for authentication.
    '''

    try:   
        secret_key = os.getenv('JWT_SECRET_KEY')
        algorithm = os.getenv('JWT_ALGORITHM')

        decoded_jwt = jwt.decode(jwt_token, secret_key, algorithms=[algorithm])

        username = decoded_jwt.get('sub')

        if username is None:
            return {'status': 400, 'message': 'Invalid token'}
    

        with Session(engine) as session:
            user = session.query(User).filter(User.username == username).first()

            if user is None:
                return {'status': 400, 'message': 'User does not exist'}

            if user:
                session.delete(user)
                session.commit()
                return {'status': 200, 'message': 'User deleted successfully'}
            
            else:
                return {'status': 400, 'message': 'Error deleting user'}
    
    except:
        return {'status': 400, 'message': 'Error deleting user'}



async def get_user_data(jwt_token):
    '''
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


def create_jwt_access_token(data):
    '''
    creating jwt access token for user auth
    '''
    to_encode = data.copy()

    secret_key = os.getenv('JWT_SECRET_KEY')
    algorithm = os.getenv('JWT_ALGORITHM')
    
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


async def update_user_year_group(jwt_token, year_group):

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
    



async def update_user_class_context(jwt_token, class_context):

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
        


async def get_username_from_jwt_token(jwt_token):
    '''
    deletes user from postgresql database using jwt token for authentication.
    '''

    try:   
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



async def get_user_chat_history(username, full_history):
    '''
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
            
    

async def set_chat_history(username, chat_history, full_history):
    '''
    sets a users chat history
    '''

    with Session(engine) as session:
        user = session.query(User).filter(User.username == username).first()

        if full_history:
            user.full_chat_history = chat_history

        else:
            user.condensed_chat_history = chat_history

        session.commit()


async def clear_user_chat(username):
    '''
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
