import os
import boto3
from dotenv import load_dotenv

URL_WITH_REGION_CODE = "https://s3.us-west-1.amazonaws.com"

load_dotenv()

# BUCKET_NAME = os.environ["BUCKET_NAME"]
# ACCESS_KEY = os.environ["ACCESS_KEY"]
# SECRET_ACCESS_KEY = os.environ["SECRET_ACCESS_KEY"]


# s3_client = boto3.client('s3', aws_access_key_id = ACCESS_KEY, aws_secret_access_key = SECRET_ACCESS_KEY)


class AWS:
    """Allows user to interact with AWS s3 for files."""
    def __init__(self, aws_access_key_id, aws_secret_access_key, bucket_name):
        # self.aws_access_key_id = aws_access_key_id
        # self.aws_secret_access_key = aws_secret_access_key
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    def save_file(self, file_data, filename):
        self.s3_client.upload_fileobj(file_data, self.bucket_name, filename)

    def get_file_info_from_aws(self, filename):
        response = self.s3_client.generate_presigned_url('get_object',
                                                Params={'Bucket': self.bucket_name,
                                                        'Key': filename})
        return response


# filename = AWS.save_file("chow2.jpg", "chow2.jpg")
# print("Filename", filename)
# aws_info = AWS.get_file_info_from_aws(filename)
# print("AWS Info", aws_info)
