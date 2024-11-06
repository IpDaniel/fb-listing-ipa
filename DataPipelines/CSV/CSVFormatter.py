from ..Base.Formatter import Formatter
from io import StringIO
import csv

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