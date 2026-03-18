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

from pandas import DataFrame
from pathlib import Path


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
