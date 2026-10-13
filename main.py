import argparse
import os
from datetime import date
from pathlib import Path
from rescueroute.data_loader import load_donations, load_recipients, load_volunteers
from rescueroute.scheduler import schedule_fifo, schedule_greedy
from rescueroute.validation import validate_data

# Keep the demonstration reproducible regardless of the current calendar date.
DEFAULT_PLANNING_DATE = date(2026, 10, 8)

def display_results(title, assignments):
    """Print the outcome and explanation for every processed donation."""
    print(f"\n{'=' * 60}")
    print(title)
    print('=' * 60)

    for assignment in assignments:
        donation_id = assignment['donation_id']
        status = assignment['status'].upper()
        print(f"\n{donation_id}: {status}")
        if assignment['status'] == 'assigned':
            print(f"  Recipient: {assignment['recipient_id']}")
            print(f"  Volunteer: {assignment['volunteer_id']}")
            print(f"  Scheduled: {assignment['scheduled_time'].strftime('%H:%M')}")
        print(f"  Reason: {assignment['reason']}")

    assigned = sum(a['status'] == 'assigned' for a in assignments)
    print(f"\nAssigned: {assigned}/{len(assignments)} | Unassigned: {len(assignments) - assigned}")

def main():
    parser = argparse.ArgumentParser(description='RescueRoute donation scheduling demo')
    parser.add_argument(
        '--date',
        type=date.fromisoformat,
        default=DEFAULT_PLANNING_DATE,
        metavar='YYYY-MM-DD',
        help='Simulated planning date (default: 2026-10-08)',
    )
    args = parser.parse_args()

    # Existing data_loader.py uses relative paths such as data/donations.csv.
    # Make them work when this script is launched from another directory.
    os.chdir(Path(__file__).resolve().parent)

    try:
        donations, recipients, volunteers = validate_data(
            load_donations(), load_recipients(), load_volunteers()
        )
    except (OSError, ValueError) as exc:
        parser.exit(status=1, message=f'Could not load or validate input: {exc}\n')

    print('RescueRoute — Surplus Food Matching & Pickup Planner')
    print(f'Simulated planning date: {args.date.isoformat()}')
    print(f'Donations: {len(donations)} | Recipients: {len(recipients)} | Volunteers: {len(volunteers)}')

    fifo = schedule_fifo(donations, recipients, volunteers, args.date)
    greedy = schedule_greedy(donations, recipients, volunteers, args.date)

    display_results('FIFO — Input / arrival order', fifo)
    display_results('GREEDY — Earliest expiry, largest quantity, earliest ready time', greedy)

    print('\nNote: detailed metrics and strategy comparison are planned for metrics.py.')

if __name__ == '__main__':
    main()
