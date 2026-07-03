"""QA matrix runner for the Clairvoy travel agent.

Runs the 18-case QA scenario matrix (itinerary recommendation + after-sales)
against the live agent and prints each final response for manual review.

Prerequisites:
    export GOOGLE_API_KEY='your_api_key'
    export GOOGLE_GENAI_USE_VERTEXAI=FALSE

Usage:
    uv run python run_qa_matrix.py             # run all 18 cases
    uv run python run_qa_matrix.py 1.a 8.b     # run selected cases
"""

import asyncio
import os
import sys
from datetime import datetime

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

from app.agent import root_agent

QA_CASES: dict[str, str] = {
    "1.a": "Can you recommend a travel itinerary for me?",
    "1.b": "I want an itinerary for a trip to Singapore.",
    "1.c": "Please make me an itinerary for a trip to Korea.",
    "2.a": "Recommend me an itinerary for a 3-day trip, anywhere is fine.",
    "2.b": "Give me an itinerary to Labuan Bajo for 5 days.",
    "2.c": "Plan me a 10-day itinerary in Europe.",
    "3.a": "I want to visit Melbourne for a spring trip, what itinerary do you suggest?",
    "3.b": "I want to go on a sakura trip. Where should I go and what should I do?",
    "4.a": "Recommend a budget-friendly itinerary in Indonesia.",
    "4.b": "Give me a luxurious itinerary for Singapore.",
    "5.a": "Recommend an itinerary for a couple trip.",
    "5.b": "Plan a family trip itinerary to Bali.",
    "6.a": "Make me a 3-day Bali itinerary with a budget under IDR 5.000.000.",
    "6.b": "Plan a solo trip itinerary to Korea focused on exploring the culture.",
    "7.a": "What are the refund and reschedule rules for SQ (Singapore Airlines)?",
    "7.b": "Can you estimate the refund and reschedule cost for my SQ ticket? Economy Standard (M class), base fare IDR 3.500.000, taxes IDR 800.000, 2 passengers.",
    "8.a": "Calculate the refund for booking CLV-2026-0001, split per supplier airline.",
    "8.b": "Calculate the refund for booking CLV-2026-0002 as of 2026-08-01, split per supplier for the airline and the hotel.",
}


async def run_case(case_id: str, prompt: str) -> None:
    session_service = InMemorySessionService()
    now = datetime.now()
    await session_service.create_session(
        app_name="app",
        user_id="qa_user",
        session_id=f"qa_{case_id.replace('.', '_')}",
        state={
            "time": now.strftime("%H:%M:%S"),
            "date": now.strftime("%Y-%m-%d"),
            "datetime": now.isoformat(),
            "workspace.id": "qa-workspace",
            "workspace.name": "QA Matrix",
        },
    )
    runner = Runner(agent=root_agent, app_name="app", session_service=session_service)

    print("=" * 100)
    print(f"CASE {case_id}: {prompt}")
    print("-" * 100)
    async for event in runner.run_async(
        user_id="qa_user",
        session_id=f"qa_{case_id.replace('.', '_')}",
        new_message=genai_types.Content(
            role="user", parts=[genai_types.Part.from_text(text=prompt)]
        ),
    ):
        if event.actions and event.actions.transfer_to_agent:
            print(f"[routing] transfer_to_agent -> {event.actions.transfer_to_agent}")
        if event.get_function_calls():
            for call in event.get_function_calls():
                print(f"[tool] {call.name}({call.args})")
        if event.is_final_response() and event.content and event.content.parts:
            text = event.content.parts[0].text or ""
            print(text)
    print()


async def main() -> None:
    if (
        not os.getenv("GOOGLE_API_KEY")
        and os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "FALSE").upper() != "TRUE"
    ):
        print(
            "ERROR: set GOOGLE_API_KEY (or configure Vertex AI) to run the QA matrix."
        )
        sys.exit(1)

    selected = sys.argv[1:] or list(QA_CASES)
    unknown = [case for case in selected if case not in QA_CASES]
    if unknown:
        print(f"Unknown case ids: {unknown}. Available: {list(QA_CASES)}")
        sys.exit(1)

    for case_id in selected:
        await run_case(case_id, QA_CASES[case_id])


if __name__ == "__main__":
    asyncio.run(main())
