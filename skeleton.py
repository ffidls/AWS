import logging
import boto3
from botocore.exceptions import ClientError
import os


class S3R:
    def __init__(self, resource):
        self.resource = resource

    def buckets_all(self):
        try:
            return self.resource.buckets.all()
        except Exception:
            return self.resource.keys()

    def name(self, bucket):
        try:
            return str(bucket.name)
        except Exception:
            return str(bucket)


class S3C:
    def __init__(self, client):
        self.s3_client = client

    def upload_file(self, file_name, bucket_name, object_name):
        try:
            self.s3_client.upload_file(file_name, bucket_name, object_name)
        except Exception:
            None

    def download(self, bucket_name, file_name, path):
        try:
            self.s3_client.download_file(bucket_name, file_name, path)
        except Exception:
            None


class Brain:
    def __init__(self, bucket_name, resource, client):
        self.bucket_name = bucket_name
        self.s3_resource = S3R(resource)
        self.s3_client = S3C(client)

    def list_bucket(self, args):
        for bucket in self.s3_resource.buckets_all():
            print(bucket.name())

    def create_bucket1(self):
        return True

    def check_bucket(self):
        fl = True
        for bucket in self.s3_resource.buckets_all():
            if bucket.name() == self.bucket_name:
                fl = False
        self.create_bucket1() if fl else None
        return fl

    def upload_file(self, args):
        file_name = args.file_name
        self.check_bucket()
        object_name = os.path.basename(file_name)

        try:
            self.s3_client.upload_file(file_name, self.bucket_name, object_name)
        except FileNotFoundError:
            print(f"The system cannot find the file specified: {file_name}")
            return False

        print("upload was done")
        return True

    def download(self, args):
        try:
            name_file = args.file_dowload
            ind = name_file.index(".")
            self.s3_client.download(self.bucket_name, name_file, f"s3_{name_file[:ind]}{name_file[ind:]}")

        except Exception:
            print("no such file")


model_AWS = Brain(bucket_name= "ffodls-s3-demo-bucket-example111119",
                  resource=boto3.resource("s3"),
                  client=boto3.client("s3"))


