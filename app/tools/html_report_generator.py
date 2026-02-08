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

"""HTML Report Generator tool for creating executive reports.

Uses direct text generation (same as original notebook Part 4) to create
McKinsey/BCG style 7-slide HTML presentations from strategic report data.
Saves the generated HTML as an artifact for download in adk web.
"""

import logging
from datetime import datetime

from google import genai
from google.adk.tools import ToolContext
from google.genai import types
from google.genai.errors import ServerError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from ..config import PRO_MODEL

logger = logging.getLogger("ClairvoyB2BTravel")


async def generate_html_report(
    report_data: str, tool_context: ToolContext
) -> dict:
    """Generate a McKinsey/BCG style HTML executive report for B2B travel partnerships.

    This tool creates a professional 7-slide HTML presentation from the
    B2B partnership data using direct text generation with Gemini.
    The generated HTML is automatically saved as an artifact for viewing in adk web.

    Args:
        report_data: The B2B partnership data in a formatted string containing
                    client requirements, validation assessment, supplier recommendations,
                    financial projections, commercial viability, integration package, and next steps.
        tool_context: ADK ToolContext for saving artifacts.

    Returns:
        dict: A dictionary containing:
            - status: "success" or "error"
            - message: Status message
            - artifact_filename: Name of saved artifact (if successful)
            - artifact_version: Version number of artifact (if successful)
            - html_length: Character count of generated HTML
            - error_message: Error details (if failed)
    """
    try:
        # Initialize client (uses GOOGLE_API_KEY from env)
        client = genai.Client()

        current_date = datetime.now().strftime("%Y-%m-%d")

        # Comprehensive prompt for multi-slide HTML generation
        # B2B Travel Partnership Proposal format
        prompt = f"""Generate a comprehensive, professional HTML report for a B2B travel partnership proposal.

This report should be in the style of McKinsey/BCG consulting presentations:
- Multi-slide format using full-screen scrollable sections
- Modern, clean, executive-ready design
- Data-driven visualizations
- Professional color scheme and typography

CRITICAL REQUIREMENTS:

1. STRUCTURE - Create 7 distinct slides (full-screen sections):

   SLIDE 1 - EXECUTIVE SUMMARY & PARTNERSHIP RECOMMENDATION
   - Large, prominent display of client name and POS markets
   - Routes and product types requested
   - Overall partnership viability assessment
   - Recommended decision (Proceed / Proceed with Caution / Decline)
   - Eye-catching hero section with professional branding

   SLIDE 2 - SUPPLIER RECOMMENDATIONS
   - Primary suppliers for FLIGHTS (airline names, routes, commission %, availability)
   - Primary suppliers for HOTELS (hotel brands, destinations, commission %, star ratings)
   - Primary suppliers for ACTIVITIES (providers, activity types, commission %)
   - Backup suppliers for redundancy (in smaller cards)
   - Visual presentation: cards/boxes with supplier logos (text-based placeholders)

   SLIDE 3 - FINANCIAL PROJECTIONS & GMV
   - Estimated monthly GMV by product type (Flights / Hotels / Activities)
   - Commission revenue projections (monthly and annual)
   - Net revenue estimates after costs
   - Annual projected revenue total
   - Visual representation: large stat boxes with currency symbols

   SLIDE 4 - COMMERCIAL VIABILITY & RISK ASSESSMENT
   - Margin analysis: Are margins sufficient?
   - Risk assessment: Supplier dependency, availability, pricing volatility
   - Client fit: Payment terms alignment, pricing type match, volume commitments
   - Strategic fit: Growth potential, effort vs reward
   - Color-coded risk levels (green = low, amber = medium, red = high)

   SLIDE 5 - INTEGRATION PACKAGE & TIMELINE
   - API endpoints overview (Search, Book, Ticket, Refund for each product)
   - Authentication method recommendation (OAuth2 / API Key / JWT)
   - Rate limits by tier (Starter / Professional / Enterprise)
   - White-label customization options (custom domain, branded responses)
   - Integration timeline estimate (weeks breakdown: Sandbox → Development → Testing → Production)

   SLIDE 6 - KEY STRENGTHS & CONCERNS
   - Top 3-4 partnership strengths (cards with evidence from validation)
   - Top 2-3 concerns or risks (cards with mitigation strategies)
   - Balanced view: opportunities vs. challenges

   SLIDE 7 - NEXT STEPS & METHODOLOGY
   - Concrete action items (3-5 specific, numbered recommendations with owners/timelines)
   - Methodology: How this analysis was performed (GDS search, validation framework, consolidation approach)
   - Data sources (Amadeus mock for MVP, note real API integration pending)

2. DESIGN:
   - Use professional consulting color palette:
     * Primary: Navy blue (#1e3a8a, #3b82f6) for headers/trust
     * Success: Green (#059669, #10b981) for positive metrics
     * Warning: Amber (#d97706, #f59e0b) for concerns
     * Neutral: Grays (#6b7280, #e5e7eb) for backgrounds
   - Modern sans-serif fonts (system: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto)
   - Cards with subtle shadows and rounded corners
   - Generous white space and padding
   - Responsive grid layouts

3. TECHNICAL:
   - Self-contained: ALL CSS embedded in <style> tag
   - No external dependencies (no CDNs, no external images)
   - Each slide: min-height: 100vh; page-break-after: always;
   - Smooth scroll behavior
   - Print-friendly

4. DATA TO INCLUDE (use EXACTLY this data, do not invent):

{report_data}

5. OUTPUT:
   - Generate ONLY the complete HTML code
   - Start with <!DOCTYPE html>
   - End with </html>
   - NO explanations before or after the HTML
   - NO markdown code fences

Make it visually stunning, data-rich, and executive-ready.

Current date: {current_date}
"""

        logger.info("Generating HTML report using Gemini...")

        # Retry wrapper for handling model overload errors
        @retry(
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=2, min=2, max=30),
            retry=retry_if_exception_type(ServerError),
            before_sleep=lambda retry_state: logger.warning(
                f"Gemini API error, retrying in {retry_state.next_action.sleep} seconds... "
                f"(attempt {retry_state.attempt_number}/3)"
            ),
        )
        def generate_with_retry():
            return client.models.generate_content(
                model=PRO_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=1.0),
            )

        # Direct text generation (NOT code execution)
        # Same as original notebook: types.GenerateContentConfig(temperature=1.0)
        response = generate_with_retry()

        # Extract HTML from response.text
        html_code = response.text
        # Strip markdown code fences if present
        if html_code.startswith("```"):
            # Remove opening fence (```html or ```)
            if html_code.startswith("```html"):
                html_code = html_code[7:]
            elif html_code.startswith("```HTML"):
                html_code = html_code[7:]
            else:
                html_code = html_code[3:]

            # Remove closing fence
            if html_code.rstrip().endswith("```"):
                html_code = html_code.rstrip()[:-3]

            html_code = html_code.strip()

        # Validate we got HTML
        if not html_code.strip().startswith(
            "<!DOCTYPE"
        ) and not html_code.strip().startswith("<html"):
            logger.warning("Generated content may not be valid HTML")

        # Save as artifact with proper MIME type so it appears in ADK web UI
        html_artifact = types.Part.from_bytes(
            data=html_code.encode("utf-8"), mime_type="text/html"
        )
        artifact_filename = "partnership_proposal.html"

        version = await tool_context.save_artifact(
            filename=artifact_filename, artifact=html_artifact
        )

        # Also store in state for AG-UI frontend display
        tool_context.state["html_report_content"] = html_code

        logger.info(
            f"Saved HTML report artifact: {artifact_filename} (version {version})"
        )

        return {
            "status": "success",
            "message": f"HTML report generated and saved as artifact '{artifact_filename}'",
            "artifact_filename": artifact_filename,
            "artifact_version": version,
            "html_length": len(html_code),
        }

    except Exception as e:
        logger.error(f"Failed to generate HTML report: {e}")
        return {
            "status": "error",
            "error_message": f"Failed to generate HTML report: {e!s}",
        }
