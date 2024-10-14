# Crossref Marple ROR Predictor

Uses Crossref's Marple API to match ROR IDs to affiliation strings.

## Installation
```
pip install -r requirements.txt
```

## Usage
```
python marple_search.py -i <input_file.csv> -o <output_file.csv> [-s <strategy>] [-v]
```

Arguments:
- `-i`, `--input`: Input CSV file (required)
- `-o`, `--output`: Output CSV file (default: 'ror-affiliation_results.csv')
- `-s`, `--strategy`: Matching strategy ('affiliation-single-search' or 'affiliation-multi-search', default: 'affiliation-single-search')
- `-v`, `--verbose`: Enable verbose logging

The input CSV file should contain an 'affiliation' column with the affiliation strings to be processed.

## Output

The script outputs a CSV file with the following additional columns:

- `predicted_ror_id`: Predicted ROR ID(s)
- `prediction_score`: Confidence score(s) for the prediction(s)
- `match_type`: 'match' or 'no_match'

## Logging

The script generates a log file with the naming format `YYYYMMDD_HHMMSS_ror-affiliation.log`.