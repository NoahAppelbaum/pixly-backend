import boto3

URL_WITH_REGION_CODE = "https://s3.us-west-1.amazonaws.com"


class AWS:
    """Allows user to interact with AWS s3 for files."""
    def __init__(self, aws_access_key_id, aws_secret_access_key, bucket_name):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    def save_file(self, file, filename):
        self.s3_client.upload_fileobj(
            file,
            self.bucket_name,
            filename,
            ExtraArgs={"ContentType": "image/jpg"}
            )

    def get_presigned_url(self, filename):
        response = self.s3_client.generate_presigned_url('get_object',
                                                Params={'Bucket': self.bucket_name,
                                                        'Key': filename})
        return response


# filename = AWS.save_file("chow2.jpg", "chow2.jpg")
# print("Filename", filename)
# aws_info = AWS.get_file_info_from_aws(filename)
# print("AWS Info", aws_info)
