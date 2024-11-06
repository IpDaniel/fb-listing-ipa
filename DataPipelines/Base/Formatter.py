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



