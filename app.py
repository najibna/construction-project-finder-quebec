"""Load and clean Quebec construction projects."""

from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent


def load_projects():
    """Read the project list from projects.csv."""
    return pd.read_csv(HERE / "projects.csv")


def clean_projects(projects):
    """Make city and value usable."""
    projects = projects.copy()
    projects["city"] = projects["city"].fillna("").str.strip()
    projects["value_cad"] = pd.to_numeric(projects["value_cad"], errors="coerce")
    return projects


def main():
    projects = load_projects()
    projects = clean_projects(projects)
    print(f"Loaded {len(projects)} projects.")


if __name__ == "__main__":
    main()
