"""Load and clean Quebec construction projects."""

from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent


def load_projects():
    """Read the project list from projects.csv."""
    return pd.read_csv(HERE / "projects.csv")


def clean_projects(projects):
    """Strip city names so extra spaces do not break a match."""
    projects = projects.copy()
    projects["city"] = projects["city"].fillna("").str.strip()
    return projects


def main():
    projects = load_projects()
    projects = clean_projects(projects)
    print(f"Loaded {len(projects)} projects.")


if __name__ == "__main__":
    main()
