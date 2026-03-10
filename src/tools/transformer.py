import pandas as pd


def transform_invoice_string_data_to_df(extracted_data: list) -> pd.DataFrame:
    transformed_df = pd.DataFrame(extracted_data, columns=["invoice_id", "amount"])
    transformed_df["amount"] = transformed_df["amount"].astype(float)

    return transformed_df


def get_necessary_columns_from_df(full_df: pd.DataFrame) -> pd.DataFrame:
    narrowed_df = full_df[["InvoiceNo", "Amount"]]

    return narrowed_df.rename(
        columns={"InvoiceNo": "invoice_id", "Amount": "amount"}, inplace=True
    )
