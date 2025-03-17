import os

from Operations import FileOperations


class Skeleton:
    def __init__(self, bucket_name, file_operations=FileOperations):
        self.bucket_name = bucket_name
        self.file_operations = file_operations

    def list_buckets(self, args):
        for bucket in self.file_operations.list():
            print(bucket)

    def check_bucket(self):
        fl = True
        for bucket in self.file_operations.list():
            if bucket == self.bucket_name:
                fl = False
        self.file_operations.create() if fl else None
        return fl

    def upload_file(self, args):
        file_name = args.file_name
        self.check_bucket()
        object_name = os.path.basename(file_name)

        try:
            self.file_operations.upload(file_name, self.bucket_name, object_name)
        except FileNotFoundError:
            print(f"The system cannot find the file specified: {file_name}")
            return False

        print("upload was done")
        return True

    def download(self, args):
        try:
            name_file = args.file_download
            ind = name_file.index(".")
            self.file_operations.download(self.bucket_name, name_file, f"s3_{name_file[:ind]}{name_file[ind:]}")

        except Exception:
            print("no such file")
