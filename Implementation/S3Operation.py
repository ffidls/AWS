from Operations import FileOperations

import logging
import boto3
from botocore.exceptions import ClientError
import os
import argparse


class S3FileOperations(FileOperations):
    def __init__(self, bucket_name, s3_resource, s3_client):
        super().__init__()
        self.bucket_name = bucket_name
        self.s3_resource = s3_resource
        self.s3_client = s3_client

    def create(self, region=None):
        try:
            if region is None:
                self.s3_client.create_bucket(Bucket=self.bucket_name)
            else:
                location = {'LocationConstraint': region}
                self.s3_client.create_bucket(Bucket=self.bucket_name,
                                CreateBucketConfiguration=location)
            return True

        except ClientError as e:
            logging.error(e)
            return ClientError

    def list(self):
        return self.s3_resource.buckets.all()

    def upload(self, file_name, bucket_name, object_name):
        objects = self.s3_client.list_objects_v2(Bucket=bucket_name)
        for obj in objects['Contents']:
            print(obj['Key'])
        self.s3_client.upload_file(file_name, bucket_name, object_name)

    def download(self, bucket_name, file_name, path):
        objects = self.s3_client.list_objects_v2(Bucket=bucket_name)
        for obj in objects['Contents']:
            print(obj['Key'])

        self.s3_client.download_file(bucket_name, file_name, path)

    def name(self, bucket):
        return str(bucket.name())
