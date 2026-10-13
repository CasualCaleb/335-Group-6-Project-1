"""Validate and normalize RescueRoute CSV records before scheduling."""

from datetime import date, datetime, time


def _required(row, field, kind, row_number):
    value = row.get(field)
    if value is None or not str(value).strip():
        raise ValueError(f"{kind} row {row_number}: missing {field}")
    return str(value).strip()


def _positive_number(row, field, kind, row_number):
    raw = _required(row, field, kind, row_number)
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"{kind} row {row_number}: invalid {field}: {raw}") from exc
    if not (0 < value < float('inf')):
        raise ValueError(f"{kind} row {row_number}: {field} must be a finite positive number")
    return value


def _nonnegative_integer(row, field, kind, row_number):
    raw = _required(row, field, kind, row_number)
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{kind} row {row_number}: {field} must be an integer") from exc
    if value < 0:
        raise ValueError(f"{kind} row {row_number}: {field} cannot be negative")
    return value


def _time(row, field, kind, row_number):
    raw = _required(row, field, kind, row_number)
    try:
        return datetime.strptime(raw, '%H:%M').time()
    except ValueError as exc:
        raise ValueError(f"{kind} row {row_number}: {field} must use HH:MM (24-hour)") from exc


def _unique_id(row, field, seen, kind, row_number):
    identifier = _required(row, field, kind, row_number)
    if identifier in seen:
        raise ValueError(f"{kind} row {row_number}: duplicate {field} {identifier}")
    seen.add(identifier)
    return identifier


def validate_donations(records):
    """Return copies with quantity_kg as float, expiry_date as date, ready_time as time."""
    results, seen = [], set()
    for number, row in enumerate(records, 1):
        donation = dict(row)
        donation['donation_id'] = _unique_id(row, 'donation_id', seen, 'Donation', number)
        for field in ('donor_name', 'food_type', 'pickup_area'):
            donation[field] = _required(row, field, 'Donation', number)
        donation['quantity_kg'] = _positive_number(row, 'quantity_kg', 'Donation', number)
        raw_date = _required(row, 'expiry_date', 'Donation', number)
        try:
            donation['expiry_date'] = date.fromisoformat(raw_date)
        except ValueError as exc:
            raise ValueError(f"Donation row {number}: expiry_date must use YYYY-MM-DD") from exc
        donation['ready_time'] = _time(row, 'ready_time', 'Donation', number)
        results.append(donation)
    return results


def validate_recipients(records):
    """Return copies with accepted_food_types as set and capacity_kg as float."""
    results, seen = [], set()
    for number, row in enumerate(records, 1):
        recipient = dict(row)
        recipient['recipient_id'] = _unique_id(row, 'recipient_id', seen, 'Recipient', number)
        for field in ('organization_name', 'area'):
            recipient[field] = _required(row, field, 'Recipient', number)
        foods = _required(row, 'accepted_food_types', 'Recipient', number)
        recipient['accepted_food_types'] = {item.strip() for item in foods.split(';') if item.strip()}
        if not recipient['accepted_food_types']:
            raise ValueError(f"Recipient row {number}: no accepted food types")
        recipient['capacity_kg'] = _positive_number(row, 'capacity_kg', 'Recipient', number)
        recipient['closing_time'] = _time(row, 'closing_time', 'Recipient', number)
        results.append(recipient)
    return results


def validate_volunteers(records):
    """Return copies with vehicle capacity as float and max_pickups as int."""
    results, seen = [], set()
    for number, row in enumerate(records, 1):
        volunteer = dict(row)
        volunteer['volunteer_id'] = _unique_id(row, 'volunteer_id', seen, 'Volunteer', number)
        volunteer['area'] = _required(row, 'area', 'Volunteer', number)
        volunteer['vehicle_capacity_kg'] = _positive_number(row, 'vehicle_capacity_kg', 'Volunteer', number)
        volunteer['max_pickups'] = _nonnegative_integer(row, 'max_pickups', 'Volunteer', number)
        volunteer['availability_start'] = _time(row, 'availability_start', 'Volunteer', number)
        volunteer['availability_end'] = _time(row, 'availability_end', 'Volunteer', number)
        if volunteer['availability_start'] >= volunteer['availability_end']:
            raise ValueError(f"Volunteer row {number}: availability_end must follow availability_start")
        results.append(volunteer)
    return results


def validate_data(donations, recipients, volunteers):
    """Validate all datasets and return (donations, recipients, volunteers)."""
    return (
        validate_donations(donations),
        validate_recipients(recipients),
        validate_volunteers(volunteers),
    )
