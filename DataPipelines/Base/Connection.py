from abc import ABC, abstractmethod

class Connection(ABC):
    @abstractmethod
    def connect(self):
        raise NotImplementedError("connect method not implemented for abstract class")

    @abstractmethod
    def close(self):
        raise NotImplementedError("close method not implemented for abstract class")

    @abstractmethod
    def executeQuery(self, headers=True, read_only=True):
        raise NotImplementedError("executeQuery method not implemented for abstract class")

    @abstractmethod
    def storeSessionData(self, csv_file_path):
        raise NotImplementedError("storeSessionData method not implemented for abstract class")


