'''
routes for chat
'''

from fastapi import APIRouter
from .models import ChatSchema, UserSchema
from ..user.user_account import get_username_from_jwt_token, clear_user_chat, get_user_chat_history
from ..controller_agent import run_controller_agent

router = APIRouter()

@router.post('/send_chat')
async def send_chat(data: ChatSchema):
    '''
    route for sending a chat from frontend, running controller agent.
    '''
    
    user_prompt = data.user_prompt
    jwt_token = data.jwt_token

    username = await get_username_from_jwt_token(jwt_token)
    
    if username:
        response = await run_controller_agent(username, user_prompt)
        status = response['status']
        message = response['message']

    else:
        status = 400
        message = 'Invalid user JWT token'

    return {'status': status, 'message': message}


@router.post('/get_condensed_chat_history')
async def get_chat_history(data: UserSchema):
    '''
    returns condensed chat history to user
    '''
    
    jwt_token = data.jwt_token

    username = await get_username_from_jwt_token(jwt_token)
    
    if username:
        response = await get_user_chat_history(username, False)
        status = response['status']
        message = response['message']
        chat_history = response['chat_history']

    else:
        status = 400
        message = 'Invalid user JWT token'
        chat_history = None

    return {'status': status, 'message': message, 'chat_history': chat_history}


@router.post('/get_full_chat_history')
async def get_chat_history(data: UserSchema):
    '''
    returns full chat history to frontend
    '''
    
    jwt_token = data.jwt_token

    username = await get_username_from_jwt_token(jwt_token)
    
    if username:
        response = await get_user_chat_history(username, True)
        status = response['status']
        message = response['message']
        chat_history = response['chat_history']

    else:
        status = 400
        message = 'Invalid user JWT token'
        chat_history = None

    return {'status': status, 'message': message, 'chat_history': chat_history}


@router.post('/clear_chat')
async def clear_chat(data: UserSchema):
    '''
    route to remove chat history for user
    '''
    
    jwt_token = data.jwt_token

    username = await get_username_from_jwt_token(jwt_token)
    
    if username:
        response = await clear_user_chat(username)
        status = response['status']
        message = response['message']

    else:
        status = 400
        message = 'Invalid user JWT token'

    return {'status': status, 'message': message}
