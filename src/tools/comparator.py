from pandas import DataFrame, Series, isna, concat


class Comparator:
    def __init__(self, df_xlsx: DataFrame, df_pdf: DataFrame):
        self.df_xlsx = df_xlsx
        self.df_pdf = df_pdf

    def build_invoices_ids(self) -> DataFrame:
        return DataFrame(
            {
                "invoice_id": concat(
                    [self.df_pdf["invoice_id"], self.df_xlsx["invoice_id"]]
                ).unique()
            }
        )

    def _merge_data_frames(self) -> DataFrame:
        invoice_ids = self.build_invoices_ids()
        data_merged = invoice_ids.merge(self.df_xlsx, how="left", on="invoice_id")
        data_merged = data_merged.merge(self.df_pdf, how="left", on="invoice_id")
        data_merged.rename(
            {"amount_x": "amount_xlsx", "amount_y": "amount_pdf"},
            axis="columns",
            inplace=True,
        )
        return data_merged

    @staticmethod
    def _get_invoice_status(row: Series) -> str:
        is_xlsx_nan = isna(row["amount_xlsx"])
        is_pdf_nan = isna(row["amount_pdf"])
        not_xlsx_pdf_same = row["amount_xlsx"] != row["amount_pdf"]

        if is_xlsx_nan:
            return "Missing in Excel"
        elif is_pdf_nan:
            return "Missing in PDF"
        elif not_xlsx_pdf_same:
            return "Amount mismatch"
        else:
            return "OK"

    @staticmethod
    def _generate_invoice_status(merged_data: DataFrame) -> DataFrame:
        return merged_data.apply(Comparator._get_invoice_status, axis="columns")
