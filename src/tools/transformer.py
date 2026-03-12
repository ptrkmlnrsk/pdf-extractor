import pandas as pd

COLUMNS_TO_RENAME = {
    "InvoiceNo": "invoice_id",
    # "Amount": "amount"
}
# ten słownik to mapper


def transform_invoice_string_data_to_df(extracted_data: list) -> pd.DataFrame:
    transformed_df = pd.DataFrame(extracted_data, columns=["invoice_id", "amount"])
    transformed_df["amount"] = transformed_df["amount"].astype(float)

    return transformed_df


# TODO


def get_necessary_columns_from_df(full_df: pd.DataFrame) -> pd.DataFrame:
    narrowed_df = full_df[list(COLUMNS_TO_RENAME.keys())]

    return narrowed_df.rename(columns=COLUMNS_TO_RENAME, inplace=True)
