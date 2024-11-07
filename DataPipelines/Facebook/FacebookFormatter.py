from ..Base.Formatter import Formatter

class FacebookFormatter(Formatter):
    def format(self, data, expected_headers):
        for header in expected_headers:
            if header not in data.columns:
                raise ValueError(f"Header {header} not found in data")
        return f"String part 1{data[expected_headers[0]]} 
        String part 2{data[expected_headers[1]]}"
