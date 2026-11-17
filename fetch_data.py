""""Fetch a reproducible bounded USAspending.gov FY2025 award sample."""
import csv
import time
from pathlib import Path
import requests

URL = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
FIELDS = ["Award ID", "Recipient Name", "Award Amount", "Start Date", "Awarding Agency", "Awarding Sub Agency", "Description"]
OUT = Path("data/awards.csv")

def main():
    rows = []
    for page in range(1, 11):
        payload = {
            "filters": {"time_period": [{"start_date": "2024-10-01", "end_date": "2025-09-30"}],
                        "award_type_codes": ["A", "B", "C", "D"]},
            "fields": FIELDS, "page": page, "limit": 100,
            "sort": "Award Amount", "order": "desc", "subawards": False,
        }
        response = requests.post(URL, json=payload, timeout=60)
        response.raise_for_status()
        rows.extend(response.json().get("results", []))
        time.sleep(0.2)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    mapping = {"source_internal_id": "internal_id", "award_id": "Award ID", "recipient_name": "Recipient Name",
               "award_amount": "Award Amount", "start_date": "Start Date", "awarding_agency_name": "Awarding Agency",
               "awarding_sub_agency": "Awarding Sub Agency", "description": "Description"}
    with OUT.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(mapping))
        writer.writeheader()
        for row in rows:
            writer.writerow({dst: row.get(src) for dst, src in mapping.items()})
    print(f"Wrote {len(rows)} rows to {OUT}. This is a top-award sample, not a representative draw.")

if __name__ == "__main__":
    main()

