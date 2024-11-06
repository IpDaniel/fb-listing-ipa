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



# Example usage:
# formatted_data = some_formatter.format()
# uploader = FileUploader(formatted_data, "/path/to/output.txt")
# result = uploader.upload()
