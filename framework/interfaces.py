from abc import ABC, abstractmethod

class BaseLexer(ABC):
    @abstractmethod
    def tokenize(self, code: str) -> list:
        pass

class BaseParser(ABC):
    @abstractmethod
    def parse(self, tokens: list) -> dict:
        pass

class BaseInterpreter(ABC):
    @abstractmethod
    def execute(self, ast: dict) -> str:
        pass
