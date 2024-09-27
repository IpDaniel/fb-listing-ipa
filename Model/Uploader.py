from abc import ABC, abstractmethod

class Uploader(ABC):
    def __init__(self, formatted_data):
        self.formatted_data = formatted_data

    @abstractmethod
    def upload(self):
        """
        Upload the formatted data to the respective location.
        This method should be implemented by all subclasses.
        """
        raise NotImplementedError("Subclasses must implement upload() method")

class FileUploader(Uploader):
    def __init__(self, formatted_data, file_path):
        super().__init__(formatted_data)
        self.file_path = file_path

    def upload(self):
        with open(self.file_path, 'w') as file:
            file.write(self.formatted_data)
        return f"Data uploaded to file: {self.file_path}"

class S3Uploader(Uploader):
    def __init__(self, formatted_data, bucket_name, object_key):
        super().__init__(formatted_data)
        self.bucket_name = bucket_name
        self.object_key = object_key

    def upload(self):
        # This is a placeholder. In a real implementation, you would use boto3 or another S3 client
        print(f"Uploading data to S3 bucket '{self.bucket_name}' with key '{self.object_key}'")
        # s3_client.put_object(Bucket=self.bucket_name, Key=self.object_key, Body=self.formatted_data)
        return f"Data uploaded to S3: s3://{self.bucket_name}/{self.object_key}"

class DatabaseUploader(Uploader):
    def __init__(self, formatted_data, connection_string, table_name):
        super().__init__(formatted_data)
        self.connection_string = connection_string
        self.table_name = table_name

    def upload(self):
        # This is a placeholder. In a real implementation, you would use an appropriate database client
        print(f"Uploading data to database table '{self.table_name}'")
        # db_connection = create_connection(self.connection_string)
        # upload_to_table(db_connection, self.table_name, self.formatted_data)
        return f"Data uploaded to database table: {self.table_name}"

# Example usage:
# formatted_data = some_formatter.format()
# uploader = FileUploader(formatted_data, "/path/to/output.txt")
# result = uploader.upload()
