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

"""Pydantic schemas for API distribution package models."""

from pydantic import BaseModel, Field


class APIEndpoint(BaseModel):
    """Single API endpoint specification."""

    method: str = Field(description="HTTP method (POST, GET, PUT, DELETE)")
    path: str = Field(description="API path (e.g., '/api/v1/flights/search')")
    description: str = Field(description="What this endpoint does")
    request_example: dict = Field(description="Sample request payload")
    response_example: dict = Field(description="Sample response payload")


class RateLimitConfig(BaseModel):
    """Rate limiting configuration."""

    requests_per_minute: int = Field(description="Max requests per minute")
    burst_limit: int = Field(description="Burst allowance")


class WhiteLabelConfig(BaseModel):
    """White-label customization options."""

    custom_domain_available: bool = Field(
        description="Can client use custom domain?"
    )
    branded_responses: bool = Field(
        description="Can customize response formats?"
    )
    custom_error_messages: bool = Field(
        description="Can customize error messages?"
    )


class SandboxConfig(BaseModel):
    """Sandbox environment details."""

    sandbox_url: str = Field(description="Sandbox API base URL")
    test_credentials: dict = Field(description="Test API credentials")
    test_data_available: bool = Field(description="Is test data available?")


class DistributionPackage(BaseModel):
    """Technical integration package for B2B client."""

    api_endpoints: list[APIEndpoint] = Field(
        description="Available API endpoints (Search, Book, Ticket, Refund)"
    )
    authentication_method: str = Field(
        description="Auth method (OAuth2, API Key, JWT)"
    )
    rate_limits: RateLimitConfig = Field(
        description="Rate limiting and quota configuration"
    )
    white_label_options: WhiteLabelConfig = Field(
        description="White-label customization capabilities"
    )
    integration_timeline: str = Field(
        description="Estimated integration timeline (e.g., '2 weeks', '1 month')"
    )
    sandbox_environment: SandboxConfig = Field(
        description="Sandbox environment for testing"
    )
    documentation_url: str = Field(description="Link to API documentation")
