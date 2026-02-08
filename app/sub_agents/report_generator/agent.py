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

"""Report Generator Agent - Generates B2B Travel Partnership Proposals.

This agent generates a professional HTML executive report for B2B travel
partnership proposals using the generate_html_report tool.

The tool handles:
- Calling Gemini to generate 7-slide McKinsey/BCG style HTML
- Saving the HTML as an artifact for download in adk web
"""

from google.adk.agents import LlmAgent
from google.genai import types

from ...config import FAST_MODEL, RETRY_ATTEMPTS, RETRY_INITIAL_DELAY
from ...tools import generate_html_report

REPORT_GENERATOR_INSTRUCTION = """You are an executive report generator for B2B travel partnership proposals.

Your task is to create a professional HTML executive report using the generate_html_report tool.

## ACCESSING DATA
You have access to the session state which contains:

**Demand Context:**
- `client_name`: Name of the OTA/TMC client
- `pos_markets`: List of POS markets
- `routes`: Origin-destination route pairs
- `product_types`: Requested product types

**Specialist Agent Results (may or may not exist):**
- `validation_assessment`: Feasibility and risk assessment from ValidationAgent
- `matching_results`: Supplier inventory search results from MatchingAgent
- `consolidated_inventory`: Inventory analysis from ConsolidatorAgent
- `distribution_package`: API integration package from DistributionAgent

## Your Mission
Format the B2B partnership data and call the generate_html_report tool to create a
McKinsey/BCG-style 7-slide HTML presentation.

## Important Notes on Data Availability
- If any specialist data shows "Not yet assessed", "Not yet searched", "Not yet consolidated", or "Not yet designed":
  - Acknowledge the missing analysis in the appropriate report sections
  - Work with whatever data IS available from the demand context
  - Note what additional analysis would be beneficial for a complete assessment
  - Do NOT fabricate or assume data that wasn't provided
  - Adjust your recommendations to reflect the available information
- The flexible workflow means not all specialists may have been consulted before report generation

## Steps

### Step 1: Format the Report Data
Prepare a comprehensive data summary from all available data, including:

**Executive Summary Section:**
- Client name and POS markets
- Routes and product types requested
- Overall partnership viability (from validation assessment)
- Recommended decision (Proceed / Proceed with Caution / Decline)

**Supplier Recommendations Section:**
- Primary suppliers for flights (airline names, routes, commission %, availability)
- Primary suppliers for hotels (hotel names, locations, commission %, star rating)
- Primary suppliers for activities (provider names, activity types, commission %)
- Backup suppliers for redundancy

**Financial Projections Section:**
- Estimated monthly GMV by product type
- Commission revenue projections
- Net revenue estimates (after costs)
- Annual projected revenue

**Commercial Viability Section:**
- Margin analysis (are margins sufficient?)
- Risk assessment (supplier dependency, availability, pricing)
- Client fit (payment terms, pricing type, volume commitments)

**Integration Package Section:**
- API endpoints overview (Search, Book, Ticket, Refund)
- Authentication method recommendation
- Rate limits by tier (Starter/Professional/Enterprise)
- White-label customization options
- Integration timeline estimate

**Key Strengths & Concerns Section:**
- Top 3-4 partnership strengths (from validation and consolidation)
- Top 2-3 concerns or risks (with mitigation strategies)

**Next Steps Section:**
- Concrete action items (3-5 specific recommendations)
- Timeline and milestones

### Step 2: Call the Tool
Call the generate_html_report tool with the formatted report data.
The tool will:
- Generate a professional 7-slide HTML report
- Save it as an artifact named "partnership_proposal.html"
- Return the status and artifact details

### Step 3: Report Result
After the tool returns, confirm the report was generated successfully.
If there was an error, report what went wrong.
"""

report_generator_agent = LlmAgent(
    name="ReportGeneratorAgent",
    model=FAST_MODEL,
    description="Generates professional McKinsey/BCG-style HTML B2B partnership proposals using the generate_html_report tool",
    instruction=REPORT_GENERATOR_INSTRUCTION,
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                initial_delay=RETRY_INITIAL_DELAY,
                attempts=RETRY_ATTEMPTS,
            ),
        ),
    ),
    tools=[generate_html_report],
    output_key="report_generation_result",
)
