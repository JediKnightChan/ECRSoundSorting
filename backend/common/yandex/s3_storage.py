import boto3
import cv2
import os
import numpy as np

from collections import namedtuple
from operator import attrgetter

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


def s3walk_dirs(path):
    subdirs = list(s3list(path, recursive=False, list_objs=False))
    yield from subdirs
    for subdir in subdirs:
        yield from s3walk_dirs(subdir.key)


def s3list(path, start=None, end=None, recursive=True, list_dirs=True,
           list_objs=True, limit=None):
    """
    Iterator that lists a bucket's objects under s3_path, (optionally) starting with
    start and ending before end.

    If recursive is False, then list only the "depth=0" items (dirs and objects).

    If recursive is True, then list recursively all objects (no dirs).

    Args:
        path:
            a directory in the bucket.
        start:
            optional: start key, inclusive (may be a relative s3_path under s3_path, or
            absolute in the bucket)
        end:
            optional: stop key, exclusive (may be a relative s3_path under s3_path, or
            absolute in the bucket)
        recursive:
            optional, default True. If True, lists only objects. If False, lists
            only depth 0 "directories" and objects.
        list_dirs:
            optional, default True. Has no effect in recursive listing. On
            non-recursive listing, if False, then directories are omitted.
        list_objs:
            optional, default True. If False, then directories are omitted.
        limit:
            optional. If specified, then lists at most this many items.

    Returns:
        an iterator of S3Obj.
"""
    s3 = generate_s3_client()
    S3Obj = namedtuple('S3Obj', ['key', 'mtime', 'size', 'ETag'])

    kwargs = dict()
    if start is not None:
        if not start.startswith(path):
            start = os.path.join(path, start)
        # note: need to use a string just smaller than start, because
        # the list_object API specifies that start is excluded (the first
        # result is *after* start).
        kwargs.update(Marker=__prev_str(start))
    if end is not None:
        if not end.startswith(path):
            end = os.path.join(path, end)
    if not recursive:
        kwargs.update(Delimiter='/')
        if not path.endswith('/'):
            path += '/'
    kwargs.update(Prefix=path)
    if limit is not None:
        kwargs.update(PaginationConfig={'MaxItems': limit})

    paginator = s3.get_paginator('list_objects')
    for resp in paginator.paginate(Bucket='text-recognition', **kwargs):
        q = []
        if 'CommonPrefixes' in resp and list_dirs:
            q = [S3Obj(f['Prefix'], None, None, None) for f in resp['CommonPrefixes']]
        if 'Contents' in resp and list_objs:
            q += [S3Obj(f['Key'], f['LastModified'], f['Size'], f['ETag']) for f in resp['Contents']]
        # note: even with sorted lists, it is faster to sort(a+b)
        # than heapq.merge(a, b) at least up to 10K elements in each list
        q = sorted(q, key=attrgetter('key'))
        if limit is not None:
            q = q[:limit]
            limit -= len(q)
        for p in q:
            if end is not None and p.key >= end:
                return
            yield p


def __prev_str(s):
    if len(s) == 0:
        return s
    s, c = s[:-1], ord(s[-1])
    if c > 0:
        s += chr(c - 1)
    s += ''.join(['\u7FFF' for _ in range(10)])
    return s
