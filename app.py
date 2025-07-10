"""Find construction projects in Montreal worth at least $5 million."""

from pathlib import Path

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
    """Keep Montreal projects worth at least $5 million."""
    in_montreal = projects["city"].str.contains("montreal", case=False)
    big_enough = projects["value_cad"] >= MIN_VALUE_CAD
    return projects[in_montreal & big_enough]


def main():
    projects = load_projects()
    projects = clean_projects(projects)
    results = find_opportunities(projects)
    print(f"Found {len(results)} Montreal projects worth at least $5M.")


if __name__ == "__main__":
    main()
