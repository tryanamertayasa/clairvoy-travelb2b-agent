"""Programmatic test script for Clairvoy B2B Travel Agent.

This script tests the agent with a sample B2B travel inquiry to validate
the conversational delegation and agent functionality.

Prerequisites:
    Set environment variables:
        GOOGLE_API_KEY=your_api_key
        GOOGLE_GENAI_USE_VERTEXAI=FALSE
"""

import asyncio
import os
import sys

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

from app.agent import root_agent


async def main():
    """Test the Clairvoy agent with a sample B2B travel inquiry."""
    print("=" * 80)
    print("CLAIRVOY B2B TRAVEL AGENT - PROGRAMMATIC TEST")
    print("=" * 80)
    print()

    # Check for required environment variables
    if not os.getenv("GOOGLE_API_KEY"):
        print("ERROR: GOOGLE_API_KEY environment variable is not set!")
        print()
        print("To run this test, you need to set:")
        print("  export GOOGLE_API_KEY='your_api_key'")
        print("  export GOOGLE_GENAI_USE_VERTEXAI=FALSE")
        print()
        print("Get your API key from: https://aistudio.google.com/apikey")
        sys.exit(1)

    print("✓ API credentials found")
    print()

    # Initialize session service
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="app", user_id="test_user", session_id="test_session"
    )

    # Create runner
    runner = Runner(
        agent=root_agent, app_name="app", session_service=session_service
    )

    # Sample B2B travel inquiry
    test_query = """We're a Singapore-based OTA called "TravelEase Asia" looking to expand our inventory.

We need:
- Flight inventory on routes from India (Mumbai, Delhi) to Dubai and Singapore
- Hotel inventory in Dubai and Singapore (3-star to 5-star)
- Activities and tours in Dubai

We operate in Singapore, Malaysia, and Indonesia (our POS markets).

We prefer NET rate pricing and can commit to around 2,000 bookings per month initially.
Payment terms: NET 30 preferred.

Can you help us assess this partnership opportunity?"""

    print(f"Test Query:\n{test_query}\n")
    print("=" * 80)
    print("AGENT RESPONSE:")
    print("=" * 80)
    print()

    # Run the agent
    final_response = None
    async for event in runner.run_async(
        user_id="test_user",
        session_id="test_session",
        new_message=genai_types.Content(
            role="user", parts=[genai_types.Part.from_text(text=test_query)]
        ),
    ):
        # Print agent name and content for each event
        if event.author and event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(f"[{event.author}]:")
                    print(part.text)
                    print()

        # Capture final response
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text

    print("=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)
    print()

    if final_response:
        print("FINAL RESPONSE CAPTURED:")
        print(final_response)
    else:
        print("WARNING: No final response captured")

    print()
    print("Test script finished successfully!")


if __name__ == "__main__":
    asyncio.run(main())
