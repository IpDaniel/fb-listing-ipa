import json
import csv
from abc import ABC, abstractmethod
from io import StringIO

# This abstract base class defines an interface for various output formatters.
# Concrete implementations provide specific formatting methods for data
# returned by the Connection.executeQuery() method.

class Formatter(ABC):
    def __init__(self, headers=None, data=None):
        self.headers = headers
        self.data = data

    @abstractmethod
    def format(self):
        raise NotImplementedError("Subclasses must implement format() method")

class JSONFormatter(Formatter):
    def format(self):
        if self.headers and self.data:
            return json.dumps([dict(zip(self.headers, row)) for row in self.data])
        return json.dumps(self.data)

class CSVFormatter(Formatter):
    def format(self):
        output = StringIO()
        writer = csv.writer(output)
        
        if self.headers:
            #check if the headers are just a list of column names and throw an error if they are
            if not isinstance(self.headers, list):
                raise ValueError("Headers are not a list of column names")
            # Extract only the first element (column name) from each header tuple
            header_row = [header[0] for header in self.headers]
            writer.writerow(header_row)
        
        if self.data:
            # The data is already in the correct format for writerows()
            writer.writerows(self.data)
        
        return output.getvalue()

