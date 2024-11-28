import boto3
from botocore.exceptions import ClientError
from chalicelib.utils.ssm import get_value_parameter


class S3Bucket:

    bucket_name = "currency-collector"
    client_s3 = boto3.client(
        "s3",
        aws_access_key_id=get_value_parameter("ACCESS_KEY"),
        aws_secret_access_key=get_value_parameter("SECRET_KEY"),
    )

    def write_file(self, content, file_name):
        try:
            existing_content = (
                self.client_s3.get_object(Bucket=self.bucket_name, Key=file_name)[
                    "Body"
                ]
                .read()
                .decode("utf-8")
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                existing_content = ""
            else:
                raise e

        new_content = existing_content + "\n" + content

        self.client_s3.put_object(
            Bucket=self.bucket_name, Key=file_name, Body=new_content
        )
