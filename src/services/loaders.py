from pandas import read_excel
from pathlib import Path
from src.services.base import BaseLoader
from typing import Literal

DEFAULT_XLSX_ENGINE: Literal["openpyxl"] = "openpyxl"  # unikamy magic numbers


class XLSXLoader(BaseLoader):
    def read_source(self, file_path: Path, **kwargs):
        sheet_name = kwargs.get("sheet_name")
        return read_excel(file_path, sheet_name=sheet_name, engine=DEFAULT_XLSX_ENGINE)


class PDFLoader(BaseLoader):
    def read_source(self, file_path: Path, **kwargs) -> list[str]:
        import pdfplumber

        pages = []

        with pdfplumber.open(file_path) as pdf_obj:
            for page in pdf_obj.pages:
                text_string = page.extract_text()
                if text_string:
                    pages.append(text_string)

        return pages


class LoaderFactory:
    @staticmethod
    def get_loader(suffix: str) -> BaseLoader:
        match suffix:
            case ".xlsx":
                return XLSXLoader()
            case ".pdf":
                return PDFLoader()
            case _:
                raise ValueError(f"Unsupported file type: {suffix}")
