# llm_parser.py
import json
from typing import Optional, List
from pydantic import BaseModel, Field
import openai

class NoticeBoardSchema(BaseModel):
    case_number: Optional[str] = Field(None, description="Extracted Court Case/Bail Application Number")
    parties: Optional[str] = Field(None, description="Litigating Parties (e.g., State vs. Unknown)")
    court_hall: Optional[str] = Field(None, description="Court room or hall identifier")
    legal_stage: Optional[str] = Field(None, description="Current legal stage, e.g., Framing of Charges, Bail Arguments")
    inferred_warnings: List[str] = Field(default=[], description="Downstream context gaps flagged for Module 4")

def parse_sparse_notice_text(snippet: str, api_key: str) -> NoticeBoardSchema:
    """
    Uses an LLM to transform a messy, fragmented physical notice board string 
    into a strictly validated database schema.
    """
    client = openai.OpenAI(api_key=api_key)
    
    prompt = f"""
    You are an expert Indian court data assistant. Extract key metadata from this notice board scrap text.
    If a specific variable is completely missing or cannot be inferred, return null for it.
    If 'bail' is mentioned in the text, add an item to inferred_warnings: 'Arrest confirmed. Request arrest date verification.'
    
    Notice Board Scrap: "{snippet}"
    """
    
    try:
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Extract structural court metadata from physical court scraps."},
                {"role": "user", "content": prompt}
            ],
            response_format=NoticeBoardSchema,
        )
        return response.choices[0].message.parsed
    except Exception as e:
        return NoticeBoardSchema(
            case_number="Error",
            inferred_warnings=[f"Parsing exception layer encountered: {str(e)}"]
        )