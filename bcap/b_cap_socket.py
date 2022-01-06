from abc import ABCMeta, abstractmethod


class BCapSocket(metaclass=ABCMeta):
    @abstractmethod
    def connect(self, endpoint: str, timeout: float, retry: int) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def request(self, func_id: int, args: list) -> any:
        pass

    @abstractmethod
    def get_timeout(self) -> float:
        pass

    @abstractmethod
    def set_timeout(self, timeout: float) -> None:
        pass

    @abstractmethod
    def set_retry(self, retry: int) -> None:
        pass

    @abstractmethod
    def set_compression(self, enable: bool, level: int = -1) -> None:
        pass
