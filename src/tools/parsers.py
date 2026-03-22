from src.tools.base import BaseParser
from pandas import DataFrame
import re


class ParserFactory:
    @staticmethod
    def get_parser(suffix: str) -> BaseParser:
        match suffix:
            case ".xlsx":
                return InvoiceXLSXParser()
            case ".pdf":
                return InvoicePDFParser()
            case _:
                raise ValueError(f"Unsupported file type: {suffix}")


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
