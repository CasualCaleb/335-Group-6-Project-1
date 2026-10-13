from datetime import date, time
import pytest
from matching import find_match
from scheduler import schedule_fifo, schedule_greedy
from validation import validate_data

PLANNING_DATE = date(2026, 10, 8)

def example_data():
    donations = [
        {
            'donation_id': 'D001', 'donor_name': 'Market',
            'food_type': 'Produce', 'quantity_kg': '10',
            'expiry_date': '2026-10-10', 'pickup_area': 'Covina',
            'ready_time': '09:00',
        }
    ]
    recipients = [
        {
            'recipient_id': 'R001', 'organization_name': 'Food Bank',
            'accepted_food_types': 'Produce;Bakery', 'capacity_kg': '15',
            'area': 'Covina', 'closing_time': '17:00',
        }
    ]
    volunteers = [
        {
            'volunteer_id': 'V001', 'vehicle_capacity_kg': '20',
            'area': 'Covina', 'availability_start': '08:00',
            'availability_end': '16:00', 'max_pickups': '2',
        }
    ]
    return validate_data(donations, recipients, volunteers)

def test_valid_data_is_normalized():
    donations, recipients, volunteers = example_data()
    assert donations[0]['quantity_kg'] == 10.0
    assert donations[0]['expiry_date'] == date(2026, 10, 10)
    assert recipients[0]['accepted_food_types'] == {'Produce', 'Bakery'}
    assert volunteers[0]['max_pickups'] == 2

def test_normal_match():
    donations, recipients, volunteers = example_data()
    result = schedule_fifo(donations, recipients, volunteers, PLANNING_DATE)[0]
    assert result['status'] == 'assigned'
    assert result['recipient_id'] == 'R001'
    assert result['volunteer_id'] == 'V001'
    assert result['reason']


def test_duplicate_donation_id_is_rejected():
    donations, recipients, volunteers = example_data()
    # The validator must reject duplicate IDs on raw input.
    from validation import validate_donations
    raw = [dict(donations[0], expiry_date='2026-10-10', ready_time='09:00')]
    with pytest.raises(ValueError, match='duplicate'):
        validate_donations(raw + [dict(raw[0])])

def test_expired_donation_is_unassigned():
    donations, recipients, volunteers = example_data()
    donations[0]['expiry_date'] = date(2026, 10, 7)
    result = schedule_fifo(donations, recipients, volunteers, PLANNING_DATE)[0]
    assert result['status'] == 'unassigned'
    assert 'expired' in result['reason'].lower()

def test_incompatible_food_type():
    donations, recipients, volunteers = example_data()
    donations[0]['food_type'] = 'Dairy'
    result = schedule_fifo(donations, recipients, volunteers, PLANNING_DATE)[0]
    assert result['status'] == 'unassigned'
    assert 'food type' in result['reason'].lower()

def test_insufficient_recipient_capacity():
    donations, recipients, volunteers = example_data()
    recipients[0]['capacity_kg'] = 5.0
    result = schedule_fifo(donations, recipients, volunteers, PLANNING_DATE)[0]
    assert result['status'] == 'unassigned'
    assert 'recipient capacity' in result['reason'].lower()

def test_insufficient_vehicle_capacity():
    donations, recipients, volunteers = example_data()
    volunteers[0]['vehicle_capacity_kg'] = 5.0
    result = schedule_fifo(donations, recipients, volunteers, PLANNING_DATE)[0]
    assert result['status'] == 'unassigned'
    assert 'vehicle capacity' in result['reason'].lower()

def test_unavailable_volunteer():
    donations, recipients, volunteers = example_data()
    volunteers[0]['max_pickups'] = 0
    result = schedule_fifo(donations, recipients, volunteers, PLANNING_DATE)[0]
    assert result['status'] == 'unassigned'
    assert 'volunteer' in result['reason'].lower()

def test_recipient_closes_too_early():
    donations, recipients, volunteers = example_data()
    recipients[0]['closing_time'] = time(8, 0)
    result = schedule_fifo(donations, recipients, volunteers, PLANNING_DATE)[0]
    assert result['status'] == 'unassigned'
    assert 'closes' in result['reason'].lower()

def test_competing_donations_use_remaining_capacity():
    donations, recipients, volunteers = example_data()
    second = dict(donations[0], donation_id='D002')
    donations.append(second)
    results = schedule_fifo(donations, recipients, volunteers, PLANNING_DATE)
    assert [r['status'] for r in results] == ['assigned', 'unassigned']
    assert 'capacity' in results[1]['reason'].lower()

def test_volunteer_pickup_limit():
    donations, recipients, volunteers = example_data()
    recipients[0]['capacity_kg'] = 30.0
    volunteers[0]['max_pickups'] = 1
    donations.append(dict(donations[0], donation_id='D002'))
    results = schedule_fifo(donations, recipients, volunteers, PLANNING_DATE)
    assert [r['status'] for r in results] == ['assigned', 'unassigned']
    assert 'maximum pickups' in results[1]['reason'].lower()

def test_empty_inputs():
    assert schedule_fifo([], [], [], PLANNING_DATE) == []
    donations, _, _ = example_data()
    result = schedule_fifo(donations, [], [], PLANNING_DATE)[0]
    assert result['status'] == 'unassigned'
    assert result['reason']

def test_fifo_and_greedy_have_different_outcomes():
    donations, recipients, volunteers = example_data()
    donations[0]['expiry_date'] = date(2026, 10, 12)
    donations.append(dict(
        donations[0], donation_id='D002', expiry_date=date(2026, 10, 9)
    ))
    fifo = schedule_fifo(donations, recipients, volunteers, PLANNING_DATE)
    greedy = schedule_greedy(donations, recipients, volunteers, PLANNING_DATE)
    assert [r['donation_id'] for r in fifo] == ['D001', 'D002']
    assert [r['donation_id'] for r in greedy] == ['D002', 'D001']
    assert [r['donation_id'] for r in fifo if r['status'] == 'assigned'] == ['D001']
    assert [r['donation_id'] for r in greedy if r['status'] == 'assigned'] == ['D002']

def test_greedy_quantity_tiebreaker():
    donations, recipients, volunteers = example_data()
    donations.append(dict(donations[0], donation_id='D002', quantity_kg=12.0))
    results = schedule_greedy(donations, recipients, volunteers, PLANNING_DATE)
    assert results[0]['donation_id'] == 'D002'

def test_strategy_runs_do_not_mutate_input_records():
    donations, recipients, volunteers = example_data()
    first = schedule_fifo(donations, recipients, volunteers, PLANNING_DATE)
    second = schedule_fifo(donations, recipients, volunteers, PLANNING_DATE)
    assert first == second
    assert recipients[0]['capacity_kg'] == 15.0
    assert volunteers[0]['max_pickups'] == 2

def test_find_match_does_not_modify_counters():
    donations, recipients, volunteers = example_data()
    capacity = {'R001': 15.0}
    pickup_counts = {'V001': 0}
    result = find_match(donations[0], recipients, volunteers, capacity, pickup_counts, PLANNING_DATE)
    assert result['status'] == 'assigned'
    assert capacity == {'R001': 15.0}
    assert pickup_counts == {'V001': 0}