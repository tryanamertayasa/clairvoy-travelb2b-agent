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

"""Intake Agent - Parses B2B travel demand requests.

This agent parses B2B travel demand inquiries and extracts structured
parameters (client name, POS markets, routes, products, commercial terms)
into session state for use by subsequent agents.
"""

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

from ...config import FAST_MODEL, RETRY_ATTEMPTS, RETRY_INITIAL_DELAY
from ...schemas.demand_schema import B2BDemandRequest


def after_intake(callback_context: CallbackContext) -> types.Content | None:
    """After intake, copy the parsed B2B demand to state for other agents."""
    parsed = callback_context.state.get("parsed_request", {})

    # Extract fields from B2BDemandRequest
    if isinstance(parsed, dict):
        callback_context.state["client_name"] = parsed.get("client_name", "")
        callback_context.state["pos_markets"] = parsed.get("pos_markets", [])
        callback_context.state["routes"] = parsed.get("routes", [])
        callback_context.state["product_types"] = parsed.get("product_types", [])
        callback_context.state["commercial_needs"] = parsed.get(
            "commercial_needs", {}
        )
        callback_context.state["additional_context"] = parsed.get(
            "additional_context", ""
        )
    elif hasattr(parsed, "client_name"):
        # Handle Pydantic model
        callback_context.state["client_name"] = parsed.client_name
        callback_context.state["pos_markets"] = parsed.pos_markets
        callback_context.state["routes"] = [
            route.model_dump() if hasattr(route, "model_dump") else route
            for route in parsed.routes
        ]
        callback_context.state["product_types"] = parsed.product_types
        callback_context.state["commercial_needs"] = (
            parsed.commercial_needs.model_dump()
            if hasattr(parsed.commercial_needs, "model_dump")
            else parsed.commercial_needs
        )
        callback_context.state["additional_context"] = (
            parsed.additional_context or ""
        )

    # Track intake stage completion
    stages = callback_context.state.get("stages_completed", [])
    stages.append("intake")
    callback_context.state["stages_completed"] = stages

    return None


INTAKE_INSTRUCTION = """You are a B2B demand parser for a travel consolidation platform.

Your task is to extract structured B2B partnership requirements from client inquiries.

## Examples

User: "We're a Singapore-based OTA looking for flight inventory on India-Dubai routes with NET pricing"
→ client_name: "Singapore OTA"
→ pos_markets: ["Singapore"]
→ routes: [{"origin": "India", "destination": "Dubai", "travel_dates": null}]
→ product_types: ["flights"]
→ commercial_needs: {"preferred_margin_type": "NET rates"}

User: "Dubai travel agency needs hotel + activity suppliers for Southeast Asia, payment NET 30"
→ client_name: "Dubai travel agency"
→ pos_markets: ["Dubai", "UAE"]
→ routes: [{"origin": "UAE", "destination": "Southeast Asia", "travel_dates": null}]
→ product_types: ["hotels", "activities"]
→ commercial_needs: {"payment_terms": "NET 30"}

User: "Looking for Mumbai-Dubai flight inventory, we operate in India and Middle East"
→ client_name: "Unknown OTA"
→ pos_markets: ["India", "Middle East"]
→ routes: [{"origin": "Mumbai", "destination": "Dubai", "travel_dates": null}]
→ product_types: ["flights"]

User: "We need comprehensive travel packages for India-UAE routes, 10k bookings monthly"
→ client_name: "Unknown TMC"
→ pos_markets: ["India", "UAE"]
→ routes: [{"origin": "India", "destination": "UAE", "travel_dates": null}]
→ product_types: ["flights", "hotels", "activities"]
→ commercial_needs: {"volume_commitment": "10,000 bookings per month"}

## Instructions
1. Identify the client/company making the inquiry (or "Unknown OTA/TMC" if not specified)
2. Extract their Point-of-Sale markets (countries/regions where they sell travel)
3. Identify routes/destinations they're interested in (origin-destination pairs)
4. Determine product types needed (flights, hotels, activities, packages)
5. Note commercial requirements (payment terms, pricing type, volume commitments)
6. Capture any additional context or special requirements

If information is unclear, make reasonable inferences based on context.
"""

intake_agent = LlmAgent(
    name="IntakeAgent",
    model=FAST_MODEL,
    description="Parses B2B travel demand to extract client info, POS markets, routes, products, and commercial terms",
    instruction=INTAKE_INSTRUCTION,
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                initial_delay=RETRY_INITIAL_DELAY,
                attempts=RETRY_ATTEMPTS,
            ),
        ),
    ),
    output_schema=B2BDemandRequest,
    output_key="parsed_request",
    after_agent_callback=after_intake,
)
