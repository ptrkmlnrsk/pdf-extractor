from abc import ABC, abstractmethod
from pandas import DataFrame
from pathlib import Path


class BaseLoader(ABC):
    @abstractmethod
    def read_source(self, file_path: Path, **kwargs):
        pass


class BaseParser(ABC):
    @abstractmethod
    def parse(self, suffix: str) -> DataFrame:
        pass
