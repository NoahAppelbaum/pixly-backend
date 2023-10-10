import boto3
BUCKET_NAME = "pixly-photo-sharing"

s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)

s3_client = boto3.client('s3')


with open("chow.jpg", "rb") as data:
    print(s3_client.upload_fileobj(data, BUCKET_NAME, "chow.jpg"))
