# Quebec Construction Project Finder

A small Python program that reads a list of construction projects and keeps the ones that match one rule:

**Montreal (or Montréal), worth at least CAD $5 million, bid date today or later.**

It saves those matches to a spreadsheet (`opportunities.csv`) and a local database (`projects.db`).

This is a minimal data pipeline: load a file, clean it with Pandas, filter it, store the result. The input is a CSV you supply. Swap in an authorized ConstructConnect export by replacing `projects.csv` and keeping the same column names.

## Run it

You need Python 3.

```bash
python -m pip install -r requirements.txt
python app.py
```

On a Mac with Homebrew Python, install into a virtual environment if `pip` refuses a system-wide install:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Expected output with the sample file: **0 opportunities**. The sample bid dates are 13 October 2026, so they are already in the past. That is the filter working. See [Why the sample returns nothing](#why-the-sample-returns-nothing).

## Files

| File | Role |
| --- | --- |
| `app.py` | The whole program |
| `projects.csv` | Input. Five example projects |
| `requirements.txt` | The one dependency: Pandas |
| `opportunities.csv` | Output spreadsheet. Created when you run the program |
| `projects.db` | Output database. Created when you run the program |

Required columns in `projects.csv`:

`project_id`, `name`, `city`, `value_cad`, `bid_date`, `category`, `source_url`

Dates use `YYYY-MM-DD`. `value_cad` is a number of Canadian dollars, with no `$` or commas.

## How the code works

`app.py` is four functions, called in order from `main`.

### 1. `load_projects`

Reads `projects.csv` into a Pandas table (a DataFrame). `project_id` is read as text so a value like `06023317` would keep its leading zero.

### 2. `clean_projects`

Prepares the three columns the filter uses:

- **city** — fill blanks and strip spaces, so `" Montreal "` matches Montreal.
- **value_cad** — turn the text into a number. A bad value becomes blank instead of stopping the program.
- **bid_date** — turn `2026-10-13` into a real date. A bad date becomes blank.
- **duplicates** — if the same `project_id` appears twice, keep the first row.

### 3. `find_opportunities`

A row is kept only when all three are true:

1. The city contains `montreal` or `montréal` (uppercase or lowercase).
2. `value_cad` is at least `5_000_000` (the `MIN_VALUE_CAD` constant at the top of `app.py`).
3. `bid_date` is today or a future day. Today is midnight at the start of the current day, so a bid due today still counts.

Matches are sorted with the largest dollar value first.

### 4. `save_results`

Writes every matching row to:

- `opportunities.csv`, for opening in Excel or Numbers.
- `projects.db`, a SQLite file. The table is named `opportunities`. Each run replaces that table, so yesterday’s matches are not mixed with today’s.

SQLite needs no server. You can open `projects.db` with [DB Browser for SQLite](https://sqlitebrowser.org/) or with:

```bash
sqlite3 projects.db "SELECT name, city, value_cad, bid_date FROM opportunities;"
```

