#!/usr/bin/python3


#arguments: gif url, bucket name, expiration time

import sys

# Fetch and save a file from the internet using requests
import requests
import os

def download_file(url, file_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded to {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading: {e}")

image_url = sys.argv[1]
file = "downloaded_image.gif"
path = os.path.join(os.getcwd(), file) # Saves to current directory

download_file(image_url, path)

#Upload file to bucket in S3

import boto3
s3 = boto3.client('s3', region_name="us-east-1")

resp = s3.put_object(
    Body = file,
    Bucket = sys.argv[2],
    Key = file,
    ContentType='image/gif'
)
#response = s3.generate_presigned_url(
#    'get_object',
#    Params={'Bucket': sys.argv[2], 'Key': file},
#    ExpiresIn=sys.argv[3]
#    )

#print(response)
import logging
from botocore.exceptions import ClientError


def create_presigned_url(bucket_name, object_name, expiration):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    # Generate a presigned URL for the S3 object
    try:
        response = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None
    # The response contains the presigned URL
    print(response)

create_presigned_url(sys.argv[2], file, int(sys.argv[3]))
