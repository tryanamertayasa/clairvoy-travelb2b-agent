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

"""Airline fare rules and hotel cancellation policies.

MVP: Curated mock rules per carrier/fare class. Future: integrate the
Amadeus Fare Rules API for live rule retrieval.
"""

from google.adk.tools import ToolContext

AIRLINE_FARE_RULES: dict[str, dict] = {
    "SQ": {
        "airline": "Singapore Airlines",
        "currency": "IDR",
        "fare_classes": {
            "Y": {
                "fare_family": "Economy Flexi",
                "refundable": True,
                "refund_fee_idr": 0,
                "refund_penalty_pct": 0.0,
                "reschedulable": True,
                "reschedule_fee_idr": 0,
                "notes": "Fully refundable and changeable without fee; fare difference applies on reschedule.",
            },
            "M": {
                "fare_family": "Economy Standard",
                "refundable": True,
                "refund_fee_idr": 750000,
                "refund_penalty_pct": 0.0,
                "reschedulable": True,
                "reschedule_fee_idr": 500000,
                "notes": "Refund fee per passenger; fare difference applies on reschedule.",
            },
            "Q": {
                "fare_family": "Economy Lite",
                "refundable": False,
                "refund_fee_idr": 0,
                "refund_penalty_pct": 1.0,
                "reschedulable": True,
                "reschedule_fee_idr": 1000000,
                "notes": "Base fare non-refundable (taxes refundable); change fee per passenger plus fare difference.",
            },
        },
        "no_show_fee_idr": 1500000,
        "general_notes": [
            "Refunds processed to the original form of payment within 4-6 weeks.",
            "Unused airport taxes are refundable for all fare families.",
            "No-show converts the ticket to the no-show fee schedule.",
        ],
    },
    "GA": {
        "airline": "Garuda Indonesia",
        "currency": "IDR",
        "fare_classes": {
            "Y": {
                "fare_family": "Economy Flexible",
                "refundable": True,
                "refund_fee_idr": 0,
                "refund_penalty_pct": 0.05,
                "reschedulable": True,
                "reschedule_fee_idr": 0,
                "notes": "5% administration deduction on refund; free rebooking, fare difference applies.",
            },
            "Q": {
                "fare_family": "Economy Promo",
                "refundable": True,
                "refund_fee_idr": 0,
                "refund_penalty_pct": 0.5,
                "reschedulable": True,
                "reschedule_fee_idr": 600000,
                "notes": "50% cancellation penalty on base fare; change fee per passenger plus fare difference.",
            },
        },
        "no_show_fee_idr": 1000000,
        "general_notes": [
            "Refund requests must be filed before first-segment departure to avoid no-show penalty.",
        ],
    },
    "AI": {
        "airline": "Air India",
        "currency": "IDR",
        "fare_classes": {
            "Y": {
                "fare_family": "Economy Comfort",
                "refundable": True,
                "refund_fee_idr": 500000,
                "refund_penalty_pct": 0.0,
                "reschedulable": True,
                "reschedule_fee_idr": 400000,
                "notes": "Flat fees per passenger; fare difference applies on reschedule.",
            },
        },
        "no_show_fee_idr": 900000,
        "general_notes": [],
    },
    "EK": {
        "airline": "Emirates",
        "currency": "IDR",
        "fare_classes": {
            "Y": {
                "fare_family": "Economy Flex",
                "refundable": True,
                "refund_fee_idr": 600000,
                "refund_penalty_pct": 0.0,
                "reschedulable": True,
                "reschedule_fee_idr": 450000,
                "notes": "Flat fees per passenger; fare difference applies on reschedule.",
            },
            "Q": {
                "fare_family": "Economy Special",
                "refundable": False,
                "refund_fee_idr": 0,
                "refund_penalty_pct": 1.0,
                "reschedulable": True,
                "reschedule_fee_idr": 1200000,
                "notes": "Base fare non-refundable (taxes refundable); change fee per passenger.",
            },
        },
        "no_show_fee_idr": 1600000,
        "general_notes": [],
    },
    "6E": {
        "airline": "IndiGo",
        "currency": "IDR",
        "fare_classes": {
            "Y": {
                "fare_family": "Saver",
                "refundable": True,
                "refund_fee_idr": 0,
                "refund_penalty_pct": 0.4,
                "reschedulable": True,
                "reschedule_fee_idr": 350000,
                "notes": "40% cancellation penalty on base fare; change fee per passenger.",
            },
        },
        "no_show_fee_idr": 700000,
        "general_notes": [],
    },
    "EY": {
        "airline": "Etihad Airways",
        "currency": "IDR",
        "fare_classes": {
            "Y": {
                "fare_family": "Economy Comfort",
                "refundable": True,
                "refund_fee_idr": 550000,
                "refund_penalty_pct": 0.0,
                "reschedulable": True,
                "reschedule_fee_idr": 500000,
                "notes": "Flat fees per passenger; fare difference applies on reschedule.",
            },
        },
        "no_show_fee_idr": 1400000,
        "general_notes": [],
    },
    "QR": {
        "airline": "Qatar Airways",
        "currency": "IDR",
        "fare_classes": {
            "Y": {
                "fare_family": "Economy Classic",
                "refundable": True,
                "refund_fee_idr": 650000,
                "refund_penalty_pct": 0.0,
                "reschedulable": True,
                "reschedule_fee_idr": 500000,
                "notes": "Flat fees per passenger; fare difference applies on reschedule.",
            },
        },
        "no_show_fee_idr": 1500000,
        "general_notes": [],
    },
}

AIRLINE_NAME_TO_CODE: dict[str, str] = {
    "singapore airlines": "SQ",
    "garuda": "GA",
    "garuda indonesia": "GA",
    "air india": "AI",
    "emirates": "EK",
    "indigo": "6E",
    "etihad": "EY",
    "etihad airways": "EY",
    "qatar": "QR",
    "qatar airways": "QR",
}

HOTEL_CANCELLATION_POLICIES: dict[str, dict] = {
    "Marriott International": {
        "currency": "IDR",
        "free_cancellation_days_before_checkin": 3,
        "late_cancellation_penalty_nights": 1,
        "no_show_penalty_nights": 1,
        "reschedule_fee_idr": 0,
        "notes": "Free cancellation until 3 days before check-in; afterwards one night per room is charged. Date changes free, subject to rate difference.",
    },
    "Hilton Hotels": {
        "currency": "IDR",
        "free_cancellation_days_before_checkin": 2,
        "late_cancellation_penalty_nights": 1,
        "no_show_penalty_nights": 1,
        "reschedule_fee_idr": 0,
        "notes": "Free cancellation until 2 days before check-in; afterwards one night per room is charged.",
    },
    "Hyatt Hotels": {
        "currency": "IDR",
        "free_cancellation_days_before_checkin": 3,
        "late_cancellation_penalty_nights": 2,
        "no_show_penalty_nights": 2,
        "reschedule_fee_idr": 250000,
        "notes": "Free cancellation until 3 days before check-in; afterwards two nights per room; date-change fee per booking plus rate difference.",
    },
}


def resolve_airline_code(airline: str) -> str | None:
    """Resolves an airline name or IATA code to a known carrier code."""
    query = airline.strip()
    if query.upper() in AIRLINE_FARE_RULES:
        return query.upper()
    return AIRLINE_NAME_TO_CODE.get(query.lower())


def get_fare_rules(airline: str, tool_context: ToolContext) -> dict:
    """Get refund and reschedule fare rules for an airline.

    Use this tool when the user asks about an airline's refund, cancellation,
    or reschedule (rebooking/change) rules, or when estimating refund or
    reschedule costs from ticket details. Rules are returned per fare class
    with fees, penalty percentages, and no-show conditions.

    Args:
        airline (str): IATA carrier code (e.g., "SQ", "GA") or airline name
            (e.g., "Singapore Airlines").

    Returns:
        dict: {
            "status": "success",
            "carrier_code": str,
            "airline": str,
            "currency": "IDR",
            "fare_classes": {class_code: rule dict},
            "no_show_fee_idr": int,
            "general_notes": [str],
            "data_source": "curated_rules"
        }
        On unknown airlines, returns status "not_found" with supported carriers.
    """
    code = resolve_airline_code(airline)
    if code is None:
        return {
            "status": "not_found",
            "error_message": f"No fare rules on file for '{airline}'.",
            "supported_carriers": {
                c: r["airline"] for c, r in AIRLINE_FARE_RULES.items()
            },
        }

    rules = AIRLINE_FARE_RULES[code]
    return {
        "status": "success",
        "carrier_code": code,
        "airline": rules["airline"],
        "currency": rules["currency"],
        "fare_classes": rules["fare_classes"],
        "no_show_fee_idr": rules["no_show_fee_idr"],
        "general_notes": rules["general_notes"],
        "data_source": "curated_rules",
        "note": "Curated sample rules for MVP. Integrate Amadeus Fare Rules API for live data.",
    }


def get_hotel_policy(hotel: str, tool_context: ToolContext) -> dict:
    """Get the cancellation and date-change policy for a hotel chain.

    Use this tool when the user asks about hotel refund/cancellation rules or
    when estimating a hotel refund.

    Args:
        hotel (str): Hotel chain name (e.g., "Marriott International", "Hilton
            Hotels", "Hyatt Hotels").

    Returns:
        dict: {
            "status": "success",
            "hotel": str,
            "policy": {free-cancellation window, late penalty nights, fees},
            "data_source": "curated_rules"
        }
        On unknown hotels, returns status "not_found" with supported chains.
    """
    query = hotel.strip().lower()
    match = next(
        (
            name
            for name in HOTEL_CANCELLATION_POLICIES
            if query in name.lower() or name.lower() in query
        ),
        None,
    )
    if match is None:
        return {
            "status": "not_found",
            "error_message": f"No cancellation policy on file for '{hotel}'.",
            "supported_hotels": list(HOTEL_CANCELLATION_POLICIES),
        }

    return {
        "status": "success",
        "hotel": match,
        "policy": HOTEL_CANCELLATION_POLICIES[match],
        "data_source": "curated_rules",
    }
