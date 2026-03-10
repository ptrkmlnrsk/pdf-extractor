import pandas as pd


# TODO df1,df2 jako pola klasy
def get_invoices_ids(df_xlsx: pd.DataFrame, df_pdf: pd.DataFrame) -> pd.DataFrame:
    invoices_ids = pd.DataFrame(
        {
            "invoice_id": pd.concat(
                [df_pdf["invoice_id"], df_xlsx["invoice_id"]]
            ).unique()
        }
    )
    return invoices_ids


def merge_data_frames(
    df_xlsx: pd.DataFrame, df_pdf: pd.DataFrame, invoices_ids: pd.DataFrame
) -> pd.DataFrame:
    data_merged = invoices_ids.merge(df_xlsx, how="left", on="invoice_id")
    data_merged = data_merged.merge(df_pdf, how="left", on="invoice_id")
    data_merged.rename(
        {"amount_x": "amount_xlsx", "amount_y": "amount_pdf"},
        axis="columns",
        inplace=True,
    )

    return data_merged


def _get_status(row):
    if pd.isna(row["amount_xlsx"]):
        return "Missing in Excel"
    elif pd.isna(row["amount_pdf"]):
        return "Missing in PDF"
    elif row["amount_xlsx"] != row["amount_pdf"]:
        return "Amount mismatch"
    else:
        return "OK"


def generate_status(merged_data: pd.DataFrame) -> pd.DataFrame:
    return merged_data.apply(_get_status, axis="columns")
