import pandas as pd


class Comparator:
    def __init__(self, df_xlsx: pd.DataFrame, df_pdf: pd.DataFrame):
        self.df_xlsx = df_xlsx
        self.df_pdf = df_pdf
        self.merged_data = None
        self.invoice_ids = None

    def build_invoices_ids(self) -> None:
        self.invoice_ids = pd.DataFrame(
            {
                "invoice_id": pd.concat(
                    [self.df_pdf["invoice_id"], self.df_xlsx["invoice_id"]]
                ).unique()
            }
        )

    def merge_data_frames(self) -> None:
        if self.invoice_ids is None:
            raise ValueError(
                "No invoice ids provided. Create ids using build_invoices_ids()"
            )

        data_merged = self.invoice_ids.merge(self.df_xlsx, how="left", on="invoice_id")
        data_merged = data_merged.merge(self.df_pdf, how="left", on="invoice_id")
        data_merged.rename(
            {"amount_x": "amount_xlsx", "amount_y": "amount_pdf"},
            axis="columns",
            inplace=True,
        )
        self.merged_data = data_merged

    @staticmethod
    def _get_status(row: pd.Series) -> str:
        if pd.isna(row["amount_xlsx"]):
            return "Missing in Excel"
        elif pd.isna(row["amount_pdf"]):
            return "Missing in PDF"
        elif row["amount_xlsx"] != row["amount_pdf"]:
            return "Amount mismatch"
        else:
            return "OK"

    def generate_status(self) -> None:
        if self.merged_data is None:
            raise ValueError("No data provided.")

        self.merged_data["status"] = self.merged_data.apply(
            self._get_status, axis="columns"
        )
