import argparse

import boto3

from Implementation.S3Operation import S3FileOperations
from Logic.Brain import Skeleton


def parse_args():
    parser = argparse.ArgumentParser(description="Amazon S3")
    subparsers = parser.add_subparsers(dest="command", help="command options: list, upload, download")

    S3File = S3FileOperations(bucket_name="ffodls-s3-demo-bucket-example111119",
                              s3_resource=boto3.resource("s3"),
                              s3_client=boto3.client("s3"))
    model1 = Skeleton(bucket_name="ffodls-s3-demo-bucket-example111119",
                      file_operations=S3File)

    parser_list = subparsers.add_parser("list", help="list of S3 ")
    parser_list.set_defaults(func=model1.list_buckets)

    upload_bucket = subparsers.add_parser("upload", help="write file name")
    upload_bucket.add_argument("file_name", type=str)
    upload_bucket.set_defaults(func=model1.upload_file)

    download_fail = subparsers.add_parser("download", help="download file")
    download_fail.add_argument("file_download", type=str)
    download_fail.set_defaults(func=model1.download)

    return parser.parse_args()


def main():
    parser = argparse.ArgumentParser(description="Amazon S3")
    args = parse_args()

    # check on namespace
    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()