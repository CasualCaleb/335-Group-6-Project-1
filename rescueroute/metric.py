"""Preformance metrics for RescueRoute donation scheduling."""
from collections import defaultdict

def calculate_metrics(donations, recipients, volunteers, assignments):
    """calculates preformace metrics from one scheduling strategy.

    Urgent rescue rate:
        Percentage of donations sharing the earliest exiry date that were assigned.

    Recipient Capacity utilization:
        Assigned quantity / total initial recipient capacity.

    Volunteer capacity utilization:
        Assigned quantity / theoretical total vehicle capacity, 
        calculated as vehicle_capacity_kg * max_pickups per volunteer    
    """

    donation_by_id = {
        donation["donation_id"]: donation
        for donation in donations
    }

    #counts assignments with both a recipient and a volunteer.
    assigned_ids = {
        assignment["donation_id"]
        for assignment in assignments
        if (
            assignment["status"] == "assigned"
            and assignment["recipient_id"] is not None
            and assignment["volunteer_id"] is not None
        )
    }

    assigned_donations = [
        donation_by_id[donation_id]
        for donation_id in assigned_ids
    ]

    assigned_quantity = sum(
        donation["quantity_kg"]
        for donation in assigned_donations
    )

    received_count = len(donations)
    assigned_count = len(assigned_ids)
    unassigned_count = received_count - assigned_count

    #all unassigned donations contribute to food at risk
    at_risk_quantity = sum(
        donation["quantity_kg"]
        for donation in donations 
        if donation["donation_id"] not in assigned_ids
    )

    #Urgent donations are those shating the earlist expiry date
    if donations:
        earliest_expiry = min(
            donation["expiry_date"] for donation in donations
        )
        urgent_donations = [
            donation for donation in donations
            if donation["expiry_date"] == earliest_expiry
        ]
    else:
        urgent_donations = []

    urgent_ids = {
        donation["donation_id"]
        for donation in urgent_donations
    }
    urgent_assigned = len(urgent_ids & assigned_ids)

    urgent_rescue_rate = (
        100 * urgent_assigned / len(urgent_donations)
        if urgent_donations else 0.0
    )

    # Recipient capacity is the sum of initial capacities.
    recipient_capacity = sum(
        recipient["capacity_kg"] for recipient in recipients
    )

    recipient_utilization = (
        100 * assigned_quantity / recipient_capacity
        if recipient_capacity > 0 else 0.0
    )

    # Each volunteer can carry up to vehicle capacity per pickup.
    volunteer_capacity = sum(
        volunteer["vehicle_capacity_kg"] * volunteer["max_pickups"]
        for volunteer in volunteers
    )

    volunteer_utilization = (
        100 * assigned_quantity / volunteer_capacity
        if volunteer_capacity > 0 else 0.0
    )

    return {
        "donations_received": received_count,
        "donations_assigned": assigned_count,
        "donations_unassigned": unassigned_count,
        "food_quantity_rescued_kg": assigned_quantity,
        "food_quantity_at_risk_kg": at_risk_quantity,
        "urgent_rescue_rate_percent": urgent_rescue_rate,
        "recipient_capacity_utilization_percent": recipient_utilization,
        "volunteer_capacity_utilization_percent": volunteer_utilization,
    }

def compare_strategies(fifo_metrics, greedy_metrics):
    """
    Compare Greedy against FIFO.

    Positive differences favor Greedy; negative differences favor FIFO.
    """
    comparison_fields = {
        "donations_assigned": "donations_assigned",
        "food_quantity_rescued_kg": "food_quantity_rescued_kg",
        "urgent_rescue_rate_percent": "urgent_rescue_rate_percent",
        "recipient_capacity_utilization_percent":
            "recipient_capacity_utilization_percent",
        "volunteer_capacity_utilization_percent":
            "volunteer_capacity_utilization_percent",
    }

    return {
        metric: greedy_metrics[metric] - fifo_metrics[metric]
        for metric in comparison_fields
    }

def display_metrics(title, metrics):
    """Print a readable summary of the calculated metrics."""
    print(f"\n{'=' * 60}")
    print(title)
    print("=" * 60)

    print(f"Donations received: {metrics['donations_received']}")
    print(f"Donations assigned: {metrics['donations_assigned']}")
    print(f"Donations unassigned: {metrics['donations_unassigned']}")

    print(
        "Food quantity rescued: "
        f"{metrics['food_quantity_rescued_kg']:.2f} kg"
    )
    print(
        "Food quantity at risk: "
        f"{metrics['food_quantity_at_risk_kg']:.2f} kg"
    )

    print(
        "Urgent rescue rate: "
        f"{metrics['urgent_rescue_rate_percent']:.2f}%"
    )
    print(
        "Recipient capacity utilization: "
        f"{metrics['recipient_capacity_utilization_percent']:.2f}%"
    )
    print(
        "Volunteer capacity utilization: "
        f"{metrics['volunteer_capacity_utilization_percent']:.2f}%"
    )

def display_metrics(title, metrics):
    """Print a readable summary of the calculated metrics."""
    print(f"\n{'=' * 60}")
    print(title)
    print("=" * 60)

    print(f"Donations received: {metrics['donations_received']}")
    print(f"Donations assigned: {metrics['donations_assigned']}")
    print(f"Donations unassigned: {metrics['donations_unassigned']}")

    print(
        "Food quantity rescued: "
        f"{metrics['food_quantity_rescued_kg']:.2f} kg"
    )
    print(
        "Food quantity at risk: "
        f"{metrics['food_quantity_at_risk_kg']:.2f} kg"
    )

    print(
        "Urgent rescue rate: "
        f"{metrics['urgent_rescue_rate_percent']:.2f}%"
    )
    print(
        "Recipient capacity utilization: "
        f"{metrics['recipient_capacity_utilization_percent']:.2f}%"
    )
    print(
        "Volunteer capacity utilization: "
        f"{metrics['volunteer_capacity_utilization_percent']:.2f}%"
    )

def display_comparison(comparison):
    """Print the difference between Greedy and FIFO."""
    print(f"\n{'=' * 60}")
    print("GREEDY VS FIFO COMPARISON")
    print("=" * 60)

    for metric, difference in comparison.items():
        if metric.endswith("_kg"):
            print(f"{metric}: {difference:+.2f} kg")
        elif metric.endswith("_percent"):
            print(f"{metric}: {difference:+.2f} percentage points")
        else:
            print(f"{metric}: {difference:+.0f}")