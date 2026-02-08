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

"""Sub-agents for Clairvoy B2B Travel Consolidator.

This module exports all specialized agents:
0. IntakeAgent - Parses B2B demand (client, POS, routes, products, commercial needs)
1. ValidationAgent - Validates partnership feasibility, risk, and pricing (AI-only)
2. MatchingAgent - Searches GDS for supplier inventory (Amadeus mock)
3. ConsolidatorAgent - Aggregates inventory and calculates GMV potential
4. DistributionAgent - Designs API integration packages
5. ReportGeneratorAgent - Generates HTML B2B partnership proposals
"""

from .consolidator_agent import consolidator_agent
from .distribution_agent import distribution_agent
from .intake_agent import intake_agent
from .matching_agent import matching_agent
from .report_generator import report_generator_agent
from .validation_agent import validation_agent
