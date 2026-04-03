import argparse
from src.services.invoice_service import InvoiceService
from src.services.exporter import write_reconciliation_report_to_csv


def main():
    parser = argparse.ArgumentParser(description="Invoice reconciliation tool")

    parser.add_argument("--xlsx", required=True, help="Excel file path")
    parser.add_argument("--sheet", help="Excel sheet name")
    parser.add_argument("--pdf", required=True, help="PDF file path")
    parser.add_argument("--output", required=True, help="Output CSV path")

    args = parser.parse_args()

    service = InvoiceService()
    result = service.run_reconciliation(args.xlsx, args.pdf, sheet_name=args.sheet)

    write_reconciliation_report_to_csv(result, args.output)


if __name__ == "__main__":
    main()
