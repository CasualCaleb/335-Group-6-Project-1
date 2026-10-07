# RescueRoute

**CPSC 335 — Algorithms and Data Structures**

RescueRoute is an explainable Python application for matching time-sensitive surplus food donations with compatible community organizations and volunteer drivers.

The project compares a **FIFO baseline** with a **greedy urgency-first strategy** and explains why each donation was assigned, deferred, or left unmatched.

> **Academic project disclaimer:** RescueRoute is an educational prototype. It is not a production food-safety, medical, emergency-response, or certified routing system. Unless otherwise documented, all project data is simulated.

---

## Project Goals

RescueRoute is designed to answer the following question:

> How can time-sensitive food donations be prioritized and assigned to compatible recipients and volunteers in a way that is efficient, transparent, and easy to explain?

The system will:

- Load donation, recipient, and volunteer data from CSV or JSON files.
- Validate IDs, quantities, food types, capacities, availability, and time values.
- Identify feasible donation-recipient-volunteer matches.
- Implement and compare FIFO and greedy scheduling strategies.
- Produce a human-readable reason for every assignment or rejection.
- Calculate metrics that compare both strategies.
- Include automated tests for normal cases and edge cases.

---

## Team Members

| Member | Role | Responsibilities |
|---|---|---|
| Caleb McMullin | TBD | TBD |
| Emily Velasco | TBD | TBD |
| Bryan Zavala | TBD | TBD |

Suggested team roles:

- **Algorithm & Optimization Lead** — FIFO scheduler, greedy strategy, priority selection, complexity analysis, and strategy comparison.
- **Data & Matching Lead** — input files, validation, compatibility checks, capacity rules, data structures, and test data.
- **Product & Quality Lead** — explainable output, metrics, automated tests, README, demo materials, and interface polish.

All team members are expected to participate in design discussions, debugging, testing, code review, documentation, and the final presentation.

---

## Core Data Model

### Donation

Minimum information:

- `donation_id`
- donor name
- food type
- quantity
- expiration / remaining shelf life
- pickup area
- ready time

### Recipient

Minimum information:

- `recipient_id`
- organization name
- accepted food types
- capacity
- area / location
- closing time

### Volunteer

Minimum information:

- `volunteer_id`
- vehicle capacity
- area / location
- availability
- maximum pickups

### Assignment

Minimum information:

- `donation_id`
- `recipient_id`
- `volunteer_id`
- scheduled time
- decision reason
- status

---

## Algorithms

RescueRoute compares two scheduling approaches using the **same input data**.

### 1. FIFO Baseline

The FIFO scheduler processes donations in arrival order.

For each donation:

1. Check whether the donation is still valid.
2. Search for the first feasible recipient.
3. Search for the first feasible volunteer.
4. Create the assignment if all constraints are satisfied.
5. Otherwise, record the donation as unassigned with an explanation.

FIFO provides a simple baseline for comparing the effectiveness of the greedy strategy.

---

### 2. Greedy Urgency-First Strategy

The greedy scheduler prioritizes donations according to urgency rather than strict arrival order.

### Greedy Rule

Our initial greedy rule is:

1. Prioritize the donation with the **least remaining shelf life**.
2. If two donations have equal remaining shelf life, prioritize the **larger quantity**.
3. If still tied, prioritize the donation with the **earlier ready/arrival time**.

This rule attempts to rescue food that is most likely to expire first while using quantity and arrival time as deterministic tie-breakers.

The greedy strategy is not assumed to produce a globally optimal schedule. Its purpose is to make a reasonable local decision at each step and compare the result against FIFO.

---

## Matching Constraints

A donation-recipient-volunteer assignment is feasible only when all required conditions are satisfied.

Examples include:

- The recipient accepts the donation's food type.
- The recipient has enough remaining capacity.
- The recipient is open when the donation can be delivered.
- The donation has not expired.
- A volunteer is available.
- The volunteer has enough vehicle capacity.
- The volunteer has not exceeded their maximum number of pickups.
- Any required area/location compatibility rule is satisfied.

---

## Explainable Decisions

Every donation must produce a human-readable decision.

Example assignment:

```text
Donation D-1001 was assigned to Community Shelter with volunteer V-301
because the donation expires in 90 minutes, the shelter accepts the food
type, recipient capacity is available, and the volunteer can carry the quantity.
```

Example rejection:

```text
Donation D-1008 could not be assigned because no compatible recipient
had enough remaining capacity before the donation expired.
```

Example greedy-priority explanation:

```text
Donation D-1014 was considered after D-1002 because D-1002 had less
remaining shelf life under the urgency-first greedy rule.
```

The goal is for a user to understand the constraints and priority rules that caused each decision.

---

## Data Structures

The project uses standard Python data structures where they naturally fit the problem.

| Need | Data Structure | Reason |
|---|---|---|
| Lookup by ID | `dict` | Expected fast direct retrieval |
| Duplicate ID detection | `set` | Expected fast membership testing |
| Food-type compatibility | `set` | Natural representation of accepted categories |
| FIFO pending donations | `deque` or `list` | Preserves arrival order |
| Greedy pending donations | `heapq` or sorted list | Selects the next donation by priority |
| Assignment history | `list` | Maintains ordered results |
| Metrics | `dict` | Stores named aggregate values |

---

## Complexity Analysis

Let:

- `D` = number of donations
- `R` = number of recipients
- `V` = number of volunteers

A straightforward matching implementation may examine recipients and volunteers for each donation.

A simple worst-case estimate is:

```text
O(D × R × V)
```

if every donation may require checking combinations of recipients and volunteers.

Direct ID lookup and duplicate detection using dictionaries and sets are expected to be approximately:

```text
O(1)
```

on average.

If the greedy implementation uses a heap to prioritize donations, inserting and removing donations from the priority queue costs approximately:

```text
O(log D)
```

per heap operation.

The exact dominant complexity will depend on the final matching implementation and any indexing or filtering added by the team.

---

## Metrics

The application will report metrics including:

- Donations received
- Donations assigned
- Donations unassigned
- Total food quantity rescued
- Food quantity at risk
- Urgent rescue rate
- Recipient capacity utilization
- Volunteer capacity utilization
- FIFO vs. greedy comparison

The comparison will help determine whether urgency-based scheduling improves outcomes over simple FIFO ordering.

---

## Project Structure

A possible project structure is:

```text
RescueRoute/
├── data/
│   ├── donations.csv
│   ├── recipients.csv
│   └── volunteers.csv
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── loader.py
│   ├── validation.py
│   ├── matching.py
│   ├── fifo.py
│   ├── greedy.py
│   ├── metrics.py
│   └── explanations.py
│
├── tests/
│   ├── test_validation.py
│   ├── test_fifo.py
│   ├── test_greedy.py
│   ├── test_matching.py
│   └── test_metrics.py
│
├── docs/
│   └── ...
│
├── README.md
├── requirements.txt
└── .gitignore
```

The final structure may change as the implementation develops.

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd RescueRoute
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running RescueRoute

Example:

```bash
python src/main.py
```

Final command-line arguments and input options will be documented once the interface is finalized.

---

## Testing

The project uses `pytest` or Python's built-in `unittest` framework.

Run the test suite with:

```bash
pytest
```

Required testing scenarios include:

- Normal compatible donation-recipient-volunteer match
- Duplicate donation ID
- Expired or nearly expired donation
- No compatible recipient food type
- Insufficient recipient capacity
- No available volunteer with sufficient vehicle capacity
- Two donations competing for the same capacity
- Empty input files or lists
- A case where FIFO and greedy produce different outcomes
- A fairness or starvation case showing why a donation may be deferred

Tests should verify expected behavior rather than simply execute the program without errors.

---

## FIFO vs. Greedy Comparison

Both algorithms will run against the same input data.

Results will be compared using metrics such as:

| Metric | FIFO | Greedy |
|---|---:|---:|
| Donations assigned | TBD | TBD |
| Donations unassigned | TBD | TBD |
| Quantity rescued | TBD | TBD |
| Quantity at risk | TBD | TBD |
| Urgent rescue rate | TBD | TBD |
| Recipient utilization | TBD | TBD |
| Volunteer utilization | TBD | TBD |

Final results will be added after implementation and benchmarking.

---

## Limitations

RescueRoute intentionally simplifies a real-world logistics problem.

Current limitations may include:

- Simulated input data
- Simplified location/area matching
- No live traffic information
- No real food-safety verification
- No guarantee of globally optimal assignments
- Simplified time and travel assumptions
- Greedy decisions may create fairness or starvation trade-offs

These limitations will be updated as the project evolves.

---

## Development Schedule

### Week 1

- Create repository
- Define data model
- Implement input validation
- Implement FIFO baseline
- Create sample data
- Create at least 5 tests

### Week 2

- Implement greedy urgency-first strategy
- Add explainable decisions
- Add metrics
- Compare FIFO and greedy
- Expand to at least 10 tests
- Update README

### Week 3

- Polish implementation
- Finalize automated tests
- Complete documentation
- Prepare demo
- Prepare final report
- Prepare final presentation

---

## Development Workflow

Before starting work:

```bash
git pull
```

Create a branch for the task:

```bash
git checkout -b feature/task-name
```

Commit changes:

```bash
git add .
git commit -m "Implement task description"
```

Push the branch:

```bash
git push origin feature/task-name
```

Use pull requests and code review before merging major changes into `main`.

Example branch names:

```text
feature/fifo-scheduler
feature/greedy-scheduler
feature/input-validation
feature/metrics
test/matching-cases
docs/complexity-analysis
fix/capacity-check
```

---

## Team Contributions

Final contributions will be documented here before submission.

### Caleb McMullin

- TBD

### Team Member 2

- TBD

### Team Member 3

- TBD

---

## Optional Stretch Features

Stretch features should only be considered after the required system is working correctly.

Possible additions include:

- Streamlit dashboard
- Simulated map distances
- Fairness rules
- Route planning
- What-if analysis
- Constraint-optimization comparison

---

## Final Deliverables

The completed project will include:

- GitHub repository
- Runnable Python application
- Sample CSV or JSON input files
- FIFO scheduling implementation
- Greedy urgency-first scheduling implementation
- Explainable assignment and failure output
- Automated test suite
- Metrics and FIFO-vs.-greedy comparison
- Architecture and complexity documentation
- Limitations and trade-off discussion
- Team contribution statements
- 3–5 minute demo video or live demonstration

---

## Course

**CPSC 335 — Algorithms and Data Structures**

**Group Project: RescueRoute**

---

## License

This project is intended for educational use as part of CPSC 335.
