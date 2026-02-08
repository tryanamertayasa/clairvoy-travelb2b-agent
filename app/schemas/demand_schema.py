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

"""Pydantic schemas for B2B travel demand intake."""

from pydantic import BaseModel, Field


class RouteRequest(BaseModel):
    """Single route request (origin-destination pair)."""

    origin: str = Field(
        description="Origin airport/city code (e.g., 'BOM', 'Mumbai')"
    )
    destination: str = Field(
        description="Destination airport/city code (e.g., 'DXB', 'Dubai')"
    )
    travel_dates: list[str] | None = Field(
        default=None,
        description="Preferred travel dates (ISO format) or None for general inquiry",
    )


class CommercialTerms(BaseModel):
    """Commercial requirements for the partnership."""

    payment_terms: str | None = Field(
        default=None,
        description="Payment terms (e.g., 'NET 30', 'prepaid', 'credit line')",
    )
    volume_commitment: str | None = Field(
        default=None, description="Expected monthly transaction volume"
    )
    preferred_margin_type: str | None = Field(
        default=None,
        description="Pricing type (e.g., 'NET rates', 'commission-based', 'markup')",
    )


class B2BDemandRequest(BaseModel):
    """Structured output for parsing B2B travel demand inquiry."""

    client_name: str = Field(
        description="Name of the OTA/TMC/travel company making the inquiry"
    )
    pos_markets: list[str] = Field(
        description="Point-of-Sale markets (countries/regions where they operate, e.g., ['India', 'UAE', 'Singapore'])"
    )
    routes: list[RouteRequest] = Field(
        description="Origin-destination route pairs they're interested in"
    )
    product_types: list[str] = Field(
        description="Product types needed (e.g., ['flights', 'hotels', 'activities'])"
    )
    commercial_needs: CommercialTerms = Field(
        description="Commercial and payment terms requirements"
    )
    additional_context: str | None = Field(
        default=None,
        description="Any additional context, special requirements, or notes",
    )
