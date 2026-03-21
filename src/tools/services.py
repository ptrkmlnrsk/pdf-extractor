from pathlib import Path
from pandas import DataFrame
from src.tools.loaders import LoaderFactory
from src.tools.parsers import ParserFactory


class InvoiceService:
    def read_source(self, file_path: str | Path, **kwargs) -> DataFrame:
        file_path = Path(file_path)
        suffix = file_path.suffix.lower()
        loader = LoaderFactory.get_loader(suffix)
        raw_data = loader.read_source(file_path, **kwargs)
        parser = ParserFactory.get_parser(suffix)  # f821
        df = parser.parse(raw_data)

        # przetwarzanie df to kolejny etap w serwisie
        return df


# TODO: ćwiczenie zeby jakoś wczytac dane z WORDa
