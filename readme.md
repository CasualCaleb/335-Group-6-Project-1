# RescueRoute 🚚🥕

**CPSC 335 — Algorithms and Data Structures**

A Python prototype that matches surplus food donations with compatible recipient organizations and volunteer drivers. It compares two scheduling approaches and explains each decision.

## Run it

Requires Python 3.10+.

```bash
pip install -r requirements.txt
python main.py
```

To use a different simulated date:

```bash
python main.py --date 2026-10-12
```

Run the tests:

```bash
python -m pytest -v
```

## How it works

- **FIFO:** Handles donations in CSV input order, assigning the first feasible recipient and volunteer.
- **Greedy:** Handles earliest-expiring donations first; ties go to larger quantities, then earlier ready times.
- **Matching:** Checks food type, area, time, remaining recipient capacity, and volunteer availability, vehicle capacity, and pickup limits.
- **Output:** Shows assignments or rejection reasons for every donation.

The project uses dictionaries for capacity and pickup tracking, sets for compatibility and validation, and a sorted list for greedy ordering. With **D** donations, **R** recipients and **V** volunteers, FIFO takes up to **O(DRV)** time; greedy takes **O(D log D + DRV)**.

## Project files

- `main.py` — runs both algorithms
- `data_loader.py` / `validation.py` — loads and checks CSV data
- `matching.py` — finds feasible matches
- `scheduler.py` — FIFO and greedy scheduling
- `data/` — sample CSV files
- `tests/` — automated tests

## Team

- **Caleb McMullin** — Algorithm & Optimization Lead
- **Emily Velasco** — Product & Quality Lead
- **Bryan Zavala** — Data & Matching Lead