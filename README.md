# Federal Spending Outlier Explorer

A reproducible unsupervised baseline that ranks unusually large federal award records for human review. It does **not** identify fraud, waste, abuse, poor value, or procurement violations.

## Run on a bounded USAspending sample

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python fetch_data.py
python main.py --input data/awards.csv --amount award_amount --group awarding_agency_name --out outputs
```

`fetch_data.py` queries the official USAspending API for FY2025 activity and retrieves 10 pages (up to 1,000) of contract, grant, loan, and other financial assistance awards sorted by **total award amount**. Repeated API internal IDs are preserved in the local file; award IDs alone are not guaranteed unique. The bounded top-award sample is deliberately selected by amount and is not representative of federal spending. Award start dates span years outside FY2025 because the API period is an activity filter, not a filter on award start date. The query is not a sample of FY2025 obligations.

## Observed run (November 17, 2026)

The top-1,000 query returned 1,000 records with 1,000 API internal IDs, 991 distinct displayed award IDs, and 18 awarding agencies. Total award amounts ranged from $579 million to $51.3 billion (median $1.07 billion). On these already large awards, Isolation Forest flagged 10 records (1%) for review; flagged amounts were $3.28 billion to $51.3 billion. These counts describe this selected query only. No row-level data, recipient details, or review queue are committed.

The API request and methodology are recorded in `fetch_data.py`; `reports/benchmark.json` contains aggregate results and the local source CSV SHA-256 for provenance. The live API can change, so fetching again may produce different records and metrics.

## Method and limits

- Features: log-transformed total award amount and within-sample awarding-agency frequency. The model is fitted to the same bounded sample it ranks.
- Isolation Forest uses 300 trees, a fixed random seed, and a 1% contamination setting. That setting selects a review queue size; it is not an estimated real-world anomaly rate.
- No labeled fraud or outcome data are available here. There is no precision/recall estimate, causal conclusion, or evidence that any flagged award is improper.
- The source query selects only the largest records, creating strong selection bias. The agency frequency feature is also fitted on this one sample. Use this as a code and workflow demonstration only.
- Before operational use, define the decision question and population, include valid spending denominators and award actions, freeze training/reference periods, evaluate with adjudicated labels and human review, and assess agency/award-type coverage and false-positive burden.

## Source and reuse

Data source: [USAspending.gov API documentation](https://api.usaspending.gov/docs/endpoints/) and [spending by award endpoint](https://api.usaspending.gov/docs/endpoints/api/search/spending_by_award/). The API source data are not redistributed here. Review USAspending source terms and field definitions before reuse.

No code license file is included yet. Third-party data remain subject to their source terms.

