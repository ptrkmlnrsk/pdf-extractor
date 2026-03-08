import pytest
import pandas as pd

from src.handlers.file_handler import read_text_from_pdf, read_excel_file


@pytest.mark.file_handler_pdf
def test_reading_text_from_pdf_file():
    filepath = "./data/transactions.pdf"
    assert isinstance(read_text_from_pdf(filepath), str)

@pytest.mark.file_handler_excel
def test_reading_excel_file():
    filepath = "./data/transactions.xlsx"
    sheet='Transactions'
    df = read_excel_file(filepath, sheet)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty