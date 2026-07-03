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

"""Unit tests for the itinerary catalog and after-sales settlement tools."""

from app.tools.bookings import calculate_settlement, lookup_booking
from app.tools.destinations import get_destination_guide, search_destinations
from app.tools.fares import get_fare_rules, get_hotel_policy


class TestDestinationCatalog:
    def test_sakura_theme_returns_japan_and_korea(self):
        result = search_destinations("sakura", "any", "any", None)
        assert result["status"] == "success"
        names = {d["name"] for d in result["destinations"]}
        assert "Tokyo & Kyoto" in names
        assert "Seoul" in names

    def test_spring_family_filter(self):
        result = search_destinations("spring", "spring", "family", None)
        names = {d["name"] for d in result["destinations"]}
        assert "Melbourne" in names

    def test_korea_alias_resolves_to_seoul(self):
        result = get_destination_guide("Korea", None)
        assert result["status"] == "success"
        assert result["guides"][0]["name"] == "Seoul"

    def test_europe_returns_multi_city_guides(self):
        result = get_destination_guide("Europe", None)
        assert result["status"] == "success"
        assert result["count"] >= 2

    def test_guides_carry_prices_for_cost_breakdowns(self):
        result = get_destination_guide("Bali", None)
        guide = result["guides"][0]
        assert all("price_idr" in a for a in guide["activities"])
        assert all("price_idr_per_night" in h for h in guide["hotels"])
        assert {"budget", "mid", "luxury"} <= set(guide["daily_food_cost_idr"])

    def test_unknown_destination_reports_alternatives(self):
        result = get_destination_guide("Atlantis", None)
        assert result["status"] == "not_found"
        assert result["available_destinations"]


class TestFareRules:
    def test_sq_rules_by_code(self):
        result = get_fare_rules("SQ", None)
        assert result["status"] == "success"
        assert result["airline"] == "Singapore Airlines"
        assert {"Y", "M", "Q"} <= set(result["fare_classes"])
        assert result["fare_classes"]["Q"]["refundable"] is False

    def test_sq_rules_by_name(self):
        result = get_fare_rules("Singapore Airlines", None)
        assert result["carrier_code"] == "SQ"

    def test_unknown_airline(self):
        result = get_fare_rules("ZZ Unknown Air", None)
        assert result["status"] == "not_found"
        assert "SQ" in result["supported_carriers"]

    def test_hotel_policy_partial_match(self):
        result = get_hotel_policy("Marriott", None)
        assert result["status"] == "success"
        assert result["policy"]["free_cancellation_days_before_checkin"] == 3


class TestSettlementCalculation:
    def test_lookup_known_booking(self):
        result = lookup_booking("CLV-2026-0001", None)
        assert result["status"] == "success"
        assert result["total_paid_idr"] == 15_600_000

    def test_lookup_unknown_booking_lists_references(self):
        result = lookup_booking("NOPE-123", None)
        assert result["status"] == "not_found"
        assert "CLV-2026-0001" in result["available_references"]

    def test_refund_split_airlines_only(self):
        result = calculate_settlement("CLV-2026-0001", "refund", "2026-08-01", None)
        assert result["status"] == "success"
        by_supplier = {e["supplier"]: e for e in result["per_supplier"]}

        sq = by_supplier["Singapore Airlines"]
        assert sq["paid_idr"] == 8_600_000
        assert sq["penalty_idr"] == 1_500_000
        assert sq["refund_due_idr"] == 7_100_000

        ga = by_supplier["Garuda Indonesia"]
        assert ga["paid_idr"] == 7_000_000
        assert ga["penalty_idr"] == 2_800_000
        assert ga["refund_due_idr"] == 4_200_000

        assert result["totals"] == {
            "paid_idr": 15_600_000,
            "penalty_idr": 4_300_000,
            "refund_due_idr": 11_300_000,
        }

    def test_reschedule_split_airlines_only(self):
        result = calculate_settlement("CLV-2026-0001", "reschedule", "today", None)
        by_supplier = {e["supplier"]: e for e in result["per_supplier"]}
        assert by_supplier["Singapore Airlines"]["penalty_idr"] == 1_000_000
        assert by_supplier["Garuda Indonesia"]["penalty_idr"] == 1_200_000
        assert result["totals"]["refund_due_idr"] == 0

    def test_refund_split_airline_and_hotel_free_window(self):
        result = calculate_settlement("CLV-2026-0002", "refund", "2026-08-01", None)
        by_supplier = {e["supplier"]: e for e in result["per_supplier"]}

        sq = by_supplier["Singapore Airlines"]
        assert sq["penalty_idr"] == 4_800_000
        assert sq["refund_due_idr"] == 1_500_000

        hotel = by_supplier["Marriott International"]
        assert hotel["type"] == "hotel"
        assert hotel["penalty_idr"] == 0
        assert hotel["refund_due_idr"] == 12_600_000

    def test_refund_split_hotel_late_cancellation(self):
        result = calculate_settlement("CLV-2026-0002", "refund", "2026-08-14", None)
        hotel = next(e for e in result["per_supplier"] if e["type"] == "hotel")
        assert hotel["penalty_idr"] == 4_200_000
        assert hotel["refund_due_idr"] == 8_400_000

    def test_invalid_action(self):
        result = calculate_settlement("CLV-2026-0001", "cancelamundo", "today", None)
        assert result["status"] == "error"

    def test_invalid_date(self):
        result = calculate_settlement("CLV-2026-0001", "refund", "next tuesday", None)
        assert result["status"] == "error"
