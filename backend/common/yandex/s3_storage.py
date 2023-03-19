import boto3
import cv2
import numpy as np

from WebAdmin.settings import AWS_S3_ACCESS_KEY_ID, AWS_S3_SECRET_ACCESS_KEY


def generate_s3_client():
    s3_session = boto3.session.Session()
    s3_storage_client = s3_session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=AWS_S3_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY,
        region_name="ru-central1"
    )
    return s3_storage_client


def upload_file_to_s3(content, s3_key, bucket='myownbucket'):
    s3_storage_client = generate_s3_client()
    s3_storage_client.put_object(Bucket=bucket, Key=s3_key, Body=content)


def get_file_from_s3(s3_key, bucket='myownbucket'):
    """Get file content from S3 Object Storage by key"""
    s3_storage_client = generate_s3_client()
    obj_response = s3_storage_client.get_object(Bucket=bucket, Key=s3_key)
    content = obj_response['Body'].read()
    return content


def load_image_from_s3(s3_key, bucket='text-recognition'):
    """Get CV2 image object from S3 Object Storage by key"""
    content = get_file_from_s3(s3_key, bucket)
    np_array = np.frombuffer(content, np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    return img


def upload_image_to_s3(image, s3_key, bucket='text-recognition'):
    """Uploads CV2 image in .jpg format to S3 Object Storage to the specified key"""
    content = cv2.imencode(".jpg", image)[1].tobytes()
    upload_file_to_s3(content, s3_key, bucket)
