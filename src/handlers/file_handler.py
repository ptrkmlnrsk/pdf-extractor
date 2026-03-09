import pdfplumber
import pandas as pd


def read_excel_file(filename: str, sheet: str) -> pd.DataFrame:
    return pd.read_excel(filename, sheet_name=sheet, engine="xlrd")


# TODO zainstalowac te paczke xlrd


def read_text_from_pdf(file_name: str) -> str:
    with pdfplumber.open(file_name) as pdf_obj:
        text_list = ""

        for page in pdf_obj.pages:
            text_list = page.extract_text()

        return text_list


if __name__ == "__main__":
    # pdf = read_pdf_file(file_name="D:\\repos\\pdf-extractor\\data\\transactions.pdf")
    file_path = "transactions.pdf"
    text_from_pdf = read_text_from_pdf(file_name=file_path)
    print(text_from_pdf)

    transactions_data = read_excel_file(file_path, sheet="Transactions")
    print(transactions_data)
