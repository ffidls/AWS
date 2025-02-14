import logging
import boto3
from botocore.exceptions import ClientError
import os
import argparse


# Let's use Amazon S3
s3 = boto3.resource('s3')
bucket_name = "ffodls-s3-demo-bucket-example111111"

def check_bucket(name):
    s3_for_check = boto3.client('s3')
    try:
        s3_for_check.head_object(Bucket=name, Key='file-key')
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False                                                             


def list_buckets(args):
    # Print out bucket names
    for bucket in s3.buckets.all():
        print(bucket.name)


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


def upload_file(args):
    file_name = args.file_name

    """if not check_bucket(bucket_name):
        print("create a new bucket, try again")
        #create_bucket()"""

    object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        print("upload error")
        return False
    print("uploud done")
    return True

"""
s3 = boto3.client('s3')
with open("FILE_NAME", "rb") as f:
    s3.upload_fileobj(f, "amzn-s3-demo-bucket", "OBJECT_NAME")
"""

def download(args):
    s3 = boto3.client('s3')
    #s3.download_file('amzn-s3-demo-bucket', 'OBJECT_NAME', 'FILE_NAME')

    print("fails which you have:")
    objects = s3.list_objects_v2(Bucket=bucket_name)
    for obj in objects['Contents']:
        print(obj['Key'])

    name_fail = input("write fail name which you want dwoload: ")
    ind = name_fail.index(".")
    s3.download_file(bucket_name, name_fail, f"s3_file{name_fail[ind:]}")
  

def parse_args():
    parser = argparse.ArgumentParser(description="Amazon S3")
    subparsers = parser.add_subparsers(dest="command")

    parser_list = subparsers.add_parser("list", help="list of S3 ")
    parser_list.set_defaults(func=list_buckets)

    upload_bucket = subparsers.add_parser("uploud", help="write file name")
    upload_bucket.add_argument("file_name", type=str)
    upload_bucket.set_defaults(func=upload_file)

    download_fail = subparsers.add_parser("download", help="dowloud fail")
    download_fail.set_defaults(func=download)

    return parser.parse_args()


def main():
    args = parse_args()

    # Проверяем, передана ли команда
    if not hasattr(args, "func"):
        print("error")
        return

    args.func(args)


if __name__ == "__main__":
    main()