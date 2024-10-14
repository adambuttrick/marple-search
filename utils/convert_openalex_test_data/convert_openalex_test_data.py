import csv
import requests
import argparse
import logging


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Retrieve ROR IDs and enhance CSV file')
    parser.add_argument('-i', '--input_file',
                        help='Path to the input CSV file')
    parser.add_argument('-o', '--output_file',
                        default='converted.csv', help='Path to the output CSV file')
    return parser.parse_args()


def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)


def retrieve_ror_ids(institution_ids):
    if not institution_ids or institution_ids == "-1":
        return []
    ror_ids = []
    ids = [id.strip() for id in institution_ids.strip(
        '[]').split(',') if id.strip() != "-1"]
    for id in ids:
        api_url = f"https://api.openalex.org/institutions/I{id}"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            ror_id = data.get("ror")
            if ror_id:
                ror_ids.append(ror_id)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error retrieving ROR ID for institution ID {id}: {e}")
    return list(set(ror_ids))


def write_enhanced_csv(file_path, data):
    fieldnames = list(data[0].keys()) + ['ror_ids']
    with open(file_path, 'w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            institution_ids = row.get("labels")
            ror_ids = retrieve_ror_ids(institution_ids)
            row['ror_ids'] = '; '.join(ror_ids) if ror_ids else None
            writer.writerow(row)


def main():
    logging.basicConfig(level=logging.INFO)
    args = parse_arguments()
    data = read_csv(args.input_file)
    write_enhanced_csv(args.output_file, data)
    logging.info(f"File written to {args.output_file}")


if __name__ == '__main__':
    main()
