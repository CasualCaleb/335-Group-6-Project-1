from datetime import date

def recipient_rejection(donation, recipient, remaining_capacity, scheduled_time):
    if donation['food_type'] not in recipient['accepted_food_types']:
        return 'food type not accepted'
    if donation['pickup_area'] != recipient['area']:
        return 'recipient is outside the pickup area'
    if donation['quantity_kg'] > remaining_capacity:
        return 'insufficient recipient capacity'
    if scheduled_time > recipient['closing_time']:
        return 'recipient closes before pickup is possible'
    return None

def volunteer_rejection(donation, volunteer, pickups_used, scheduled_time):
    if donation['pickup_area'] != volunteer['area']:
        return 'volunteer is outside the pickup area'
    if donation['quantity_kg'] > volunteer['vehicle_capacity_kg']:
        return 'insufficient vehicle capacity'
    if pickups_used >= volunteer['max_pickups']:
        return 'volunteer has reached maximum pickups'
    if scheduled_time < volunteer['availability_start']:
        return 'volunteer not yet available'
    if scheduled_time > volunteer['availability_end']:
        return 'volunteer no longer available'
    return None

def find_match(donation, recipients, volunteers, remaining_capacities,
               pickup_counts, schedule_date):
    if not isinstance(schedule_date, date):
        raise TypeError('schedule_date must be a datetime.date')

    donation_id = donation['donation_id']
    expiry = donation['expiry_date']
    if expiry < schedule_date:
        return _unassigned(donation_id, 'Donation expired before the planning date')

    if not recipients:
        return _unassigned(donation_id, 'No recipients are available')
    if not volunteers:
        return _unassigned(donation_id, 'No volunteers are available')

    rejected = []
    for recipient in recipients:
        recipient_id = recipient['recipient_id']
        if recipient_id not in remaining_capacities:
            raise ValueError(f'Missing remaining capacity for {recipient_id}')

        # Each candidate volunteer may become available after the donation is ready.
        for volunteer in volunteers:
            volunteer_id = volunteer['volunteer_id']
            if volunteer_id not in pickup_counts:
                raise ValueError(f'Missing pickup count for {volunteer_id}')

            scheduled_time = max(donation['ready_time'], volunteer['availability_start'])
            reason = recipient_rejection(
                donation, recipient, remaining_capacities[recipient_id], scheduled_time
            )
            if reason is None:
                reason = volunteer_rejection(
                    donation, volunteer, pickup_counts[volunteer_id], scheduled_time
                )
            if reason is not None:
                rejected.append(reason)
                continue

            return {
                'donation_id': donation_id,
                'recipient_id': recipient_id,
                'volunteer_id': volunteer_id,
                'scheduled_time': scheduled_time,
                'status': 'assigned',
                'reason': (
                    f"{donation['quantity_kg']:g} kg of {donation['food_type']} assigned "
                    f"to {recipient['organization_name']} with volunteer {volunteer_id}; "
                    'food type, area, time, and capacity constraints satisfied'
                ),
            }

    # Provide a useful explanation instead of reporting only an unassigned ID.
    if rejected:
        distinct_reasons = list(dict.fromkeys(rejected))
        detail = '; '.join(distinct_reasons[:4])
        return _unassigned(donation_id, f'No feasible recipient/volunteer pair: {detail}')
    return _unassigned(donation_id, 'No feasible recipient/volunteer pair')

def _unassigned(donation_id, reason):
    return {
        'donation_id': donation_id,
        'recipient_id': None,
        'volunteer_id': None,
        'scheduled_time': None,
        'status': 'unassigned',
        'reason': reason,
    }
