import csv
from DataPipelines.Base.Connection import Connection

class DataManager:
    def __init__(self, name="unnamed", query="", postgres_credentials=None, 
                 connection=None, formatter=None, uploader=None, headers=True):
        self.name = name
        self.query = query
        self.postgres_credentials = postgres_credentials or {}
        self.connection = connection or Connection(self.postgres_credentials, self.query)
        self.formatter = formatter
        self.uploader = uploader
        self.headers = headers

    def process_data(self):
        self.connection.connect()
        data = self.connection.executeQuery(include_headers=self.headers)
        formatted_data = self.formatter.format(data)
        self.uploader.formatted_data = formatted_data
        result = self.uploader.upload()
        self.connection.close()
        return result

    def get_raw_data(self):
        self.connection.connect()
        data = self.connection.executeQuery(include_headers=self.headers)
        self.connection.close()
        return data

    def get_formatted_data(self):
        raw_data = self.get_raw_data()
        return self.formatter.format(raw_data)

    def save_attributes(self, csv_file_path):
        attributes = {
            'name': self.name,
            'query': self.query,
            'postgres_credentials': str(self.postgres_credentials),
            'connection': str(self.connection),
            'formatter': str(self.formatter),
            'uploader': str(self.uploader),
            'headers': str(self.headers)
        }
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in attributes.items():
                writer.writerow([key, value])
