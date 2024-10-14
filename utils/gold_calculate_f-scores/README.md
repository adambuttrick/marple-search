# Gold ROR ID Evaluator

Calculates evaluation metrics for ROR ID predictions for OpenAlex's gold standard dataset.


## Usage

```
python gold_calculate_f_score_confusion_matrix.py -i <input_file.csv> [-o <output_file.csv>] [-m <metrics_file.csv>]
```

Arguments:
- `-i`, `--input`: Input CSV file (required)
- `-o`, `--output`: Output CSV file with classification results (default: '<input_file>_classified.csv')
- `-m`, `--metrics`: Metrics output CSV file (default: '<input_file>_metrics.csv')

The input CSV file should contain 'ror_ids' (true IDs) and 'predicted_ror_id' columns.

## Output

1. A classified CSV file with additional columns:
   - TP, FP, TN, FN (confusion matrix values)

2. A metrics CSV file with the following columns:
   - Dataset, Precision, Recall, F1 Score, F0.5 Score, Specificity

3. Console output of metrics for each dataset (gold_easy, gold_full, gold_hard, gold_random)

## Datasets

- gold_easy: Easier gold standard examples
- gold_hard: More challenging gold standard examples
- gold_full: Combination of gold_easy and gold_hard
- gold_random: Random sample of 200 entries from gold_full