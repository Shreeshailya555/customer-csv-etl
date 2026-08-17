
import pandas as pd
from pathlib import Path
import logging

# THIS LOGGING IS FOR SHOW THE DATE,TIME STAMP IN THE CODE MSG EXECUTION

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# EXTRACT MACHINE



def extract():
    try:
        project_root = Path(__file__).resolve().parents[2]
        input_path = project_root / "src" / "data" / "raw" / "customers.csv"

        df = pd.read_csv(input_path)

        logging.info("Data extracted successfully!")

        print("Rows:", len(df))
        print("Columns:", len(df.columns))

        return df

    except Exception as e:
        logging.error("Data extraction failed: %s", e)
        return None






# TRANSFORM MACHINE

def transform(df):
 try:
    logging.info("Starting transformation")


    # Standardize email addresses
    df["email"] = df["email"].str.lower().str.strip()

    # Remove duplicate customers
    df = df.drop_duplicates(
        subset=["email", "phone"],
        keep="first"
    )

    # Handle missing values
    df["phone"] = df["phone"].fillna("NOT_AVAILABLE")
    df["email"] = df["email"].fillna("NOT_AVAILABLE")
    df["age"] = df["age"].fillna(df["age"].median())

    # Fix invalid ages
    invalid_age = (df["age"] < 18) | (df["age"] > 100)

    median_age = df.loc[~invalid_age, "age"].median()

    df.loc[invalid_age, "age"] = median_age

    logging.info("Transformation completed")

    return df

 except Exception as e:
     logging.error("Data transformation failed: %s", e)
     return None

# VALIDATE MACHINE


def validate(df):
  try:
    logging.info("Starting validation")


#   VALIDATE MISSING VALUES

    missing_values = df.isnull().sum()

    print("\nMissing values:")
    print(missing_values)

#   VALIDATE DUPLICATE COUNTS

    duplicate_count = df.duplicated(
        subset=["email", "phone"]
    ).sum()

    print("\nDuplicate customers:", duplicate_count)


#   Validate invalid ages

    invalid_age_count = (
            (df["age"] < 18) | (df["age"] > 100)
    ).sum()
    print("\nInvalid ages:", invalid_age_count)

    logging.info("Validation completed")

    return df
  except Exception as e:
    logging.error("Validation failed: %s", e)
    return None

# LOAD MACHINE


def load(df):
 try:
    logging.info("Starting data load")

    project_root = Path(__file__).resolve().parents[2]
    output_path = project_root / "src" / "data" / "processed" / "customers_cleaned.csv"

    df.to_csv(output_path, index=False)

    logging.info("Data loaded successfully")

    print("\nCleaned data saved successfully!")
    print("Output file:", output_path)

 except Exception as e:
        logging.error("Data load failed: %s", e)
        return None

 return True

logging.info("Starting ETL pipeline")

df = extract()

if df is None:
    logging.error("ETL pipeline stopped because extraction failed.")
    exit()

df = transform(df)

if df is None:
    logging.error("ETL pipeline stopped because transformation failed.")
    exit()

print("\n--- Transformed Data Info ---")
print("Rows:", len(df))
print("Columns:", len(df.columns))

df = validate(df)

if df is None:
    logging.error("ETL pipeline stopped because validation failed.")
    exit()

load(df)

logging.info("ETL pipeline completed successfully")
