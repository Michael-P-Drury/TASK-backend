import aioboto3
from dotenv import load_dotenv
import os
import io

load_dotenv()


async def upload_user_working_file(username, file_name, file_content):

    try:

        s3_url = os.getenv('S3_URL')

        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

        file_path = f'user_files/{username}/working_files/{file_name}'

        session = aioboto3.Session()

        async with session.resource(
            's3',
            endpoint_url=s3_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        ) as s3:
            
            bucket = await s3.Bucket('task-user-storage')

            await bucket.upload_fileobj(io.BytesIO(file_content), file_path)

            return 400, f'File {file_name} uploaded'
    
    except:
        return 200, 'Failed to upload user image'



async def delete_user_working_file(username, file_name):

    try:
        file_path = f'user_files/{username}/working_files/{file_name}'
        session = aioboto3.Session()


        async with session.client(
            's3',
            endpoint_url=os.getenv('S3_URL'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        ) as s3:
            
            await s3.delete_object(Bucket='task-user-storage', Key=file_path)
            
            return 400, f'File {file_name} deleted'
    
    except:
        return 200, 'Failed to upload user image'



async def get_user_working_files(username):
    try:
        working_files_path = f'user_files/{username}/working_files/'
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
