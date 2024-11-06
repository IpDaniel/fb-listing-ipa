from ..Base.Formatter import Formatter

class MEFormatter(Formatter):

    def __init__(self, headers, data, expected_headers):
        for header in expected_headers:
            if header not in self.headers:
                raise ValueError(f"Header {header} not found in data")
        super().__init__(headers, data)
        self.expected_headers = expected_headers
        
    def format(self):
        return super().format()
    
    def formatting_string(self):
        return ""
