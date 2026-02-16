from fastapi import APIRouter, UploadFile, File, Form
from .models import LoginSchema, UserSchema, SignupSchema, UpdateYearGroupSchema, DeleteUserWorkingFileSchema, UpdateClassContextSchema
from ..user.user_account import create_user, login_user, delete_user_account, get_user_data, update_user_year_group, update_user_class_context, get_username_from_jwt_token
from ..data_storage.s3_functionality import upload_user_working_file, delete_user_working_file, get_user_working_files

router = APIRouter()

@router.post('/login')
async def login(data: LoginSchema):
    '''
    Route for users logging into their accounts
    '''

    # Extract username and password from the request body
    username = data.username
    password = data.password

    response = await login_user(username, password)
    status = response['status']
    message = response['message']
    jwt_token = response['jwt_token']

    return {'message': message, 'status': status, 'jwt_token' : jwt_token}


@router.post('/signup')
async def signup(data: SignupSchema):
    '''
    route for users creating new accounts
    '''

    # Extract username and password from the request body
    username = data.username
    password = data.password

    response = await create_user(username, password)
    status = response['status']
    message = response['message']

    return {'message': message, 'status': status}
    

@router.post('/delete_account')
async def delete_account(data: UserSchema):
    '''
    route for users deleting their accounts
    '''

    # Extract username and password from the request body
    jwt_token = data.jwt_token

    response = await delete_user_account(jwt_token)
    status = response['status']
    message = response['message']

    return {'message': message, 'status': status}


@router.post('/get_user_info')
async def get_user_info(data: UserSchema):
    '''
    route for getting user info from jwt token
    '''

    jwt_token = data.jwt_token

    response = await get_user_data(jwt_token)
    status = response['status']
    message = response['message']
    user_data = response['user_data']

    return {'status': status, 'message': message, 'user_data': user_data}


@router.post('/update_year_group')
async def update_year_group(data: UpdateYearGroupSchema):
    '''
    route for updating user's year group
    '''

    jwt_token = data.jwt_token
    year_group = data.year_group

    response = await update_user_year_group(jwt_token, year_group)
    status = response['status']
    message = response['message']

    return {'status': status, 'message': message}


@router.post('/update_class_context')
async def update_class_context(data: UpdateClassContextSchema):
    '''
    route for updating user's class context
    '''

    jwt_token = data.jwt_token
    class_context = data.class_context

    response = await update_user_class_context(jwt_token, class_context)
    status = response['status']
    message = response['message']

    return {'status': status, 'message': message}



from fastapi import APIRouter, UploadFile, File, Form

@router.post('/upload_working_file')
async def upload_working_file( jwt_token: str = Form(...), file: UploadFile = File(...)):
    file_content = await file.read()
    filename = file.filename

    username = await get_username_from_jwt_token(jwt_token)
    
    if username:
        status, message = await upload_user_working_file(username, filename, file_content)

    else:
        status = 400
        message = 'Invalid user JWT token'

    return {'status': status, 'message': message}


@router.post('/delete_working_file')
async def upload_working_file( data: DeleteUserWorkingFileSchema ):
    
    filename = data.filename
    jwt_token = data.jwt_token

    username = await get_username_from_jwt_token(jwt_token)
    
    if username:
        status, message = await delete_user_working_file(username, filename)

    else:
        status = 400
        message = 'Invalid user JWT token'

    return {'status': status, 'message': message}


@router.post('/get_working_files')
async def get_working_files(data: UserSchema):
    jwt_token = data.jwt_token

    username = await get_username_from_jwt_token(jwt_token)
    
    if username:
        status, message, working_files = await get_user_working_files(username)

    else:
        status = 400
        message = 'Invalid user JWT token'
        working_files = []

    return {'status': status, 'message': message, 'working_files': working_files}

