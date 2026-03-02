'''
holds functionality for s3 file storage
'''

import aioboto3
from dotenv import load_dotenv
import os
import io
from botocore.config import Config

load_dotenv()

async def upload_user_output_file(username: str, file_name: str, file_content):
    '''
    inputs:
    username: str - users username
    file_name: str - filename for output file
    file_content - file content to be saved (can be different formats)
    '''
    
    try:

        s3_url = os.getenv('S3_URL')

        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

        file_path = f'user_files/{username}/output_files/{file_name}'

        session = aioboto3.Session()

        async with session.resource(
            's3',
            endpoint_url=s3_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        ) as s3:
            
            bucket = await s3.Bucket('task-user-storage')

            await bucket.upload_fileobj(io.BytesIO(file_content), file_path)

            print(f'file uploaded: {file_path}')

            return 200, f'File {file_name} uploaded'
    
    except Exception as e:
        print(e)
        return 400, 'Failed to upload user image'


async def download_user_output_file(username: str, file_name: str):
    '''
    inputs:
    username: str - users username
    file_name: str - file name to be downloaded

    for downloading a users file
    '''

    try:

        # get env variables
        s3_url = os.getenv('S3_URL')
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

        # creates entire file path for file to be downloaded
        file_path = f'user_files/{username}/output_files/{file_name}'

        session = aioboto3.Session()

        # crates async session with the s3 bucket, and reads the body for the file to download, returning the content
        async with session.client(
            's3',
            endpoint_url=s3_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        ) as s3:

            response = await s3.get_object(Bucket='task-user-storage', Key=file_path)
            
            file_content = await response['Body'].read()

            return 200, f'File {file_name} downloaded', file_content
    
    except Exception as e:
        return 400, 'Failed to upload user image', None
    


async def upload_user_working_file(username: str, file_name: str, file_content):
    '''
    inputs:
    username: str - users username
    file_name: str - filename for output file
    file_content - file content to be saved (can be different formats)
    '''

    try:

        #l oads env variables
        s3_url = os.getenv('S3_URL')
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

        file_path = f'user_files/{username}/working_files/{file_name}'

        session = aioboto3.Session()
        # creates async sioboto3 session witrh s3 bucket and uploads new file
        async with session.resource(
            's3',
            endpoint_url=s3_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        ) as s3:
            
            bucket = await s3.Bucket('task-user-storage')

            await bucket.upload_fileobj(io.BytesIO(file_content), file_path)

            return 200, f'File {file_name} uploaded'
    
    except:
        return 400, 'Failed to upload user image'



async def delete_user_working_file(username: str, file_name: str):
    '''
    inputs:
    username: str - users username
    file_name: str - file name to be deleted
    '''

    try:
        # creates entire path for file to be deleted
        file_path = f'user_files/{username}/working_files/{file_name}'

        # creates async session and then deletes the file
        session = aioboto3.Session()
        async with session.client(
            's3',
            endpoint_url=os.getenv('S3_URL'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        ) as s3:
            
            await s3.delete_object(Bucket='task-user-storage', Key=file_path)
            
            return 200, f'File {file_name} deleted'
    
    except:
        return 400, 'Failed to upload user image'
    

async def delete_user_output_file(username: str, file_name: str):
    '''
    inputs:
    username: str - users username
    file_name: str - file name to be deleted
    '''

    try:
        # creates file path for file
        file_path = f'user_files/{username}/output_files/{file_name}'

        # creates async sessiobn with s3 bucket and deletes file
        session = aioboto3.Session()
        async with session.client(
            's3',
            endpoint_url=os.getenv('S3_URL'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        ) as s3:
            
            await s3.delete_object(Bucket='task-user-storage', Key=file_path)
            
            return 200, f'File {file_name} deleted'
    
    except:
        return 400, 'Failed to upload user image'


async def get_user_working_files(username: str):
    '''
    inputs:
    username: str - users username

    gets the users working files
    '''
    try:
        # creates path for user's working files
        working_files_path = f'user_files/{username}/working_files/'

        # creates async session with s3 bucket and returns list of users working files
        session = aioboto3.Session()
        async with session.client(
            's3',
            endpoint_url=os.getenv('S3_URL'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        ) as s3:
            full_files_list = await s3.list_objects_v2(Bucket='task-user-storage', Prefix=working_files_path)

            return_files = []

            for file in full_files_list['Contents']:
                filename = file['Key'].replace(working_files_path, '')
                return_files.append(filename)

            return 200, 'User files gained successfully', return_files

    except:
        return 400, 'Error getting user files', []



async def get_user_output_files(username: str):
    '''
    inputs:
    username: str - users username
    '''
    try:
        # gets path for user's output files
        working_files_path = f'user_files/{username}/output_files/'

        # create async session with s3 client and returns list of user's output files
        session = aioboto3.Session()
        async with session.client(
            's3',
            endpoint_url=os.getenv('S3_URL'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        ) as s3:

            full_files_list = await s3.list_objects_v2(Bucket='task-user-storage', Prefix=working_files_path)

            return_files = []

            for file in full_files_list['Contents']:
                filename = file['Key'].replace(working_files_path, '')
                return_files.append(filename)

            return 200, 'User files gained successfully', return_files

    except:
        return 400, 'Error getting user files', []



async def delete_user_s3_data(username: str):
    '''
    deletes all objects for user from s3
    '''

    folder_path = f'user_files/{username}/'
    
    try:
        session = aioboto3.Session()
        async with session.client(
            's3',
            endpoint_url=os.getenv('S3_URL'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        ) as s3:
            
            full_files_list = await s3.list_objects_v2(Bucket='task-user-storage', Prefix=folder_path)

            files_list = full_files_list.get('Contents', [])

            for file_path in files_list:
                await s3.delete_object(Bucket='task-user-storage', Key=file_path['Key'])

            return 200, f'user files deleted successfully'

    except Exception as e:
        return 400, f'Error deleting user files'

