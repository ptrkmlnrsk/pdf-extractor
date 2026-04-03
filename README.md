# Invoice Reconciliation: PDF vs Excel

A Python application for reconciling financial transaction data between PDF documents and Excel files.
The project extracts, transforms, and compares invoice data, identifying inconsistencies such as missing records and mismatched amounts.

## Architecture

The project is structured into modular layers:

- **tools/** – core business logic:
  - data extraction (PDF, Excel),
  - transformation and normalization,
  - comparison logic (reconciliation),
- **db/** – database configuration and session management,
- **models/** – data models representing processed records,
- **queries/** – database query logic,
- **handlers/** – file handling utilities,
- **tests/** – unit and integration tests.

The application follows a pipeline approach:

1. Load data from PDF and Excel
2. Parse and normalize records
3. Compare datasets
4. Store or export reconciliation results

## Features

- loads invoice data from Excel and PDF-unstructured file,
- merges records by `invoice_number`,
- compares invoice amounts,
- assigns comparison status:
  - `OK`
  - `Missing in Excel`
  - `Missing in PDF`
  - `Amount mismatch`
- contains module that saves report to SQLite DB, currently in development.

## Project structure

```bash
pdf-extractor/
├── data/
├── example_data/
├── src/
│   ├── db/
│   ├── handlers/
│   ├── models/
│   ├── queries/
│   ├── services/
│   └── config.py
├── tests/
├── .gitignore
├── .pre-commit-config.yaml
├── bandit.yml
├── main.py
└── README.md
```

## Example usage

Run the app using example files:
```bash
 python main.py --xlsx ./example_data/transactions.xlsx --sheet Transactions --pdf ./example_data/transactions.pdf --output ./example_data/example_output_file
```
## Example output




