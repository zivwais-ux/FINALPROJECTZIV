# Preparation Log for clean_data.csv

## Source
- Raw data file: /home/user/FINALPROJECTZIV/data/raw/E Commerce Dataset.xlsx
- Sheet used: "E Comm"
- Dataset dimensions: 5630 rows, 20 columns

## Steps
- Read the raw data from the specified Excel sheet "E Comm".
- Exported the data as clean_data.csv to /home/user/FINALPROJECTZIV/artifacts/latest/crew1 without any modification.
- Re-read the exported CSV file.
- Compared the CSV content cell by cell against the original raw data.

## Decisions
- Missing values were preserved exactly as in the raw data (no imputation or filling).
- Category spellings were kept exactly as in the raw data (no merging or renaming).
- Outliers were retained without any clipping or removal.
- No changes were made to any data values during export.

## Verification
- The exported CSV file is identical to the raw data cell by cell.
- No differences were found between the raw data and the exported CSV.
- SHA256 checksum of clean_data.csv: e0c951d4a9a94a650ff514da4c0152b473b1ab026aeddf0662ced46e5f847019

## Output
- File path: /home/user/FINALPROJECTZIV/artifacts/latest/crew1/clean_data.csv
- This file is a faithful copy of the raw data with all missing values, category spellings, and outliers preserved exactly.