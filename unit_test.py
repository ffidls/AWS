import unittest
from moto import mock_aws
import boto3


def func_to_test(bucket_name, key, content):
    s3 = boto3.resource("s3")
    object = s3.Object(bucket_name, key)
    object.put(Body=content)


class MyTest(unittest.TestCase):

    bucket_name = "test-bucket"
    def setUp(self):
        self.mock_aws = mock_aws()
        self.mock_aws.start()

        # you can use boto3.client("s3") if you prefer
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(self.bucket_name)
        bucket.create()

    def tearDown(self):
        self.mock_aws.stop()

    def test(self):
        content = b"abc"
        key = "/path/to/obj"

        # run the file which uploads to S3
        func_to_test(self.bucket_name, key, content)

        # check the file was uploaded as expected
        s3 = boto3.resource("s3")
        object = s3.Object(self.bucket_name, key)
        actual = object.get()["Body"].read()
        self.assertEqual(actual, content)