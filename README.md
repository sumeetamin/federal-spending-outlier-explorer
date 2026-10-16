# Federal Spending Outlier Explorer

Rank unusual federal award amounts for analyst review with a reproducible Isolation Forest baseline.

> **Portfolio prototype.** Source code is provided; no benchmark results are claimed until you run it on the cited data and record the output.

## Use case

Rank unusual federal award amounts for analyst review with a reproducible Isolation Forest baseline. The CLI consumes local files, emits reproducible reports, and keeps data out of the repository.

## Data and provenance

[USAspending.gov public award data and download documentation](https://www.usaspending.gov/federal-spending-guide). A filtered USAspending award CSV with an obligation amount column; optionally include agency and award type. Source files are not bundled. Respect source terms and cite the dataset when publishing results.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
# Download/prepare the source data locally, then run:
python main.py --input data/awards.csv --amount federal_action_obligation --group awarding_agency_name --out outputs
```

## Outputs

Generated results are saved under `outputs/`; file names and metrics are printed or documented by the CLI. The repository excludes downloaded data and artifacts.

## Evaluation and operating notes

An anomaly score identifies records unlike the selected reference population. It is not a fraud, waste, or abuse finding; interpret only after validating data definitions, award types, and periods.

For production use, add a frozen reference period, out-of-time evaluation, monitoring ownership, and a documented rollback or escalation path. This project is a local baseline, not a deployed service.

## License

No code license file is included yet. Third-party data remains subject to its source terms.
