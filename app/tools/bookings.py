# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Mock booking store and refund/reschedule calculator.

MVP: In-memory sample bookings with deterministic per-supplier settlement
math. Future: integrate the real order-management system and supplier APIs.
"""

from datetime import date, datetime

from google.adk.tools import ToolContext

from .fares import AIRLINE_FARE_RULES, HOTEL_CANCELLATION_POLICIES

BOOKING_STORE: dict[str, dict] = {
    "CLV-2026-0001": {
        "client_name": "Wanderlust OTA",
        "status": "confirmed",
        "currency": "IDR",
        "items": [
            {
                "type": "flight",
                "supplier": "Singapore Airlines",
                "carrier_code": "SQ",
                "route": "CGK-SIN",
                "travel_date": "2026-08-15",
                "fare_class": "M",
                "passengers": 2,
                "base_fare_idr": 3500000,
                "taxes_idr": 800000,
            },
            {
                "type": "flight",
                "supplier": "Garuda Indonesia",
                "carrier_code": "GA",
                "route": "SIN-CGK",
                "travel_date": "2026-08-20",
                "fare_class": "Q",
                "passengers": 2,
                "base_fare_idr": 2800000,
                "taxes_idr": 700000,
            },
        ],
    },
    "CLV-2026-0002": {
        "client_name": "Wanderlust OTA",
        "status": "confirmed",
        "currency": "IDR",
        "items": [
            {
                "type": "flight",
                "supplier": "Singapore Airlines",
                "carrier_code": "SQ",
                "route": "CGK-SIN",
                "travel_date": "2026-08-15",
                "fare_class": "Q",
                "passengers": 2,
                "base_fare_idr": 2400000,
                "taxes_idr": 750000,
            },
            {
                "type": "hotel",
                "supplier": "Marriott International",
                "property": "Marriott Marina Bay",
                "check_in": "2026-08-15",
                "nights": 3,
                "rooms": 1,
                "rate_per_night_idr": 4200000,
            },
        ],
    },
}


def _flight_paid(item: dict) -> int:
    return (item["base_fare_idr"] + item["taxes_idr"]) * item["passengers"]


def _hotel_paid(item: dict) -> int:
    return item["rate_per_night_idr"] * item["nights"] * item["rooms"]


def _item_paid(item: dict) -> int:
    return _flight_paid(item) if item["type"] == "flight" else _hotel_paid(item)


def _settle_flight(item: dict, action: str) -> dict:
    carrier = AIRLINE_FARE_RULES.get(item["carrier_code"])
    if carrier is None or item["fare_class"] not in carrier["fare_classes"]:
        return {
            "status": "error",
            "error_message": f"No fare rules for {item['carrier_code']} class {item['fare_class']}.",
        }

    rule = carrier["fare_classes"][item["fare_class"]]
    pax = item["passengers"]
    paid = _flight_paid(item)

    if action == "refund":
        if not rule["refundable"]:
            penalty = item["base_fare_idr"] * pax
            refund = item["taxes_idr"] * pax
            rule_applied = (
                f"{rule['fare_family']}: base fare non-refundable; taxes refunded"
            )
        else:
            per_pax_penalty = rule["refund_fee_idr"] + round(
                item["base_fare_idr"] * rule["refund_penalty_pct"]
            )
            penalty = per_pax_penalty * pax
            refund = paid - penalty
            rule_applied = (
                f"{rule['fare_family']}: refund fee IDR {rule['refund_fee_idr']:,} "
                f"+ {rule['refund_penalty_pct']:.0%} of base fare, per passenger"
            )
        return {
            "status": "success",
            "paid_idr": paid,
            "penalty_idr": penalty,
            "refund_due_idr": refund,
            "rule_applied": rule_applied,
        }

    fee = rule["reschedule_fee_idr"] * pax
    return {
        "status": "success",
        "paid_idr": paid,
        "penalty_idr": fee,
        "refund_due_idr": 0,
        "rule_applied": (
            f"{rule['fare_family']}: change fee IDR {rule['reschedule_fee_idr']:,} "
            "per passenger; fare difference for the new date applies on top"
        ),
    }


def _settle_hotel(item: dict, action: str, as_of: date) -> dict:
    policy = HOTEL_CANCELLATION_POLICIES.get(item["supplier"])
    if policy is None:
        return {
            "status": "error",
            "error_message": f"No cancellation policy for {item['supplier']}.",
        }

    paid = _hotel_paid(item)

    if action == "reschedule":
        fee = policy["reschedule_fee_idr"]
        return {
            "status": "success",
            "paid_idr": paid,
            "penalty_idr": fee,
            "refund_due_idr": 0,
            "rule_applied": (
                f"Date change fee IDR {fee:,}; rate difference for new dates applies on top"
                if fee
                else "Free date change; rate difference for new dates applies"
            ),
        }

    check_in = date.fromisoformat(item["check_in"])
    days_until = (check_in - as_of).days
    free_window = policy["free_cancellation_days_before_checkin"]

    if days_until >= free_window:
        return {
            "status": "success",
            "paid_idr": paid,
            "penalty_idr": 0,
            "refund_due_idr": paid,
            "rule_applied": (
                f"Cancelled {days_until} days before check-in (free window is "
                f">= {free_window} days): full refund"
            ),
        }

    penalty_nights = min(policy["late_cancellation_penalty_nights"], item["nights"])
    penalty = item["rate_per_night_idr"] * penalty_nights * item["rooms"]
    return {
        "status": "success",
        "paid_idr": paid,
        "penalty_idr": penalty,
        "refund_due_idr": paid - penalty,
        "rule_applied": (
            f"Cancelled {days_until} days before check-in (inside the "
            f"{free_window}-day window): {penalty_nights} night(s) per room charged"
        ),
    }


def _item_label(item: dict) -> str:
    if item["type"] == "flight":
        return f"{item['supplier']} ({item['carrier_code']}) {item['route']} class {item['fare_class']}"
    return f"{item['supplier']} - {item['property']}, {item['nights']} night(s)"


def lookup_booking(booking_reference: str, tool_context: ToolContext) -> dict:
    """Look up a booking by its reference to see what was purchased.

    Use this tool before calculating refunds or reschedule costs, so the
    calculation runs against the actual booked items (flights per supplier
    airline, hotels).

    Args:
        booking_reference (str): Booking reference, e.g. "CLV-2026-0001".

    Returns:
        dict: {
            "status": "success",
            "booking_reference": str,
            "booking": {client, status, currency, items with fares/rates},
            "total_paid_idr": int
        }
        On unknown references, returns status "not_found" with the list of
        available sample references.
    """
    reference = booking_reference.strip().upper()
    booking = BOOKING_STORE.get(reference)
    if booking is None:
        return {
            "status": "not_found",
            "error_message": f"No booking found for '{booking_reference}'.",
            "available_references": list(BOOKING_STORE),
            "note": "Mock booking store for MVP. Ask the user for a valid reference or use one of the sample references.",
        }

    return {
        "status": "success",
        "booking_reference": reference,
        "booking": booking,
        "total_paid_idr": sum(_item_paid(item) for item in booking["items"]),
        "data_source": "mock_booking_store",
    }


def calculate_settlement(
    booking_reference: str,
    action: str,
    as_of_date: str,
    tool_context: ToolContext,
) -> dict:
    """Calculate refund or reschedule costs for a booking, split per supplier.

    Use this tool when the user asks how much a refund or reschedule will
    cost for a booking. It applies each supplier's fare rules or cancellation
    policy deterministically and returns the amount paid, penalty, and refund
    due per supplier (airlines and hotels separately), plus booking totals.

    Args:
        booking_reference (str): Booking reference, e.g. "CLV-2026-0001".
        action (str): "refund" to cancel for a refund, or "reschedule" to
            change dates.
        as_of_date (str): Date the request is made, ISO format (e.g.
            "2026-08-10"), or "today" for the current date. Determines hotel
            cancellation windows.

    Returns:
        dict: {
            "status": "success",
            "action": str,
            "currency": "IDR",
            "per_supplier": [
                {supplier, item, type, paid_idr, penalty_idr, refund_due_idr, rule_applied}
            ],
            "totals": {"paid_idr", "penalty_idr", "refund_due_idr"},
            "notes": [str]
        }
    """
    normalized_action = action.strip().lower()
    if normalized_action not in ("refund", "reschedule"):
        return {
            "status": "error",
            "error_message": f"Unknown action '{action}'. Use 'refund' or 'reschedule'.",
        }

    reference = booking_reference.strip().upper()
    booking = BOOKING_STORE.get(reference)
    if booking is None:
        return {
            "status": "not_found",
            "error_message": f"No booking found for '{booking_reference}'.",
            "available_references": list(BOOKING_STORE),
        }

    as_of_query = as_of_date.strip().lower()
    try:
        as_of = (
            datetime.now().date()
            if as_of_query == "today"
            else date.fromisoformat(as_of_query)
        )
    except ValueError:
        return {
            "status": "error",
            "error_message": f"Invalid as_of_date '{as_of_date}'. Use ISO format YYYY-MM-DD or 'today'.",
        }

    per_supplier: list[dict] = []
    notes: list[str] = []
    for item in booking["items"]:
        if item["type"] == "flight":
            settled = _settle_flight(item, normalized_action)
        else:
            settled = _settle_hotel(item, normalized_action, as_of)

        if settled["status"] != "success":
            notes.append(settled["error_message"])
            continue

        per_supplier.append(
            {
                "supplier": item["supplier"],
                "item": _item_label(item),
                "type": item["type"],
                "paid_idr": settled["paid_idr"],
                "penalty_idr": settled["penalty_idr"],
                "refund_due_idr": settled["refund_due_idr"],
                "rule_applied": settled["rule_applied"],
            }
        )

    if normalized_action == "reschedule":
        notes.append(
            "Reschedule penalties are change fees only; fare/rate differences for the new dates are charged additionally."
        )
    notes.append("Mock data for MVP: rules and bookings are curated samples.")

    return {
        "status": "success",
        "action": normalized_action,
        "booking_reference": reference,
        "currency": booking["currency"],
        "as_of_date": as_of.isoformat(),
        "per_supplier": per_supplier,
        "totals": {
            "paid_idr": sum(entry["paid_idr"] for entry in per_supplier),
            "penalty_idr": sum(entry["penalty_idr"] for entry in per_supplier),
            "refund_due_idr": sum(entry["refund_due_idr"] for entry in per_supplier),
        },
        "notes": notes,
    }
