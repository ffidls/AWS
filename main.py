import logging
import boto3
from botocore.exceptions import ClientError
import os
import argparse

# Let's use Amazon S3
s3 = boto3.resource('s3')
bucket_name = "ffodls-s3-demo-bucket-example111117"


def create_bucket(
    name=bucket_name,
    region=None):

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def check_bucket(name):
    """s3_for_check = boto3.client('s3')
    try:
        s3_for_check.head_object(Bucket=name)
        return True

    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False"""
    fl = True
    for bucket in s3.buckets.all():
        if str(bucket_name) == name:
            fl = False
        # print(bucket.name)
    create_bucket(name) if not fl else None
    return fl


def list_buckets(args):
    # Print out bucket names
    for bucket in s3.buckets.all():
        print(bucket.name)


def upload_file(args):
    file_name = args.file_name

    check_bucket(bucket_name)

    object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        print("upload error")
        return False
    except FileNotFoundError:
        print(f"The system cannot find the file specified: {file_name}")
        return False
    print("upload was done")
    return True

"""
s3 = boto3.client('s3')
with open("FILE_NAME", "rb") as f:
    s3.upload_fileobj(f, "amzn-s3-demo-bucket", "OBJECT_NAME")
"""

def download(args):
    try:
        s3 = boto3.client('s3')
        # s3.download_file('amzn-s3-demo-bucket', 'OBJECT_NAME', 'FILE_NAME')
        name_file = args.file_download

        print("fails which you have:")
        objects = s3.list_objects_v2(Bucket=bucket_name)
        for obj in objects['Contents']:
            print(obj['Key'])

        ind = name_file.index(".")
        s3.download_file(bucket_name, name_file, f"s3_{name_file[:ind]}{name_file[ind:]}")

    except Exception:
        print("no such file")


def parse_args():
    parser = argparse.ArgumentParser(description="Amazon S3")
    subparsers = parser.add_subparsers(dest="command", help="command options: list, upload, download")

    parser_list = subparsers.add_parser("list", help="list of S3 ")
    parser_list.set_defaults(func=list_buckets)

    upload_bucket = subparsers.add_parser("upload", help="write file name")
    upload_bucket.add_argument("file_name", type=str)
    upload_bucket.set_defaults(func=upload_file)

    download_fail = subparsers.add_parser("download", help="download file")
    download_fail.add_argument("file_download", type=str)
    download_fail.set_defaults(func=download)

    return parser.parse_args()


def main():
    parser = argparse.ArgumentParser(description="Amazon S3")
    subparsers = parser.add_subparsers(dest="command", help="command options: list, upload, download")
    args = parse_args()

    # check on namespace
    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()