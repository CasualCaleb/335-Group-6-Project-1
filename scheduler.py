from datetime import date

from matching import find_match

def _schedule(ordered_donations, recipients, volunteers, schedule_date, strategy):
    if not isinstance(schedule_date, date):
        raise TypeError('schedule_date must be a datetime.date')

    # Copy only state, not records: each scheduling run is independent.
    remaining_capacities = {
        recipient['recipient_id']: recipient['capacity_kg']
        for recipient in recipients
    }
    pickup_counts = {volunteer['volunteer_id']: 0 for volunteer in volunteers}
    results = []

    for donation in ordered_donations:
        assignment = find_match(
            donation, recipients, volunteers, remaining_capacities,
            pickup_counts, schedule_date
        )
        assignment['strategy'] = strategy

        if assignment['status'] == 'assigned':
            recipient_id = assignment['recipient_id']
            volunteer_id = assignment['volunteer_id']
            remaining_capacities[recipient_id] -= donation['quantity_kg']
            pickup_counts[volunteer_id] += 1

        results.append(assignment)

    return results

def schedule_fifo(donations, recipients, volunteers, schedule_date):
    return _schedule(donations, recipients, volunteers, schedule_date, 'FIFO')

def schedule_greedy(donations, recipients, volunteers, schedule_date):
    prioritized = sorted(
        donations,
        key=lambda donation: (
            donation['expiry_date'],
            -donation['quantity_kg'],
            donation['ready_time'],
        ),
    )
    return _schedule(prioritized, recipients, volunteers, schedule_date, 'Greedy')