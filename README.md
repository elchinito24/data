# Data Date Conversion Script

This repository contains a Python script to convert date columns in `data.csv` from object type to datetime format.

## Overview

The script `convert_dates.py` processes a large CSV file (435K+ rows) and converts two date columns:

1. **`sampling_date`**: Extracts the pattern `M\d{6}` (e.g., "M021990" from "February - M021990") and converts to `YYYY-MM-01` datetime format
2. **`date`**: Converts from string format `YYYY-MM-DD` to datetime

## Requirements

- Python 3.x
- pandas

Install dependencies:
```bash
pip install pandas
```

## Usage

Run the script:
```bash
python3 convert_dates.py
```

The script will:
- Read `data.csv` in chunks of 50,000 rows for memory efficiency
- Process both date columns with error handling (`errors='coerce'`)
- Save the processed data to `data_processed.csv`
- Display a summary of conversions (successful/failed)
- Show the final data types
- Print the first 10 rows as a sample

## Output Example

```
Processing data.csv...
Reading in chunks of 50000 rows

Processing chunk 1 (50000 rows)...
Processing chunk 2 (50000 rows)...
...

============================================================
CONVERSION SUMMARY
============================================================
Total rows processed: 435,742

sampling_date column:
  ✓ Successful conversions: 21,994
  ✗ Failed conversions: 413,745

date column:
  ✓ Successful conversions: 435,735
  ✗ Failed conversions: 0

============================================================
FINAL DATA TYPES
============================================================
sampling_date    datetime64[ns]
date             datetime64[ns]
...
```

## Reading the Processed File

When reading `data_processed.csv`, specify the datetime columns for proper parsing:

```python
import pandas as pd

# Read with automatic datetime parsing
df = pd.read_csv('data_processed.csv', 
                 parse_dates=['sampling_date', 'date'],
                 encoding='latin-1')

print(df.dtypes)
# sampling_date    datetime64[ns]
# date             datetime64[ns]
```

## Notes

- The `sampling_date` column in the original data has multiple formats. Only rows with the `M\d{6}` pattern are successfully converted. Other formats are coerced to NaT (Not a Time).
- The script handles large files efficiently by processing in chunks.
- The encoding `latin-1` is used to handle special characters in the data.
- The output file `data_processed.csv` is excluded from version control via `.gitignore`.
