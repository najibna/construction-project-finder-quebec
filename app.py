"""Find construction projects in Montreal."""

from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent


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
    """Keep projects whose city is Montreal."""
    in_montreal = projects["city"].str.contains("montreal", case=False)
    return projects[in_montreal]


def main():
    projects = load_projects()
    projects = clean_projects(projects)
    results = find_opportunities(projects)
    print(f"Found {len(results)} Montreal projects.")


if __name__ == "__main__":
    main()
