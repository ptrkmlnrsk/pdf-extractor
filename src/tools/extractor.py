import pdfplumber
import pandas as pd

from re import findall


def read_excel_file(filename: str, sheet: str) -> pd.DataFrame:
    return pd.read_excel(filename, sheet_name=sheet, engine="openpyxl")


def read_text_from_pdf(file_name: str) -> str:
    with pdfplumber.open(file_name) as pdf_obj:
        text_list = ""

        for page in pdf_obj.pages:
            text_list += page.extract_text()

        return text_list


def extract_data_from_string(string: str) -> list[str]:
    regex = r"(INV\d{3})[\s\S]*?(\d+\.\d{2})"

    return findall(regex, string)
