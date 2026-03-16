import pytest
import pandas as pd

from src.tools.extractor import (
    read_text_from_pdf,
    read_excel_file,
    extract_data_from_string,
)


def test_if__excel_filepath_is_empty():
    with pytest.raises(ValueError):
        read_excel_file("", sheet="test")


# TODO pytanie czy ten read_text_from_pdf nie powinien mieć innej nazwy read_pdf_file
# TODO zrobić brancha


def test_read_text_from_pdf():
    assert isinstance(read_text_from_pdf(filepath="./data/transactions9.pdf"), str)


def test_read_excel_file():
    df = read_excel_file(filepath="./data/transactions.xlsx", sheet="Transactions")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


@pytest.mark.parametrize(
    "fake_string_input, expected_list",
    [
        ("Invoice Number: INV001, Amount paid -> 100.00 PLN", [("INV001", "100.00")]),
        ("INV657 150.00 PLN", [("INV657", "150.00")]),
        (
            "Invoice ID = INV004 ; Value = 500.00 PLN ; Vendor = NewVendor",
            [("INV004", "500.00")],
        ),
    ],
)
def test_extract_data_from_string(fake_string_input, expected_list):
    assert extract_data_from_string(fake_string_input) == expected_list


def test_extract_data_from_string_empty():
    assert extract_data_from_string("") == []
