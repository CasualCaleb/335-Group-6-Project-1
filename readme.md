# RescueRoute 🚚🥕

**CPSC 335 — Algorithms and Data Structures**

A Python prototype that matches surplus food donations with compatible recipient organizations and volunteer drivers. It compares two scheduling approaches and explains each decision.

Rescue Route addresses challenges of matching donations to recipients on the basis of location, storage capacities, operating hours, food acceptance rules, and available volunteers.  The application tests and compares different algorithms: FIFO and Greedy. 

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

## Project files

- `main.py` — runs both algorithms
- `rescueroute/data_loader.py` — reads CSV files and loads records
- `rescueroute/validation.py` — validates CSV data
- `rescueroute/matching.py` — finds feasible matches
- `rescueroute/scheduler.py` — implements FIFO and greedy scheduling
- `data/` — contains sample CSV files
- `tests/` — contains automated tests

## Data Model

Donations
| Variable | Description |
|-------|-------------|
| `donation_id` | identifier for each donation |
| `donor_name` | name of the donating organization |
| `food_type` | category of donated food |
| `quantity_kg` | amount of food in kilograms |
| `expiry_date` | date the donation expires |
| `pickup_area` | location where food is available |
| `ready_time` | time the donation is available to pickup |

Recipients
| Variable | Description |
|----------|-------------|
| `recipient_id` | identifier for each recipient |
| `organization_name` | name of the recipient organization |
| `accepted_food_types` | category of food the organization accepts |
| `capacity_kg` | maximum food quantity the organization can receive in kilograms |
| `area` | recipient's location of service |
| `closing_time` | latest allowed scheduling time |

Volunteers
| Variable | Description |
|----------|-------------|
| `volunteer_id` | identifier for each volunteer |
| `vehicle_capacity_kg` | maximum food quantity the vehicle can transport per pickup |
| `area` | volunteer's service area |
| `availability_start` | beginning of volunteer availability |
| `availability_end` | end of volunteer availability |
| `max_pickups` | maximum number of assigned pickups |

Assignments
| Variable | Description |
|----------|-------------|
| `donation_id` | identifier for each donation being processed |
| `recipient_id` | identifier for the matched recipient organization |
| `volunteer_id` | identifier for the assigned volunteer |
| `scheduled_time` | scheduled pickup time |
| `status` | indicates whether the donation was assigned or unassigned |
| `decision_reason` | human-readable explanation of the scheduling decision |
| `strategy` | scheduling algorithm used (FIFO or Greedy) 

## How it works

- **FIFO:** Handles donations in CSV input order, assigning the first feasible recipient and volunteer.
  - Limitations: expiration of donations is not considered for processing order, earlier donations use resources needed by more urgent donations
- **Greedy:** Handles earliest-expiring donations first; ties go to larger quantities, then earlier ready times.
  - Limitations: prioritizing urgency does not necessarily maximize highest amount of food can be processed, locally made decision prevents more optimal solution later
- **Matching:** Checks food type, area, time, remaining recipient capacity, and volunteer availability, vehicle capacity, and pickup limits.
- **Output:** Shows assignments or rejection reasons for every donation.

The project uses dictionaries for capacity and pickup tracking, sets for compatibility and validation, and a sorted list for greedy ordering. With **D** donations, **R** recipients and **V** volunteers, FIFO takes up to **O(DRV)** time; greedy takes **O(D log D + DRV)**.


## Team and Contributions

- **Caleb McMullin** — Algorithm & Optimization Lead
- **Emily Velasco** — Product & Quality Lead
  - established and organized files and folders for initial project structure 
  - developed data_loader.py to input CSV files and load content
  - created sample data in CSV files for donations, recipients, and volunteers
  - verified overall integration of code and reworked README.md
- **Bryan Zavala** — Data & Matching Lead
