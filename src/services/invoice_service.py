from pathlib import Path
from pandas import DataFrame

from src.services.comparator import InvoiceComparator
from src.services.loaders import LoaderFactory
from src.services.parsers import ParserFactory


class InvoiceService:
    def load_and_parse(self, file_path: str | Path, **kwargs) -> DataFrame:
        file_path = Path(file_path)
        suffix = file_path.suffix.lower()
        loader = LoaderFactory.get_loader(suffix)
        raw_data = loader.read_source(file_path, **kwargs)
        parser = ParserFactory.get_parser(suffix)  # f821
        df = parser.parse(raw_data)

        return df

    def compare_invoices(self, df_xlsx: DataFrame, df_pdf: DataFrame) -> DataFrame:
        invoice_comparator = InvoiceComparator(df_xlsx, df_pdf)

        return invoice_comparator.compare()

    def run_reconciliation(self, xlsx_path: str, pdf_path: str, **kwargs) -> DataFrame:
        df_xlsx = self.load_and_parse(xlsx_path, **kwargs)
        df_pdf = self.load_and_parse(pdf_path)

        return self.compare_invoices(df_xlsx, df_pdf)
