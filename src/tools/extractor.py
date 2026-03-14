import pdfplumber
from pandas import DataFrame, read_excel
from re import findall
from pathlib import Path


def read_excel_file(filepath: str, sheet: str) -> DataFrame:
    if not filepath:
        raise ValueError("filepath cannot be empty")

    if not sheet:
        raise ValueError("You need to specify a sheet name")

    if not Path(filepath).exists():
        raise ValueError(f"{filepath} does not exist")

    df = read_excel(filepath, sheet_name=sheet, engine="openpyxl")

    if df.empty:
        raise ValueError(f"{filepath} does not contain any data")

    return df


def read_text_from_pdf(filepath: str) -> str:
    if not filepath:
        raise ValueError("filepath cannot be empty")

    if not Path(filepath).exists():
        raise ValueError(f"{filepath} does not exist")

    with pdfplumber.open(filepath) as pdf_obj:
        text_list = ""

        for page in pdf_obj.pages:
            text_list += page.extract_text()

    if len(text_list) > 0:
        raise ValueError(f"{filepath} does not contain any text")

    return text_list


def extract_data_from_string(string: str) -> list[str]:
    regex = r"(INV\d{3})[\s\S]*?(\d+\.\d{2})"
    result = findall(regex, string)

    if result is None:
        raise ValueError("No invoice data found in a text string")

    return result
