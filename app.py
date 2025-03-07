"""Load Quebec construction projects from a CSV file."""

from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent


def load_projects():
    """Read the project list from projects.csv."""
    return pd.read_csv(HERE / "projects.csv")


def main():
    projects = load_projects()
    print(f"Loaded {len(projects)} projects.")
    print(projects)


if __name__ == "__main__":
    main()
