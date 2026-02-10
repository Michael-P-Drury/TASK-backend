from fastapi import APIRouter
from .models import ChatSchema
from ..user_account.user_auth import get_username_from_jwt_token



router = APIRouter()

@router.post('/send_chat')
async def login(data: ChatSchema):
    jwt_token = data.jwt_token

    username = await get_username_from_jwt_token(jwt_token)
    
    if username:
        # decide on if you have enough info... if you do ... if you dont ...
        status = 200
        message = 'hello'
        response = 'response'

    else:
        status = 400
        message = 'Invalid user JWT token'
        response = ''

    return {'status': status, 'message': message, 'response': response}
