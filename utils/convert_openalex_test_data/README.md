# OpenAlex Test Data Converter

Converts a CSV file containing OpenAlex institution IDs by retrieving them from the API and adding the corresponding ROR IDs.


## Usage

```
python convert_openalex_test_data.py -i <input_file.csv> [-o <output_file.csv>]
```

Arguments:
- `-i`, `--input_file`: Path to the input CSV file (required)
- `-o`, `--output_file`: Path to the output CSV file (default: 'converted.csv')

The input CSV file should contain a 'labels' column with OpenAlex institution IDs.

## Output

An enhanced CSV file with an additional 'ror_ids' column containing the retrieved ROR IDs.