from pandas import DataFrame


def write_reconciliation_report_to_csv(
    reconciled_data: DataFrame, output_file_path: str
):
    try:
        reconciled_data.to_csv(
            f"{output_file_path}.csv", sep=",", index=False, header=True
        )
    except Exception as e:
        print(e)
