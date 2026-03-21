from src.tools.extractor import (
    read_excel_file,
    read_text_from_pdf,
    extract_data_from_string,
)
from src.tools.exporter import write_reconciliation_report_to_csv
from src.tools.transformer import (
    transform_invoice_string_data_to_df,
    get_necessary_columns_from_df,
)
from src.tools.comparator import InvoiceComparator
# from src.handlers.constants import DATA_DIR

from pandas import DataFrame, read_excel
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Literal
import re


def read_source(file_path: str, xlsx_sheet_name=None) -> str | DataFrame:
    path = Path(file_path)

    if path.suffix == ".xlsx":
        return read_excel_file(str(path), sheet="Sheet1")
    if path.suffix == ".pdf":
        return read_text_from_pdf(str(path))

    raise ValueError(f"Unsupported file type: {file_path}")


def extract_pdf_data(pdf_text: str) -> list[str]:
    return extract_data_from_string(pdf_text)


def write_csv_report(dataframe: DataFrame, output_file_path: str) -> None:
    write_reconciliation_report_to_csv(dataframe, output_file_path)


def handle_write_to_db():
    """Zapis tableki do bazy"""
    pass


DEFAULT_XLSX_ENGINE: Literal["openpyxl"] = "openpyxl"  # unikamy magic numbers
XLSX_COL_NAMES: list["str"] = [
    "InvoiceNo",
    "Vendor",
    "Amount",
    "Currency",
    "InvoiceDate",
]


class BaseLoader(ABC):
    @abstractmethod
    def read_source(self, file_path: Path, **kwargs):
        pass


class XLSXLoader(BaseLoader):
    def read_source(self, file_path: Path, **kwargs):
        sheet_name = kwargs.get("sheet_name")
        return read_excel(file_path, sheet_name=sheet_name, engine=DEFAULT_XLSX_ENGINE)


class PDFLoader(BaseLoader):
    def read_source(self, file_path: Path, **kwargs):
        import pdfplumber

        pages = []
        # kontekst manager moze zabijać wszystko wiec lepiej zapisac zmienne poza context managerem
        with pdfplumber.open(file_path) as pdf_obj:
            for page in pdf_obj.pages:
                text_string = page.extract_text()
                if text_string:
                    pages.append(text_string)

        return pages


class LoaderFactory:  # interpretuje to jako miejsce wykonywania Loadera
    @staticmethod
    def get_loader(suffix: str) -> BaseLoader:
        match suffix:
            case ".xlsx":
                return XLSXLoader()
            case ".pdf":
                return PDFLoader()
            case _:
                raise ValueError(f"Unsupported file type: {suffix}")


class BaseParser(ABC):
    @abstractmethod
    def parse(self, suffix: str) -> DataFrame:
        pass


class ParserFactory:
    @staticmethod
    def get_parser(suffix: str) -> BaseParser:
        match suffix:
            case ".xlsx":
                return InvoiceXLSXParser()
            # TODO: zrób klase która zmienia nazwy kolumn na te same co w PDF'ie
            case ".pdf":
                return InvoicePDFParser()
            case _:
                raise ValueError(f"Unsupported file type: {suffix}")


class InvoiceXLSXParser(BaseParser):
    def parse(self, df: DataFrame) -> DataFrame:
        column_mapping = {
            "invoice_number": ["InvoiceNo", "invoice_no", "InvoiceNumber"],
            "date": ["InvoiceDate", "invoice_date"],
            "total": ["Amount", "amount"],
        }
        dict_to_rename = {}
        for target_col, possible_names in column_mapping.items():
            for possible_name in df.columns:
                if possible_name in possible_names:
                    dict_to_rename.update({possible_name: target_col})

        df.rename(columns=dict_to_rename, inplace=True)

        return df[["invoice_number", "date", "total"]]


class InvoicePDFParser(BaseParser):
    def parse(self, pages: list[str]) -> DataFrame:
        data = []

        for text in pages:
            invoice_number = self._extract_invoice_number(text)
            date = self._extract_date(text)
            total = self._extract_total(text)

            data.append(
                {"invoice_number": invoice_number, "date": date, "total": total}
            )

        return DataFrame(data)

    def _extract_invoice_number(self, text: str):
        match = re.search(r"Faktura\s+nr\s+(\S+)", text)
        return match.group(1) if match else None

    def _extract_date(self, text: str):
        match = re.search(r"\d{4}-\d{2}-\d{2}", text)
        return match.group(0) if match else None

    def _extract_total(self, text: str):
        match = re.search(r"Razem\s+(\d+[.,]\d+)", text)
        return match.group(1) if match else None


class InvoiceService:
    def read_source(self, file_path: str | Path, **kwargs) -> DataFrame:
        file_path = Path(file_path)
        suffix = file_path.suffix.lower()
        loader = LoaderFactory.get_loader(suffix)
        raw_data = loader.read_source(file_path, **kwargs)
        parser = ParserFactory.get_parser(suffix)
        df = parser.parse(raw_data)

        # przetwarzanie df to kolejny etap w serwisie
        return df


# TODO: ćwiczenie zeby jakoś wczytac dane z WORDa


def load_invoice_sources(
    xlsx_file_path: str, xlsx_sheet_name: str, pdf_file_path: str
) -> tuple[DataFrame, str]:
    df_xlsx = read_source(file_path=xlsx_file_path, xlsx_sheet_name=xlsx_sheet_name)
    pdf_content = read_source(file_path=pdf_file_path)

    return df_xlsx, pdf_content


def prepare_pdf_dataframe(pdf_content: str):
    extracted_data = extract_pdf_data(pdf_content)
    transformed_data = transform_invoice_string_data_to_df(extracted_data)
    return get_necessary_columns_from_df(transformed_data)


def run_workflow(xlsx_sheet_name: str, output_file_path: str) -> None:
    df_xlsx, pdf_content = load_invoice_sources(xlsx_sheet_name=xlsx_sheet_name)

    df_pdf = prepare_pdf_dataframe(pdf_content)

    comparator = InvoiceComparator(df_xlsx=df_xlsx, df_pdf=df_pdf)
    result_df = comparator.compare()
    write_csv_report(result_df, output_file_path)


# class InvoiceLoader:
#    def read_source(self, file_path: str | Path, **kwargs):
#        file_path = Path(file_path)
#        match file_path.suffix.lower():
#            case ".xlsx":
#                return XLSXLoader().read_source(file_path, **kwargs)
#            case ".pdf":
#                return PDFLoader().read_source(file_path)
#            case _:
#                raise ValueError(f"Unsupported file type: {file_path}")

# LoaderFactory zastępuje InvoiceLoader
# problemem wyzej bylo to ze trzeba uzyc read_source w srodku i robila duplikaty read_soure!
