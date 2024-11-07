from ..Base.Connection import Connection
import pandas as pd

class MECollector(Connection):
    def __init__(self, file_path, expected_headers=[], lines_to_skip=1):
        self.file_path = file_path
        df = pd.read_excel(file_path, skiprows=lines_to_skip)
        for header in expected_headers:
            if header not in self.df.columns:
                raise ValueError(f"Header {header} not found in file")
        self.df = df
    
    def connect(self):
        pass
    
    def close(self):
        self.df.to_excel(self.file_path, index=False)

    def executeQuery(self):
        pass
    
    def storeSessionData(self):
        pass
