from ..Base.Formatter import Formatter
import json

class JSONFormatter(Formatter):
    def format(self):
        if self.headers and self.data:
            return json.dumps([dict(zip(self.headers, row)) for row in self.data])
        return json.dumps(self.data)