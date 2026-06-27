"""
llm_parser.py
=============
Parses sparse notice board text using local Ollama (gemma2).
"""

import httpx
import json
from pydantic import BaseModel
from typing import Optional, List

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma2:2b"


class NoticeBoardSchema(BaseModel):
    case_number: Optional[str] = None
    parties: Optional[str] = None
    court_hall: Optional[str] = None
    legal_stage: Optional[str] = None
    inferred_warnings: List[str] = []


async def parse_sparse_notice_text_async(snippet: str) -> NoticeBoardSchema:
    prompt = f"""
You are a legal clerk assistant. Extract structured information from the following
Indian court notice board fragment and respond ONLY with a valid JSON object.
No explanation, no markdown, no extra text — just raw JSON.

Notice Board Text:
\"\"\"{snippet}\"\"\"

Respond with exactly this JSON structure:
{{
  "case_number": "extracted case number or null",
  "parties": "applicant vs respondent or null",
  "court_hall": "court hall or room number or null",
  "legal_stage": "e.g. Bail Hearing, Framing of Charges, Arguments, Judgment or null",
  "inferred_warnings": ["any procedural flags or observations as list of strings"]
}}
"""
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                OLLAMA_API_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.1}
                }
            )
            raw = response.json().get("response", "").strip()

            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            raw = raw.strip()

            parsed = json.loads(raw)
            return NoticeBoardSchema(**parsed)

    except json.JSONDecodeError:
        return NoticeBoardSchema(
            inferred_warnings=["Model returned non-JSON response. Try again."]
        )
    except Exception as e:
        return NoticeBoardSchema(
            inferred_warnings=[f"Parsing exception: {str(e)}"]
        )


# Kept for import compatibility — do not use inside FastAPI endpoints
def parse_sparse_notice_text(snippet: str, api_key: str = "") -> NoticeBoardSchema:
    return NoticeBoardSchema(
        inferred_warnings=["Use parse_sparse_notice_text_async inside FastAPI endpoints."]
    )