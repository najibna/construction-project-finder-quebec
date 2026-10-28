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

## Why the sample returns nothing

`projects.csv` has five rows. Today is after 13 October 2026, so every bid date fails the “still open” check.

If those dates were still in the future, only the first two rows would match:

| Project | City | Value | Why it is out (with current dates) |
| --- | --- | --- | --- |
| Renovation of a Building L-042 | Montreal | $13.35M | Bid date has passed |
| Renovation of a Building L-042 Site Work | Montreal | $13.35M | Bid date has passed |
| Portfolio of Roof Refurbishment Works | Beaumont | $80M | Not Montreal |
| Renovation of Infrastructure at Pointe-a-la-Renommee | Gaspe | $2M | Not Montreal, and under $5M |
| Roof Renovation at Mistouk Sports Centre | Alma | $1M | Not Montreal, and under $5M |

To see a match while you are learning the code, change one Montreal `bid_date` in `projects.csv` to a future date and run `python app.py` again.

## Change the rule

Edit the top of `app.py`:

- `MIN_VALUE_CAD = 5_000_000` — the dollar cutoff.
- The string `"montreal|montréal"` inside `find_opportunities` — the city match. The `|` means “or”.

## What you will see when it works

Change one Montreal row's `bid_date` to a future date (for example `2027-01-15`) and run the program. The output looks like this:

```text
Found 2 open Montreal opportunities worth at least $5M.
                                    name     city  value_cad   bid_date
          Renovation of a Building L-042 Montreal   13350000 2027-01-15
Renovation of a Building L-042 Site Work Montreal   13350000 2027-01-15
Saved to opportunities.csv and projects.db
```

## Words used in this project

| Word | Plain meaning |
| --- | --- |
| **CSV** | A text file where each line is a row and commas separate the columns. Opens in Excel. |
| **Pandas** | A Python library for working with tables of data. |
| **DataFrame** | Pandas' name for a table. `projects` in `app.py` is one. |
| **SQLite** | A database stored in one file. No server to install. |
| **Pipeline** | Steps run in order: load, clean, filter, save. |
| **Ingest** | Bring data into the program. Here: read the CSV. |
| **NaN** | Pandas' marker for a blank or missing value. |

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `ModuleNotFoundError: No module named 'pandas'` | Run `python -m pip install -r requirements.txt`. |
| `externally-managed-environment` error on macOS | Use the virtual environment steps in [Run it](#run-it). |
| `python: command not found` | Use `python3` in place of `python`. |
| Output says 0 opportunities | Expected for the sample file. See [Why the sample returns nothing](#why-the-sample-returns-nothing). |
| A project you expect is missing | Check its city spelling, that `value_cad` is a plain number, and that `bid_date` is `YYYY-MM-DD` and not in the past. |

## Where to go next

1. Replace `projects.csv` with an authorized ConstructConnect export, or another feed you have permission to use, keeping the same columns.
2. Add a second rule, for example only a certain `category`. It is one more line in `find_opportunities`.
3. Run `python app.py` on a schedule (cron on Mac or Linux, Task Scheduler on Windows) so the results refresh by themselves.

ConstructConnect limits automated access and some project details need a subscription. This project does not scrape the site.

## Sample data

The five rows are short examples shaped like public construction listings, including a link to the ConstructConnect Quebec projects page. They are for trying the pipeline. Replace the file with a current export when you have one.
