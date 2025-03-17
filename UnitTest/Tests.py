import unittest

from Logic.Brain import Skeleton
from UnitTest.Mocks.FakeOperations import FakeFileOperations


fake_data = {"b1": ["f1", "f2"],
              "b2": ["f1", "f2", "f3"],
              "b3": ["f1"]}
fake_model = FakeFileOperations(bucket_name="b1", fake_data=fake_data)


class TestFileOperations(unittest.TestCase):
    def test_lists_of_buckets(self):
        self.assertEqual(fake_model.list(), fake_data.keys())

    def test_check_bucket(self):
        fake_logic = Skeleton(bucket_name="b4",
                              file_operations=fake_model)
        self.assertEqual(fake_logic.check_bucket(), True)


