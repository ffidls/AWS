from Operations import FileOperations


class FakeFileOperations(FileOperations):
    def __init__(self, bucket_name, fake_data=dict):
        super().__init__()
        self.fake_data = fake_data
        self.bucket_name = bucket_name

    def list(self):
        return self.fake_data.keys()

    def name(self, bucket):
        return str(bucket)

    def upload(self, file_name, bucket_name, object_name):
        self.fake_data[bucket_name].append(file_name)

    def download(self, bucket_name, file_name, path):
        pass

    def create(self):
        self.fake_data[self.bucket_name] = []
