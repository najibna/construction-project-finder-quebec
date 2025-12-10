"""Find open construction projects in Montreal worth at least $5 million.

How to run:
    python -m pip install -r requirements.txt
    python app.py

Input:  projects.csv
Output: opportunities.csv  (a spreadsheet of the matches)
        projects.db        (the same matches, in a small local database)
"""

from pathlib import Path
import sqlite3

import pandas as pd

# Folder that holds this script, the input CSV, and the output files.
HERE = Path(__file__).resolve().parent

# Keep a project when its value is at least this many Canadian dollars.
MIN_VALUE_CAD = 5_000_000


def load_projects():
    """Read the project list from projects.csv."""
    # project_id stays text so leading zeros are not dropped.
    return pd.read_csv(HERE / "projects.csv", dtype={"project_id": str})


def clean_projects(projects):
    """Make city, value, and bid date usable, then drop duplicate projects."""
    projects = projects.copy()

    # Blank cities become an empty string. Extra spaces are removed.
    projects["city"] = projects["city"].fillna("").str.strip()

    # "errors='coerce'" turns a bad number or date into a blank (NaN)
    # instead of crashing. Blank rows fail the filter later.
    projects["value_cad"] = pd.to_numeric(projects["value_cad"], errors="coerce")
    projects["bid_date"] = pd.to_datetime(projects["bid_date"], errors="coerce")

    # The same project_id can appear twice in a feed. Keep the first copy.
    return projects.drop_duplicates(subset=["project_id"])


def find_opportunities(projects):
    """Keep Montreal projects of $5M+ whose bid date is today or later."""
    today = pd.Timestamp.today().normalize()

    in_montreal = projects["city"].str.contains(
        "montreal|montréal", case=False, regex=True
    )
    big_enough = projects["value_cad"] >= MIN_VALUE_CAD
    still_open = projects["bid_date"] >= today

    matches = projects[in_montreal & big_enough & still_open]
    # Largest projects first.
    return matches.sort_values("value_cad", ascending=False)


def save_results(results):
    """Write the matches to a CSV file and a SQLite database."""
    results.to_csv(HERE / "opportunities.csv", index=False)

    with sqlite3.connect(HERE / "projects.db") as connection:
        # Replace the table each run so old matches do not linger.
        results.to_sql("opportunities", connection, if_exists="replace", index=False)


def main():
    projects = load_projects()
    projects = clean_projects(projects)
    results = find_opportunities(projects)
    save_results(results)

    print(f"Found {len(results)} open Montreal opportunities worth at least $5M.")
    print(results[["name", "city", "value_cad", "bid_date"]].to_string(index=False))
    print("Saved to opportunities.csv and projects.db")


if __name__ == "__main__":
    main()
