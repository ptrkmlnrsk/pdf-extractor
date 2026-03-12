import pandas as pd


class Comparator:
    def __init__(self, df_xlsx: pd.DataFrame, df_pdf: pd.DataFrame):
        self.df_xlsx = df_xlsx
        self.df_pdf = df_pdf

    def build_invoices_ids(self) -> None:
        return pd.DataFrame(
            {
                "invoice_id": pd.concat(
                    [self.df_pdf["invoice_id"], self.df_xlsx["invoice_id"]]
                ).unique()
            }
        )

    def _merge_data_frames(self) -> None:
        invoice_ids = self.build_invoices_ids()
        data_merged = invoice_ids.merge(self.df_xlsx, how="left", on="invoice_id")
        data_merged = data_merged.merge(self.df_pdf, how="left", on="invoice_id")
        data_merged.rename(
            {"amount_x": "amount_xlsx", "amount_y": "amount_pdf"},
            axis="columns",
            inplace=True,
        )
        return data_merged

    # TODO match case
    @staticmethod
    def _get_status(row: pd.Series) -> str:
        # zmienne moga tez przechowywac warunki
        is_xlsx_nan = pd.isna(row["amount_xlsx"])
        is_pdf_nan = pd.isna(row["amount_pdf"])
        not_xlsx_pdf_same = row["amount_xlsx"] != row["amount_pdf"]

        if is_xlsx_nan:
            return "Missing in Excel"
        elif is_pdf_nan:
            return "Missing in PDF"
        elif not_xlsx_pdf_same:
            return "Amount mismatch"
        else:
            return "OK"

    def _generate_status(self) -> None:
        # self.merged_data["status"]
        merged_data = self.merge_data_frames()
        return merged_data.apply(self._get_status, axis="columns")
