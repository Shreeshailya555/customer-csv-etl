# Customer CSV ETL Pipeline

A Python-based ETL pipeline that extracts customer data from a CSV file, cleans and transforms the data, validates the results, and loads the final dataset into a processed CSV file.

## Project Overview

This project demonstrates a basic ETL workflow using **Python and Pandas**.

The pipeline follows four main stages:

```text
customers.csv
     │
     ▼
  EXTRACT
     │
     ▼
 TRANSFORM
     │
     ▼
  VALIDATE
     │
     ▼
    LOAD
     │
     ▼
customers_cleaned.csv
```

## Technologies Used

* Python
* Pandas
* pathlib
* logging
* Git & GitHub

## Project Structure

```text
customer-csv-etl/
│
├── src/
│   ├── data/
│   │   ├── processed/
│   │   │   └── customers_cleaned.csv
│   │   └── raw/
│   │       └── customers.csv
│   │
│   └── etl/
│       └── main.py
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## ETL Process

### 1. Extract

The pipeline reads customer data from:

```text
src/data/raw/customers.csv
```

The input dataset contains **12 rows and 8 columns**.

The extraction step also logs successful completion and reports the number of rows and columns.

### 2. Transform

The transformation stage cleans and standardizes the customer data.

The following operations are performed:

* Converts email addresses to lowercase.
* Removes unnecessary whitespace from email addresses.
* Removes duplicate customers using email and phone.
* Replaces missing phone numbers with `NOT_AVAILABLE`.
* Replaces missing email addresses with `NOT_AVAILABLE`.
* Replaces missing ages with the median age.
* Detects ages below 18 or above 100.
* Replaces invalid ages with the median of valid ages.

### Why does the output contain 11 rows?

The input dataset contains **12 rows**.

Two records represent the same customer based on the duplicate-checking fields:

```text
email + phone
```

The duplicate record is removed during transformation.

Therefore:

```text
Input rows     = 12
Duplicate rows = 1
Final rows     = 11
```

The final transformed dataset contains **11 rows and 8 columns**.

## 3. Validate

The validation stage checks the transformed data for:

* Missing values
* Duplicate customers
* Invalid ages

For the current dataset, the validation results are:

```text
Missing values:
customer_id          0
name                 0
email                0
phone                0
city                 0
age                  0
registration_date    0
total_spent          0

Duplicate customers: 0
Invalid ages: 0
```

## 4. Load

After successful validation, the cleaned data is saved to:

```text
src/data/processed/customers_cleaned.csv
```

The CSV is written with `index=False` so that the Pandas DataFrame index is not stored as an additional column in the output file.

## Logging

The pipeline uses Python's built-in `logging` module to track the execution of each ETL stage.

Example:

```text
INFO - Starting ETL pipeline
INFO - Data extracted successfully!
INFO - Starting transformation
INFO - Transformation completed
INFO - Starting validation
INFO - Validation completed
INFO - Starting data load
INFO - Data loaded successfully
INFO - ETL pipeline completed successfully
```

## Error Handling

Each major ETL stage contains error handling.

### Extraction

If the input CSV cannot be found or read, the pipeline logs the extraction error and stops.

### Transformation

If an error occurs while transforming the data, the pipeline logs the transformation error and stops before validation.

### Validation

If validation fails, the pipeline stops before loading the data.

### Load

If the cleaned data cannot be written to the processed-data directory, the pipeline logs the load error.

This prevents the pipeline from reporting a successful execution when one of the ETL stages has failed.

## Installation

Clone the repository:

```bash
git clone <your-github-repository-url>
cd customer-csv-etl
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Run the Pipeline

Run the following command from the project root:

```bash
python src/etl/main.py
```

After a successful execution, the cleaned dataset will be available at:

```text
src/data/processed/customers_cleaned.csv
```

## Example Output

A successful ETL pipeline execution produces output similar to:

```text
INFO - Starting ETL pipeline
INFO - Data extracted successfully!

Rows: 12
Columns: 8

INFO - Starting transformation
INFO - Transformation completed

Rows: 11
Columns: 8

INFO - Starting validation
INFO - Validation completed

Missing values:
customer_id          0
name                 0
email                0
phone                0
city                 0
age                  0
registration_date    0
total_spent          0

Duplicate customers: 0
Invalid ages: 0

INFO - Starting data load
INFO - Data loaded successfully

Cleaned data saved successfully!
Output file: src/data/processed/customers_cleaned.csv

INFO - ETL pipeline completed successfully
```

## Future Improvements

Possible future enhancements include:

* Database loading instead of CSV output
* Automated unit tests
* Configuration through environment variables
* Scheduled ETL execution
* Cloud storage integration
* Data quality reporting
* Azure Data Factory or Databricks integration

## License

This project is licensed under the MIT License.
