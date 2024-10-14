import csv
import logging
import argparse
import requests
from datetime import datetime
from urllib.parse import quote


def setup_logging(verbose):
    now = datetime.now()
    script_start = now.strftime("%Y%m%d_%H%M%S")
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(filename=f'{script_start}_ror-affiliation.log', level=log_level,
                        format='%(asctime)s %(levelname)s %(message)s')


def query_marple(affiliation, strategy, verbose):
    results = []
    try:
        base_url = "https://marple.research.crossref.org/match"
        params = {
            "task": "affiliation-matching",
            "input": quote(affiliation),
            "strategy": strategy
        }
        url = f"{base_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
        r = requests.get(url)
        api_response = r.json()
        if api_response["status"] == "ok":
            items = api_response["message"]["items"]
            for item in items:
                ror_id = item["id"]
                confidence = item["confidence"]
                results.append((ror_id, confidence))
                if verbose:
                    logging.debug(f"Crossref Marple match found for '{affiliation}': {ror_id} (confidence: {confidence})")
                break
        if not results and verbose:
            logging.debug(f"No Crossref Marple match found for '{affiliation}'")
    except Exception as e:
        logging.error(f'Error in Crossref Marple query: {affiliation} - {e}')
    return results


def parse_and_query(input_file, output_file, strategy, verbose):
    try:
        with open(input_file, 'r+', encoding='utf-8-sig') as f_in, open(output_file, 'w') as f_out:
            reader = csv.DictReader(f_in)
            fieldnames = reader.fieldnames + [
                "predicted_ror_id", "prediction_score", "match_type"
            ]
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                affiliation = row['affiliation']
                results = query_marple(affiliation, strategy, verbose)
                match_type = "match" if results else "no_match"
                if results:
                    predicted_ids = ";".join([r[0] for r in results])
                    prediction_scores = ";".join([str(r[1]) for r in results])
                else:
                    predicted_ids = None
                    prediction_scores = None
                row.update({
                    "predicted_ror_id": predicted_ids,
                    "prediction_score": prediction_scores,
                    "match_type": match_type
                })
                writer.writerow(row)
                if verbose:
                    logging.debug(f"Processed affiliation: {affiliation}, Match type: {match_type}")
    except Exception as e:
        logging.error(f'Error in parse_and_query: {e}')


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Return ROR affiliation matches for a given CSV file.')
    parser.add_argument('-i', '--input', help='Input CSV file', required=True)
    parser.add_argument('-o', '--output', help='Output CSV file',
                        default='ror-affiliation_results.csv')
    parser.add_argument('-s', '--strategy', help='Matching strategy',
                        choices=['affiliation-single-search',
                                 'affiliation-multi-search'],
                        default='affiliation-single-search')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose logging')
    return parser.parse_args()


def main():
    args = parse_arguments()
    setup_logging(args.verbose)
    logging.info("Starting affiliation parsing and querying...")
    parse_and_query(args.input, args.output, args.strategy, args.verbose)
    logging.info("Affiliation parsing and querying completed.")


if __name__ == '__main__':
    main()
