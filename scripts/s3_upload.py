import os
import boto3
from dotenv import load_dotenv
import requests

URL_WITH_REGION_CODE = "https://s3.us-west-1.amazonaws.com"

load_dotenv()

BUCKET_NAME = os.environ["BUCKET_NAME"]
ACCESS_KEY = os.environ["ACCESS_KEY"]
SECRET_ACCESS_KEY = os.environ["SECRET_ACCESS_KEY"]



# s3 = boto3.resource('s3')
# bucket = s3.Bucket(BUCKET_NAME)
# s3_client = boto3.client('s3')
# with open("chow.jpg", "rb") as data:
#     print(s3_client.upload_fileobj(data, BUCKET_NAME, "chow.jpg"))

# s3 = boto3.resource('s3')
# bucket = s3.Bucket(os.environ["BUCKET_NAME"])


s3_client = boto3.client('s3', aws_access_key_id = ACCESS_KEY, aws_secret_access_key = SECRET_ACCESS_KEY)


def save_file(file_path, filename):


    with open(file_path, "rb") as data:
        s3_client.upload_fileobj(data, BUCKET_NAME, filename)

    return filename



def get_file_info_from_aws(filename):
    response = s3_client.generate_presigned_url('get_object',
                                             Params={'Bucket': BUCKET_NAME,
                                                     'Key': filename})
    return response


filename = save_file("chow2.jpg", "chow2.jpg")
print("Filename", filename)
aws_info = get_file_info_from_aws(filename)
print("AWS Info", aws_info)