import subprocess
import random
import os
import boto3
from botocore.exceptions import NoCredentialsError
import logging

def upload_to_aws(local_file, bucket, s3_file):
    aws_access_key_id = os.environ.get("aws_access_key_id", "accessKey1")
    aws_secret_access_key = os.environ.get("aws_secret_access_key", "verySecretKey1")
    endpoint_url = os.environ.get("S3_ENDPOINT_URL", None)
    if not endpoint_url:
        raise Exception("No S3 endpoind passed")


    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url
    )

    try:
        s3.upload_file(local_file, bucket, s3_file, ExtraArgs={'ACL': 'public-read'})
        print("Upload Successful")

        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False



if not os.environ.get('IGNITION_CONFIG'):
    raise Exception("ignition file not passed")

with open('ignition.config', 'w') as f:
    f.write(os.environ['IGNITION_CONFIG'])

image_name = os.environ.get("IMAGE_NAME", "coreos_install{}.img".format(random.getrandbits(30)))

command = "./coreos-installer iso embed -c ignition.config -o {} {} -f".format(image_name, os.environ.get("COREOS_IMAGE"))

subprocess.check_output(command, shell=True)

bucket_name = os.environ.get('S3_BUCKET', 'test')
uploaded = upload_to_aws(image_name, bucket_name, image_name)
