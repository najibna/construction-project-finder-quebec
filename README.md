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

