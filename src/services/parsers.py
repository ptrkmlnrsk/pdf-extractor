from src.services.base import BaseParser
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
            invoice_ids = self._extract_invoice_id(text)
            amounts = self._extract_amount(text)

            for inv, amount in zip(invoice_ids, amounts):
                data.append({"invoice_id": inv, "amount": amount})

        return DataFrame(data)

    def _extract_invoice_id(self, text: str):
        match = re.findall(r"(INV\d{3})", text)
        return match if match else None

    #
    def _extract_amount(self, text: str):
        match = re.findall(r"(\d+\.\d{2})", text)
        return match if match else None


class InvoiceXLSXParser(BaseParser):
    def parse(self, df: DataFrame) -> DataFrame:
        column_mapping = {
            "invoice_id": ["InvoiceNo", "invoice_no", "InvoiceNumber"],
            # "date": ["InvoiceDate", "invoice_date"],
            "amount": ["Amount", "amount"],
        }
        dict_to_rename = {}
        for target_col, possible_names in column_mapping.items():
            for possible_name in df.columns:
                if possible_name in possible_names:
                    dict_to_rename.update({possible_name: target_col})

        df.rename(columns=dict_to_rename, inplace=True)

        return df[["invoice_id", "amount"]]
