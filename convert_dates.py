#!/usr/bin/env python3
r"""
Script to convert date columns in data.csv from object type to datetime.

Requirements:
1. sampling_date: Extract M\d{6} pattern and convert to YYYY-MM-01 format
2. date: Convert YYYY-MM-DD string to datetime
"""

import pandas as pd
import sys


def convert_sampling_date(df):
    r"""
    Convert sampling_date column to datetime format.
    
    Extracts pattern M\d{6} (e.g., M021990 from "February - M021990")
    and converts to YYYY-MM-01 format.
    
    Args:
        df: DataFrame with sampling_date column
        
    Returns:
        DataFrame with converted sampling_date column
    """
    # Ensure sampling_date is text
    df['sampling_date'] = df['sampling_date'].astype(str)
    
    # Extract the part like "M021990" from any text
    df['code'] = df['sampling_date'].str.extract(r'(M\d{6})')
    
    # Extract month (positions 1-3)
    df['month'] = df['code'].str[1:3].astype(float)
    
    # Extract year (positions 3-7)
    df['year'] = df['code'].str[3:7].astype(float)
    
    # Create date in YYYY-MM-01 format
    df['sampling_date'] = pd.to_datetime(
        df['year'].astype('Int64').astype(str) + '-' +
        df['month'].astype('Int64').astype(str) + '-01',
        format='%Y-%m-%d',
        errors='coerce'
    )
    
    # Remove temporary columns
    df = df.drop(columns=['code', 'month', 'year'])
    
    return df


def convert_date(df):
    """
    Convert date column to datetime format.
    
    Args:
        df: DataFrame with date column
        
    Returns:
        DataFrame with converted date column
    """
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df


def main():
    """Main function to process the CSV file."""
    input_file = 'data.csv'
    output_file = 'data_processed.csv'
    chunk_size = 50000  # Process in chunks for large files
    
    print(f"Processing {input_file}...")
    print(f"Reading in chunks of {chunk_size} rows\n")
    
    # Track statistics
    total_rows = 0
    sampling_date_success = 0
    sampling_date_failed = 0
    date_success = 0
    date_failed = 0
    
    # Process file in chunks
    chunks = []
    for chunk_num, chunk in enumerate(pd.read_csv(input_file, chunksize=chunk_size, encoding='latin-1'), 1):
        print(f"Processing chunk {chunk_num} ({len(chunk)} rows)...")
        
        # Store original non-null counts
        sampling_date_before = chunk['sampling_date'].notna().sum()
        date_before = chunk['date'].notna().sum()
        
        # Convert columns
        chunk = convert_sampling_date(chunk)
        chunk = convert_date(chunk)
        
        # Count successful conversions
        sampling_date_after = chunk['sampling_date'].notna().sum()
        date_after = chunk['date'].notna().sum()
        
        sampling_date_success += sampling_date_after
        sampling_date_failed += (sampling_date_before - sampling_date_after)
        date_success += date_after
        date_failed += (date_before - date_after)
        
        total_rows += len(chunk)
        chunks.append(chunk)
    
    # Combine all chunks
    print("\nCombining chunks...")
    data = pd.concat(chunks, ignore_index=True)
    
    # Save processed data
    print(f"\nSaving to {output_file}...")
    data.to_csv(output_file, index=False)
    
    # Print summary
    print("\n" + "="*60)
    print("CONVERSION SUMMARY")
    print("="*60)
    print(f"Total rows processed: {total_rows:,}")
    print(f"\nsampling_date column:")
    print(f"  ✓ Successful conversions: {sampling_date_success:,}")
    print(f"  ✗ Failed conversions: {sampling_date_failed:,}")
    print(f"\ndate column:")
    print(f"  ✓ Successful conversions: {date_success:,}")
    print(f"  ✗ Failed conversions: {date_failed:,}")
    
    # Print data types
    print("\n" + "="*60)
    print("FINAL DATA TYPES")
    print("="*60)
    print(data.dtypes.to_string())
    
    # Print sample of first 10 rows
    print("\n" + "="*60)
    print("FIRST 10 ROWS (SAMPLE)")
    print("="*60)
    print(data.head(10).to_string())
    
    print(f"\n✓ Processing complete! Output saved to {output_file}")


if __name__ == "__main__":
    main()
