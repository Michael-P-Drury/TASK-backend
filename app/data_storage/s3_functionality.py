'''
holds functionality for s3 file storage
'''

import aioboto3
from dotenv import load_dotenv
import os
import io
from ..ai_capability.rag import postgress_store_support_file, postgress_delete_support_file#

load_dotenv()

async def upload_user_output_file(username: str, filename: str, file_content):
    '''
    inputs:
    username: str - users username
    filename: str - filename for output file
    file_content - file content to be saved (can be different formats)
    '''
    
    try:

        s3_url = os.getenv('S3_URL')

        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

        file_path = f'user_files/{username}/output_files/{filename}'

        session = aioboto3.Session()

        async with session.resource(
            's3',
            endpoint_url=s3_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        ) as s3:
            
            bucket = await s3.Bucket('task-user-storage')

            await bucket.upload_fileobj(io.BytesIO(file_content), file_path)

            return 200, f'File {filename} uploaded'
    
    except Exception as e:
        print(e)
        return 400, 'Failed to upload user image'


async def download_user_output_file(username: str, filename: str):
    '''
    inputs:
    username: str - users username
    filename: str - file name to be downloaded

    for downloading a users file
    '''

    try:

        # get env variables
        s3_url = os.getenv('S3_URL')
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

        # creates entire file path for file to be downloaded
        file_path = f'user_files/{username}/output_files/{filename}'

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

            return 200, f'File {filename} downloaded', file_content
    
    except Exception as e:
        return 400, 'Failed to upload user image', None



async def upload_user_support_file(username: str, filename: str, file_content):
    '''
    inputs:
    username: str - users username
    filename: str - filename for output file
    file_content - file content to be saved (can be different formats)
    '''

    try:

        #l oads env variables
        s3_url = os.getenv('S3_URL')
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

        file_path = f'user_files/{username}/support_files/{filename}'

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

            await postgress_store_support_file(username, filename, file_content)

            return 200, f'File {filename} uploaded'
    
    except:
        return 400, 'Failed to upload user image'



async def delete_user_support_file(username: str, filename: str):
    '''
    inputs:
    username: str - users username
    filename: str - file name to be deleted
    '''

    try:
        # creates entire path for file to be deleted
        file_path = f'user_files/{username}/support_files/{filename}'

        # creates async session and then deletes the file
        session = aioboto3.Session()
        async with session.client(
            's3',
            endpoint_url=os.getenv('S3_URL'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        ) as s3:
            
            await s3.delete_object(Bucket='task-user-storage', Key=file_path)

            await postgress_delete_support_file(username, filename)
            
            return 200, f'File {filename} deleted'
    
    except:
        return 400, 'Failed to upload user image'
    

async def delete_user_output_file_S3(username: str, filename: str):
    '''
    inputs:
    username: str - users username
    filename: str - file name to be deleted
    '''

    try:
        # creates file path for file
        file_path = f'user_files/{username}/output_files/{filename}'

        # creates async sessiobn with s3 bucket and deletes file
        session = aioboto3.Session()
        async with session.client(
            's3',
            endpoint_url=os.getenv('S3_URL'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        ) as s3:
            
            await s3.delete_object(Bucket='task-user-storage', Key=file_path)
            
            return 200, f'File {filename} deleted'
    
    except:
        return 400, 'Failed to upload user image'


async def get_user_support_files(username: str):
    '''
    inputs:
    username: str - users username

    gets the users support files
    '''
    try:
        # creates path for user's support files
        support_files_path = f'user_files/{username}/support_files/'

        # creates async session with s3 bucket and returns list of users support files
        session = aioboto3.Session()
        async with session.client(
            's3',
            endpoint_url=os.getenv('S3_URL'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        ) as s3:
            full_files_list = await s3.list_objects_v2(Bucket='task-user-storage', Prefix=support_files_path)

            return_files = []

            for file in full_files_list.get('Contents', []):

                filename = file['Key'].replace(support_files_path, '')
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
        support_files_path = f'user_files/{username}/output_files/'

        # create async session with s3 client and returns list of user's output files
        session = aioboto3.Session()
        async with session.client(
            's3',
            endpoint_url=os.getenv('S3_URL'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        ) as s3:

            full_files_list = await s3.list_objects_v2(Bucket='task-user-storage', Prefix=support_files_path)

            return_files = []

            for file in full_files_list.get('Contents', []):
                filename = file['Key'].replace(support_files_path, '')
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

