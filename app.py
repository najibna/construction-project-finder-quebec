"""Find open construction projects in Montreal worth at least $5 million."""

from pathlib import Path
import sqlite3

import pandas as pd

HERE = Path(__file__).resolve().parent

MIN_VALUE_CAD = 5_000_000


def load_projects():
    """Read the project list from projects.csv."""
    return pd.read_csv(HERE / "projects.csv")


def clean_projects(projects):
    """Make city, value, and bid date usable, then drop duplicate projects."""
    projects = projects.copy()
    projects["city"] = projects["city"].fillna("").str.strip()
    projects["value_cad"] = pd.to_numeric(projects["value_cad"], errors="coerce")
    projects["bid_date"] = pd.to_datetime(projects["bid_date"], errors="coerce")
    return projects.drop_duplicates(subset=["project_id"])


def find_opportunities(projects):
    """Keep Montreal projects of $5M+ whose bid date is today or later."""
    today = pd.Timestamp.today().normalize()
    in_montreal = projects["city"].str.contains("montreal", case=False)
    big_enough = projects["value_cad"] >= MIN_VALUE_CAD
    still_open = projects["bid_date"] >= today
    matches = projects[in_montreal & big_enough & still_open]
    return matches.sort_values("value_cad", ascending=False)


def save_results(results):
    """Write the matches to a CSV file and a SQLite database."""
    results.to_csv(HERE / "opportunities.csv", index=False)

    with sqlite3.connect(HERE / "projects.db") as connection:
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
