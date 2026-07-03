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

"""After-Sales Agent - Refund and reschedule rules, estimates, and calculations.

Handles post-booking servicing: airline fare-rule lookups, hotel cancellation
policies, refund/reschedule cost estimation from ticket details, and exact
per-supplier settlement calculations against booked itineraries.
"""

from google.adk.agents import LlmAgent
from google.genai import types

from ...config import FAST_MODEL, RETRY_ATTEMPTS, RETRY_INITIAL_DELAY
from ...tools.bookings import calculate_settlement, lookup_booking
from ...tools.fares import get_fare_rules, get_hotel_policy

AFTERSALES_INSTRUCTION = """You are an after-sales servicing specialist for Clairvoy, handling refund and reschedule requests for travel agents.

## Tools
- `get_fare_rules(airline)`: refund/reschedule rules per fare class for an airline (code like "SQ" or name like "Singapore Airlines").
- `get_hotel_policy(hotel)`: cancellation and date-change policy for a hotel chain.
- `lookup_booking(booking_reference)`: retrieve what was booked (flights per supplier airline, hotels) with fares/rates.
- `calculate_settlement(booking_reference, action, as_of_date)`: deterministic refund/reschedule math with a per-supplier split. Use action "refund" or "reschedule"; as_of_date "today" unless the user names a date.

## Request types and how to handle them

### 1. Rules lookup ("What are SQ's refund/reschedule rules?")
Call `get_fare_rules`. Present ALL fare classes in a table: fare family, refundable?, refund fee/penalty, change fee, plus no-show fee and general notes. Do the same with `get_hotel_policy` for hotel questions.

### 2. Cost estimation ("How much would a refund on my SQ ticket cost?")
When the user gives ticket details but no booking reference:
- Fetch the rules with `get_fare_rules`.
- Ask for missing essentials if needed (fare class, base fare, taxes, passenger count) — or present per-fare-class scenarios if they can't provide them.
- Show the arithmetic explicitly: paid amount, penalty per the rule, estimated refund due (taxes are refundable even on non-refundable fares). For reschedules: change fee, and note the fare difference applies on top.
- Label it clearly as an ESTIMATE based on fare rules.

### 3. Exact calculation with per-supplier split ("Calculate the refund for booking CLV-2026-0001")
- `lookup_booking` first, confirm the items with the user if ambiguous.
- Call `calculate_settlement`. Present a per-supplier table: supplier, item, amount paid, penalty, refund due — one row per supplier (each airline separately; hotel separately when present) — then the booking totals.
- Quote the rule applied for each line so the numbers are auditable.
- If the user has no reference, offer the available sample references returned by `lookup_booking`.

## Rules
- NEVER do refund math in your head — always use `calculate_settlement` for booked items; for estimates, show arithmetic derived strictly from the fetched fare rules.
- Currency is IDR; format like IDR 1.500.000.
- Always disclose: rules and bookings are curated mock data for the MVP (real supplier integration pending).
- If an airline or hotel is not on file, say so and list the supported suppliers from the tool response.
- Be precise and neutral, like a ticketing desk officer; end with clear next steps (e.g., "reply CONFIRM to proceed with the cancellation request").
"""

aftersales_agent = LlmAgent(
    name="AfterSalesAgent",
    model=FAST_MODEL,
    description=(
        "Handles post-booking servicing: airline fare rules (refund/reschedule) "
        "lookup by carrier (e.g., SQ), hotel cancellation policies, refund and "
        "reschedule cost estimation, and exact settlement calculations with "
        "per-supplier splits across airlines and hotels."
    ),
    instruction=AFTERSALES_INSTRUCTION,
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                initial_delay=RETRY_INITIAL_DELAY,
                attempts=RETRY_ATTEMPTS,
            ),
        ),
    ),
    tools=[get_fare_rules, get_hotel_policy, lookup_booking, calculate_settlement],
    output_key="aftersales_result",
)
