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

"""Mock GDS (Amadeus) search tool for supplier inventory.

MVP: Returns mock data. Future: Integrate real Amadeus API.
"""

from google.adk.tools import ToolContext


def search_gds_inventory(
    origin: str,
    destination: str,
    travel_date: str,
    product_type: str,
    tool_context: ToolContext,
) -> dict:
    """Search GDS for available supplier inventory.

    MVP: Returns MOCK data. Future: Integrate real Amadeus API.

    Args:
        origin: IATA code (e.g., "BOM" for Mumbai) or city name
        destination: IATA code (e.g., "DXB" for Dubai) or city name
        travel_date: ISO date (e.g., "2025-06-01") or "general" for no specific date
        product_type: "flight", "hotel", or "activity"
        tool_context: ADK tool context (required parameter)

    Returns:
        dict: {
            "status": "success",
            "suppliers": [
                {
                    "supplier_name": "Emirates",
                    "product_type": "flight",
                    "route": "BOM-DXB",
                    "base_fare": 25000,  # INR
                    "availability": "high",
                    "commission_pct": 5.0,
                    "booking_class": "Y",
                    "api_endpoint": "amadeus/v2/shopping/flight-offers"
                }
            ],
            "count": 15,
            "data_source": "mock"  # Will be "amadeus_live" when real API integrated
        }
    """
    # MVP: Return realistic mock data based on product type
    # TODO: Integrate real Amadeus Flight Offers Search API
    # https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search

    route = f"{origin}-{destination}"

    if product_type.lower() == "flight":
        mock_suppliers = [
            {
                "supplier_name": "Air India",
                "product_type": "flight",
                "route": route,
                "base_fare": 18500,
                "currency": "IDR",
                "availability": "high",
                "commission_pct": 7.0,
                "booking_class": "Y",
                "carrier_code": "AI",
                "api_endpoint": "amadeus/v2/shopping/flight-offers",
            },
            {
                "supplier_name": "Emirates",
                "product_type": "flight",
                "route": route,
                "base_fare": 25000,
                "currency": "IDR",
                "availability": "medium",
                "commission_pct": 5.0,
                "booking_class": "Y",
                "carrier_code": "EK",
                "api_endpoint": "amadeus/v2/shopping/flight-offers",
            },
            {
                "supplier_name": "IndiGo",
                "product_type": "flight",
                "route": route,
                "base_fare": 15000,
                "currency": "IDR",
                "availability": "high",
                "commission_pct": 8.0,
                "booking_class": "Y",
                "carrier_code": "6E",
                "api_endpoint": "amadeus/v2/shopping/flight-offers",
            },
            {
                "supplier_name": "Etihad Airways",
                "product_type": "flight",
                "route": route,
                "base_fare": 22000,
                "currency": "IDR",
                "availability": "medium",
                "commission_pct": 6.0,
                "booking_class": "Y",
                "carrier_code": "EY",
                "api_endpoint": "amadeus/v2/shopping/flight-offers",
            },
            {
                "supplier_name": "Qatar Airways",
                "product_type": "flight",
                "route": route,
                "base_fare": 24000,
                "currency": "IDR",
                "availability": "high",
                "commission_pct": 5.5,
                "booking_class": "Y",
                "carrier_code": "QR",
                "api_endpoint": "amadeus/v2/shopping/flight-offers",
            },
        ]
    elif product_type.lower() == "hotel":
        mock_suppliers = [
            {
                "supplier_name": "Marriott International",
                "product_type": "hotel",
                "route": destination,
                "base_fare": 8500,
                "currency": "IDR",
                "availability": "high",
                "commission_pct": 12.0,
                "room_type": "Deluxe Room",
                "star_rating": 5.0,
                "api_endpoint": "amadeus/v2/shopping/hotel-offers",
            },
            {
                "supplier_name": "Hilton Hotels",
                "product_type": "hotel",
                "route": destination,
                "base_fare": 7000,
                "currency": "IDR",
                "availability": "high",
                "commission_pct": 10.0,
                "room_type": "Standard Room",
                "star_rating": 4.5,
                "api_endpoint": "amadeus/v2/shopping/hotel-offers",
            },
            {
                "supplier_name": "Hyatt Hotels",
                "product_type": "hotel",
                "route": destination,
                "base_fare": 9000,
                "currency": "IDR",
                "availability": "medium",
                "commission_pct": 11.0,
                "room_type": "Suite",
                "star_rating": 5.0,
                "api_endpoint": "amadeus/v2/shopping/hotel-offers",
            },
        ]
    elif product_type.lower() == "activity":
        mock_suppliers = [
            {
                "supplier_name": "Viator",
                "product_type": "activity",
                "route": destination,
                "base_fare": 2500,
                "currency": "IDR",
                "availability": "high",
                "commission_pct": 15.0,
                "activity_type": "City Tour",
                "duration_hours": 4.0,
                "api_endpoint": "viator/activities/search",
            },
            {
                "supplier_name": "GetYourGuide",
                "product_type": "activity",
                "route": destination,
                "base_fare": 3000,
                "currency": "IDR",
                "availability": "high",
                "commission_pct": 14.0,
                "activity_type": "Desert Safari",
                "duration_hours": 6.0,
                "api_endpoint": "getyourguide/activities/search",
            },
        ]
    else:
        return {
            "status": "error",
            "error_message": f"Unknown product type: {product_type}. Must be 'flight', 'hotel', or 'activity'.",
            "suppliers": [],
            "count": 0,
        }

    return {
        "status": "success",
        "suppliers": mock_suppliers,
        "count": len(mock_suppliers),
        "data_source": "mock",
        "note": "Using mock data for MVP. Integrate Amadeus API for production.",
        "query": {
            "origin": origin,
            "destination": destination,
            "travel_date": travel_date,
            "product_type": product_type,
        },
    }
