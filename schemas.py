from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# ==========================================
# --- MODULE 4 INPUT SCHEMAS ---
# ==========================================

class ExtractedFacts(BaseModel):
    accused_name: str = Field(..., example="Rahul")
    offence: str = Field(..., example="Theft")
    arrest_date_time: Optional[str] = Field(None, example="2026-06-20T10:00:00")
    magistrate_presentation_time: Optional[str] = Field(None, example="2026-06-21T15:30:00")
    witness_statements: List[Dict[str, str]] = Field(
        default=[], 
        example=[{"witness": "Anand", "statement": "I saw him at 8 PM near the counter."}]
    )
    evidentiary_items: List[str] = Field(
        default=[], 
        example=["CCTV footage timestamped 22:00:00", "Recovery memo"]
    )
    sections_applied: List[str] = Field(default=[], example=["BNS Section 303"])

class RetrievedContext(BaseModel):
    statutory_provisions: List[str] = Field(..., description="Matching BNS/BNSS statutory chunks from RAG")
    case_precedents: List[str] = Field(..., description="Relevant past bail judgments from RAG")

class LoopholeInputPayload(BaseModel):
    extracted_facts: ExtractedFacts
    retrieved_context: RetrievedContext


# ==========================================
# --- MODULE 4 OUTPUT SCHEMAS ---
# ==========================================

class LoopholeItem(BaseModel):
    category: str = Field(..., description="E.g., 'Procedural Non-Compliance', 'Evidentiary Gap', or 'Contradiction'")
    finding: str = Field(..., description="Clear explanation of the discovered weakness or defect.")
    legal_basis: str = Field(..., description="Specific BNS/BNSS sections or court precedents violated.")
    defense_strategy: str = Field(..., description="Actionable instruction on how a lawyer can exploit this in a bail application.")

class LoopholeResponse(BaseModel):
    status: str = "success"
    detected_loopholes: List[LoopholeItem]