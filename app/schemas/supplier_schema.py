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

"""Pydantic schemas for GDS supplier inventory models."""

from pydantic import BaseModel, Field


class SupplierInventory(BaseModel):
    """Base supplier inventory model."""

    supplier_name: str = Field(description="Name of the supplier")
    product_type: str = Field(
        description="Product type (flight, hotel, activity)"
    )
    route: str = Field(description="Route or location (e.g., 'BOM-DXB')")
    base_price: float = Field(description="Base price in local currency")
    availability: str = Field(description="Availability (high, medium, low)")
    commission_pct: float = Field(description="Commission percentage")
    api_endpoint: str = Field(
        description="API endpoint for booking this inventory"
    )


class FlightInventory(SupplierInventory):
    """Flight-specific inventory model."""

    booking_class: str = Field(
        description="Booking class (Y, W, C, F, etc.)"
    )
    carrier_code: str | None = Field(
        default=None, description="IATA carrier code (e.g., 'AI', 'EK')"
    )


class HotelInventory(SupplierInventory):
    """Hotel-specific inventory model."""

    room_type: str | None = Field(
        default=None, description="Room type (e.g., 'Deluxe', 'Suite')"
    )
    star_rating: float | None = Field(
        default=None, description="Hotel star rating (1-5)"
    )
    location: str | None = Field(
        default=None, description="Hotel location/address"
    )


class ActivityInventory(SupplierInventory):
    """Activity/tour-specific inventory model."""

    activity_type: str | None = Field(
        default=None, description="Type of activity (e.g., 'City Tour', 'Safari')"
    )
    duration_hours: float | None = Field(
        default=None, description="Activity duration in hours"
    )
