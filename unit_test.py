import logging
import boto3
from botocore.exceptions import ClientError
import os
import argparse


class AWS_OBJ:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3_resource = boto3.resource('s3')
        self.s3_client = boto3.client('s3')

    def create_bucket1(self, region=None):
        try:
            if region is None:
                self.s3_client.create_bucket(Bucket=self.bucket_name)
            else:
                location = {'LocationConstraint': region}
                self.s3_client.create_bucket(Bucket=self.bucket_name,
                                CreateBucketConfiguration=location)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def check_bucket(self):
        fl = True
        for bucket in self.s3_resource.bucket.all():
            if str(bucket.name) == self.bucket_name:
                fl = False
        self.create_bucket1() if not fl else None
        return fl

    def list_bucket(self, args):
        for bucket in self.s3_resource.buckets.all():
            print(bucket.name)

    def upload_file(self, args):
        file_name = args.file_name

        self.check_bucket()

        object_name = os.path.basename(file_name)

        # Upload the file
        try:
            self.s3_client.upload_file(file_name, self.bucket_name, object_name)
        except ClientError as e:
            logging.error(e)
            print("upload error")
            return False
        except FileNotFoundError:
            print(f"The system cannot find the file specified: {file_name}")
            return False
        print("upload was done")
        return True

    def download(self, args):
        try:
            # s3.download_file('amzn-s3-demo-bucket', 'OBJECT_NAME', 'FILE_NAME')
            name_file = args.file_download

            print("fails which you have:")
            objects = self.s3_resource.list_objects_v2(Bucket=self.bucket_name)
            for obj in objects['Contents']:
                print(obj['Key'])

            ind = name_file.index(".")
            self.s3_resource.download_file(self.bucket_name, name_file, f"s3_{name_file[:ind]}{name_file[ind:]}")

        except Exception:
            print("no such file")


class MyModel:
    def __init__(self, name, val):
        self.name = name
        self.val = val

    def save_obj(self, arg):
        print("save")

    def print_obj(self, arg):
        print("list")

    def upload_file(self, args):
        file_name = args.file_name
        print(f"upload {file_name}")

    def download(self, args):
        download_name = args.file_name
        print(f"download fail: {download_name}")


def parse_args():
    parser = argparse.ArgumentParser(description="Amazon S3")
    subparsers = parser.add_subparsers(dest="command", help="command options: list, upload, download")

    model1 = MyModel("v1", "1")

    parser_list = subparsers.add_parser("list")
    parser_list.set_defaults(func=model1.print_obj)

    upload_bucket = subparsers.add_parser("upload")
    upload_bucket.add_argument("file_name", type=str)
    upload_bucket.set_defaults(func=model1.upload_file)

    return parser.parse_args()


def unit_test():
    parser = argparse.ArgumentParser(description="Amazon S3")
    args = parse_args()


    args.func(args)


if __name__ == "__main__":
    unit_test()