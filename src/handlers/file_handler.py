from pandas import DataFrame


def write_reconciliation_report(reconciled_data: DataFrame, file_name: str):
    reconciled_data.to_csv(f"{file_name}.csv", sep=",", index=False, header=True)
