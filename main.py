import argparse
from src.tools.services import InvoiceService


def main():
    parser = argparse.ArgumentParser(description="Invoice reconciliation tool")

    parser.add_argument("--xlsx", required=True, help="Excel file path")
    parser.add_argument("--sheet", help="Excel sheet name")
    parser.add_argument("--pdf", required=True, help="PDF file path")
    parser.add_argument("--output", required=True, help="Output CSV path")

    args = parser.parse_args()
    service = InvoiceService()

    # df_xlsx = service.load_and_parse(args.xlsx, sheet=args.sheet)
    # df_pdf = service.load_and_parse(args.pdf)

    result = service.run_reconciliation(args.xlsx, args.pdf, sheet_name=args.sheet)

    from src.tools.exporter import write_reconciliation_report_to_csv

    write_reconciliation_report_to_csv(result, args.output)


if __name__ == "__main__":
    main()
