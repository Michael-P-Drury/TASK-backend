from fastapi import APIRouter
from .models import LoginSchema, UserSchema, SignupSchema, UpdateYearGroupSchema
from ..user_account.user_auth import create_user, login_user, delete_user_account, get_user_data, update_user_year_group

router = APIRouter()

@router.get("/account")
async def read_users():
    pass


@router.post("/login")
async def login(data: LoginSchema):
    '''
    Route for users logging into their accounts
    '''

    # Extract username and password from the request body
    username = data.username
    password = data.password

    status, message, jwt_token = await login_user(username, password)

    return {"message": message, "status": status, "jwt_token" : jwt_token}


@router.post("/signup")
async def signup(data: SignupSchema):
    '''
    route for users creating new accounts
    '''

    # Extract username and password from the request body
    username = data.username
    password = data.password

    status, message = await create_user(username, password)

    return {"message": message, "status": status}
    

@router.post("/delete_account")
async def delete_account(data: UserSchema):
    '''
    route for users deleting their accounts
    '''

    # Extract username and password from the request body
    jwt_token = data.jwt_token

    status, message = await delete_user_account(jwt_token)

    return {"message": message, "status": status}


@router.post("/get_user_info")
async def get_user_info(data: UserSchema):
    '''
    route for getting user info from jwt token
    '''

    jwt_token = data.jwt_token

    status, message, user_data = await get_user_data(jwt_token)

    return {"status": status, "message": message, "user_data": user_data}


@router.post("/update_year_group")
async def update_year_group(data: UpdateYearGroupSchema):
    '''
    route for updating user's year group
    '''

    jwt_token = data.jwt_token
    year_group = data.year_group

    status, message = await update_user_year_group(jwt_token, year_group)

    return {"status": status, "message": message}