from src.tools.extractor import (
    read_excel_file,
    read_text_from_pdf,
    extract_data_from_string,
)
from src.tools.exporter import write_reconciliation_report_to_csv
# from src.tools.transformer import (
#    transform_invoice_string_data_to_df,
#    get_necessary_columns_from_df,
# )
# from src.handlers.constants import DATA_DIR

from pandas import DataFrame


def handle_read_file(file_path: str) -> str | DataFrame | list[str]:
    if file_path.endswith(".xlsx"):
        return read_excel_file(file_path, sheet="test")

    elif file_path.endswith(".pdf"):
        string_from_pdf = read_text_from_pdf(file_path)
        return extract_data_from_string(string_from_pdf)
    else:
        raise ValueError(f"File type not supported: {file_path}")


def handle_write_csv_file(dataframe: DataFrame, output_file_path: str) -> None:
    write_reconciliation_report_to_csv(dataframe, output_file_path)


def handle_write_to_db():
    """Zapis tableki do bazy"""
    pass
