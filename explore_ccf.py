#!/usr/bin/env python3
"""
Script to explore the Adobe CCF Excel file structure
"""
import pandas as pd
import xlrd
import sys

def explore_excel_file(file_path):
    """Explore the structure of the Excel file"""
    print(f"\n{'='*80}")
    print(f"Exploring: {file_path}")
    print(f"{'='*80}\n")

    # Try using xlrd for .xls files
    try:
        workbook = xlrd.open_workbook(file_path)
        print(f"Number of sheets: {workbook.nsheets}")
        print(f"\nSheet names:")
        for i, sheet_name in enumerate(workbook.sheet_names()):
            sheet = workbook.sheet_by_index(i)
            print(f"  {i+1}. {sheet_name} ({sheet.nrows} rows, {sheet.ncols} columns)")

        print("\n" + "="*80)
        print("Exploring each sheet in detail...")
        print("="*80 + "\n")

        for sheet_name in workbook.sheet_names():
            sheet = workbook.sheet_by_name(sheet_name)
            print(f"\n--- Sheet: {sheet_name} ---")
            print(f"Dimensions: {sheet.nrows} rows x {sheet.ncols} columns")

            # Show first few rows to understand structure
            if sheet.nrows > 0:
                print("\nFirst 5 rows:")
                for row_idx in range(min(5, sheet.nrows)):
                    row_data = []
                    for col_idx in range(min(10, sheet.ncols)):  # Show first 10 columns
                        cell = sheet.cell(row_idx, col_idx)
                        value = str(cell.value)[:50]  # Limit length
                        row_data.append(value)
                    print(f"  Row {row_idx}: {row_data}")

                # Show header row if different
                if sheet.nrows > 1:
                    print("\nHeader row (Row 0):")
                    headers = []
                    for col_idx in range(sheet.ncols):
                        cell = sheet.cell(0, col_idx)
                        headers.append(str(cell.value)[:30])
                    print(f"  {headers}")

            print("\n" + "-"*80)

    except Exception as e:
        print(f"Error with xlrd: {e}")
        print("\nTrying with pandas...")

        try:
            # Try with pandas
            xls = pd.ExcelFile(file_path)
            print(f"Sheet names: {xls.sheet_names}")

            for sheet_name in xls.sheet_names:
                print(f"\n--- Sheet: {sheet_name} ---")
                df = pd.read_excel(file_path, sheet_name=sheet_name, nrows=5)
                print(f"Shape: {df.shape}")
                print("\nFirst few rows:")
                print(df.head())
                print("\nColumns:")
                print(df.columns.tolist())
        except Exception as e2:
            print(f"Error with pandas: {e2}")

if __name__ == "__main__":
    file_path = "adobe-ccf/Open_Source_CCF.xls"
    explore_excel_file(file_path)
