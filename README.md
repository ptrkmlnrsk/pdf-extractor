# Invoice Reconciliation: PDF vs Excel

A Python application for reconciling financial transaction data between PDF documents and Excel files.
The project extracts, transforms, and compares invoice data, identifying inconsistencies such as missing records and mismatched amounts.

## 1. Architecture

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
4. Store or export reconciliation results in CSV file


## 2. Data flow

PDF / Excel → Extractor → Parser → Transformer → Comparator → Output / Database

## 3. Features

- loads invoice data from Excel and PDF-unstructured file,
- merges records by `invoice_number`,
- compares invoice amounts,
- assigns comparison status:
  - `OK`
  - `Missing in Excel`
  - `Missing in PDF`
  - `Amount mismatch`
- contains module that saves report to SQLite DB, currently in development

##4. Project structure

```bash
pdf-extractor/
├── data/
├── example_data/
├── src/
│   ├── db/              # database setup
│   ├── handlers/        # file handling utilities
│   ├── models/          # data models
│   ├── queries/         # database queries
│   ├── services/        # core processing logic
│   │   ├── base
│   │   ├── comparator.py
│   │   ├── extractor.py
│   │   ├── loaders.py
│   │   ├── parsers.py
│   │   ├── transformer.py
│   │   ├── exporter.py
│   │   └── invoice_service.py
│   └── config.py
├── tests/
├── .gitignore
├── .pre-commit-config.yaml
├── bandit.yml
├── main.py
├── requirements.txt
└── README.md
```

## 5. Example usage

Run the app using example files:
```bash
 python main.py --xlsx ./example_data/transactions.xlsx --sheet Transactions --pdf ./example_data/transactions.pdf --output ./example_data/example_output_file
```
## 7. Example output

```md
## Example output

| invoice_id | amount_xlsx  | amount_pdf | status            |
|------------|--------------|------------|-------------------|
| 001        | 100.00       | 100.00     | OK                |
| 002        | 200.00       | NaN        | Missing in PDF    |
| 003        | NaN          | 150.00     | Missing in Excel  |
```

## 8. Development tools

This project uses several tools to ensure code quality and security:

- **pre-commit** – runs automated checks before each commit
- **bandit** – scans the codebase for common security issues

### Setup

Install pre-commit hooks:

```bash
pre-commit install
```

Run pre-commit manually:

```bash
pre-commit run --all-files
