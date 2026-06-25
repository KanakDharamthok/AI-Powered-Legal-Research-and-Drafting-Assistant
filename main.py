import whisper
import tempfile
import os
import json
import httpx
import hashlib
from io import BytesIO
import tempfile
import whisper
import os
import pdfplumber
from llm_parser import parse_sparse_notice_text, parse_sparse_notice_text_async, NoticeBoardSchema
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, UploadFile, File, Header, HTTPException, status, Form, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Union
from draft_generator import generate_bail_draft

# Vector DB Imports for Module 3
import chromadb
from chromadb.utils import embedding_functions

# Import custom processing engines
from document_parser import process_full_pdf_pipeline, process_sparse_notice_board
from llm_parser import parse_sparse_notice_text, NoticeBoardSchema

# Import Module 4 Schemas
from schemas import LoopholeInputPayload, LoopholeResponse

print("RUNNING MAIN FILE:")
print(os.path.abspath(__file__))

print("=====================================================")
print("🚀 UNIFIED MAIN.PY WITH MODULES 2, 3 & 4 INTEGRATED LOADED")
print("=====================================================")

# --------------------------------------------------
# LIFESPAN MANAGEMENT
# --------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This block executes BEFORE the server starts listening for requests
    print("\n🗺️ REGISTERED FASTAPI ROUTES:")
    for route in app.routes:
        print(f"👉 {route.path}")
    print("=====================================================")
    
    yield  # The app runs while paused here
    
    # Optional: Any cleanup code goes here when shutting down
    print("Stopping Unified Legal Assistant Backend...")


app = FastAPI(
    title="AI Powered Legal Research and Drafting Assistant - Core Backend",
    description="Secure Blind Ingestion Pipeline, RAG Knowledge Gateway & Loophole Detection Engine",
    version="1.2.0",
    lifespan=lifespan
)

# --------------------------------------------------
# CHROMADB / EMBEDDING INITIALIZATION (MODULE 3)
# --------------------------------------------------
DB_PATH = "./data/chroma_db"

try:
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    
    embedding_model = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="BAAI/bge-small-en-v1.5"
    )
    
    collection = chroma_client.get_collection(
        name="legal_knowledge_base", 
        embedding_function=embedding_model
    )
    print(f"✅ [SUCCESS] Connected to local ChromaDB at {DB_PATH}. Collection loaded.")
except Exception as e:
    print(f"⚠️ [WARNING] Local ChromaDB connection failed on startup: {str(e)}")
    collection = None

# Local LLM Variables for Module 4 Engine
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma2"

print("Loading Whisper model...")
whisper_model = whisper.load_model("medium")
print("Whisper model loaded successfully.")

# --------------------------------------------------
# LOCAL HELPER FUNCTIONS
# --------------------------------------------------

def extract_text_from_pdf_stream(file_bytes: bytes) -> str:
    """Reads a raw binary stream of a PDF file in-memory and extracts text."""
    extracted_text = ""
    try:
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"
    except Exception as e:
        raise ValueError(f"Failed to process PDF file structure: {str(e)}")

    if not extracted_text.strip():
        return "[Scanned Document / OCR Required Layer]"

    return extracted_text.strip()

# --------------------------------------------------
# PYDANTIC SCHEMAS (MODULES 2 & 3)
# --------------------------------------------------

class FullCasePayload(BaseModel):
    status: str = "Success"
    file_name: str
    accused_name: Optional[str] = "Pending NLP Extraction"
    offence_sections: List[str] = []
    raw_extracted_text: str = Field(..., description="Sensitive core legal document text")


class BlindIngestionPayload(BaseModel):
    status: str = "Success"
    document_hash: str = Field(..., description="SHA-256 validation fingerprint for tracking")
    file_name: str
    message: str = "File parsed and securely routed directly to Module 3 Knowledge Base."


class KBQueryRequest(BaseModel):
    query: str = Field(..., description="The semantic case facts or argument query string")
    top_k: Optional[int] = Field(3, description="Number of matches to return from the local DB")
    doc_type: Optional[str] = Field(None, description="Filter source mapping: 'statute' or 'precedent'")
    legal_category: Optional[str] = Field(None, description="Filter category: 'procedural_code', 'bail_granted', 'bail_rejected'")


class KBQueryResponse(BaseModel):
    query: str
    results: List[Dict]
    
class TranscriptResponse(BaseModel):
    status: str
    transcript: str

# --------------------------------------------------
# SECURITY DEPENDENCY
# --------------------------------------------------

def verify_role_clearance(role: str = Header(...)):
    normalized_role = role.lower().strip()

    allowed_roles = [
        "intern",
        "junior advocate",
        "junior_advocate",
        "senior advocate",
        "senior_advocate"
    ]

    if normalized_role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid security credentials or organizational role assignment."
        )

    return normalized_role

# --------------------------------------------------
# ENDPOINTS
# --------------------------------------------------

@app.get("/")
def read_root():
    return {
        "status": "Operational",
        "module": "Unified Legal Assistant Backend Orchestrator"
    }


@app.post(
    "/api/v1/secure-parse",
    response_model=Union[List[Union[BlindIngestionPayload, FullCasePayload]], BlindIngestionPayload, FullCasePayload, dict]
)
async def secure_parse_document(
    files: Optional[List[UploadFile]] = File(None, description="Upload multiple court PDFs"),
    case_notes: Optional[str] = Form(None, description="Manual legal notes supplied by intern"),
    role: str = Depends(verify_role_clearance)
):
    if not files and not case_notes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incomplete Pipeline Execution: Provide either PDF files or manual case notes."
        )

    # TRACK 1 - MANUAL CASE NOTES
    if case_notes and not files:
        if not case_notes.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Case notes cannot be blank.")
        
        if role == "intern":
            return {
                "status": "Success",
                "source": "Manual Notes",
                "message": "Case notes securely routed to downstream legal analysis pipeline."
            }
        return {"status": "Success", "source": "Manual Notes", "raw_case_notes": case_notes}

    # TRACK 2 - PDF INGESTION
    responses = []
    for file in files or []:
        file_bytes = await file.read()
        file_hash = hashlib.sha256(file_bytes).hexdigest()

        try:
            raw_text = extract_text_from_pdf_stream(file_bytes)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Parsing error in file {file.filename}: {str(e)}"
            )

        if role == "intern":
            responses.append(BlindIngestionPayload(document_hash=file_hash, file_name=file.filename))
        else:
            responses.append(
                FullCasePayload(
                    file_name=file.filename,
                    accused_name="Pending NLP Extraction",
                    offence_sections=[],
                    raw_extracted_text=raw_text
                )
            )

    if len(responses) == 1:
        return responses[0]
    return responses

@app.post("/api/v1/parse-notice-board")
async def parse_notice_board(
    snippet_text: str = Query(..., description="Raw text snippet from the Indian court notice board")
):
    try:
        result = await parse_sparse_notice_text_async(snippet_text)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/query-knowledge-base", response_model=KBQueryResponse)
async def query_knowledge_base(request: KBQueryRequest):
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Vector database connection is uninitialized or unavailable."
        )
    
    try:
        where_filter = {}
        if request.doc_type:
            where_filter["doc_type"] = request.doc_type
        if request.legal_category:
            where_filter["legal_category"] = request.legal_category

        chroma_filter = where_filter if where_filter else None

        search_results = collection.query(
            query_texts=[request.query],
            n_results=request.top_k,
            where=chroma_filter
        )

        formatted_results = []
        if search_results and search_results["documents"]:
            docs = search_results["documents"][0]
            metas = search_results["metadatas"][0]
            distances = search_results["distances"][0] if "distances" in search_results else [0.0] * len(docs)

            for doc, meta, dist in zip(docs, metas, distances):
                formatted_results.append({
                    "text": doc,
                    "metadata": meta,
                    "confidence_score": round(float(1 - dist), 4)
                })

        return {
            "query": request.query,
            "results": formatted_results
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Vector DB Search Error: {str(e)}"
        )

# ==================================================
# MODULE 1: AUDIO TRANSCRIPTION
# ==================================================

@app.post("/api/v1/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...)
):
    try:
        suffix = os.path.splitext(file.filename)[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as tmp_file:

            tmp_file.write(await file.read())
            temp_path = tmp_file.name

        result = whisper_model.transcribe(
            temp_path,
            task="translate"
        )

        os.remove(temp_path)

        return {
            "status": "success",
            "transcript": result["text"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(e)}"
        )

# ==================================================
# MODULE 4: LOOPHOLE DETECTION ENGINE
# ==================================================

@app.post(
    "/api/v1/detect-loopholes", 
    response_model=LoopholeResponse, 
    tags=["Module 4: Loophole Detection Engine"]
)
async def detect_loopholes(payload: LoopholeInputPayload):
    """
    Module 4 Endpoint: Combines factual data matrices with domain knowledge contexts
    and maps them to a local Ollama server to highlight critical procedural flaws.
    """
    prompt_template = f"""
You are an elite criminal defense analyst specializing in Indian Criminal Law (BNS and BNSS).
Your objective is to thoroughly audit the prosecution's case dossier and identify viable legal loopholes, procedural defects, or factual contradictions that can strengthen a Defense Bail Application.

=== EXTRACTED CASE FACTS ===
- Accused: {payload.extracted_facts.accused_name}
- Offence Charged: {payload.extracted_facts.offence}
- Applied Legal Sections: {payload.extracted_facts.sections_applied}
- Arrest Timestamp: {payload.extracted_facts.arrest_date_time}
- Presentation to Magistrate: {payload.extracted_facts.magistrate_presentation_time}
- Evidentiary Dossier Items: {payload.extracted_facts.evidentiary_items}
- Witness Statements: {json.dumps(payload.extracted_facts.witness_statements, indent=2)}

=== RETRIEVED STATUTORY PROVISIONS & PRECEDENTS ===
Statutes:
{chr(10).join(payload.retrieved_context.statutory_provisions)}

Precedents (Past Case Law):
{chr(10).join(payload.retrieved_context.case_precedents)}

=== CRITICAL EVALUATION GUIDELINES ===
1. Procedural Non-Compliance: Verify if police violated mandatory timelines under BNSS (e.g., failing to present the accused before a magistrate within 24 hours of arrest, delay in recording statements, or missing required memo signatures).
2. Evidentiary Gaps: Identify missing or unverified linkages (e.g., missing independent recovery witnesses, unverified forensic reports, absent electronic certificates).
3. Contradictions & Alibis: Check timelines across statements and physical evidence (e.g., witness claims an incident happened at 8 PM but a physical CCTV trace shows the accused was elsewhere).

=== OUTPUT INSTRUCTIONS ===
You MUST respond with a valid raw JSON array containing objects matching this schema exactly, and absolutely NO conversational text before or after the array:
[
  {{
    "category": "Procedural Non-Compliance | Evidentiary Gap | Contradiction",
    "finding": "Detailed description of the vulnerability.",
    "legal_basis": "Relevant statutory sections (BNS/BNSS) or past court rulings that apply.",
    "defense_strategy": "Strategic recommendation for drafting the bail application argument."
  }}
]
"""

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                OLLAMA_API_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt_template,
                    "stream": False,
                    "options": {
                        "temperature": 0.2
                    }
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to communicate with local Ollama inference server."
                )
                
            result_data = response.json()
            raw_llm_output = result_data.get("response", "").strip()
            
            if raw_llm_output.startswith("```json"):
                raw_llm_output = raw_llm_output.replace("```json", "", 1)
            if raw_llm_output.endswith("```"):
                raw_llm_output = raw_llm_output.rsplit("```", 1)[0]
                
            loopholes_list = json.loads(raw_llm_output.strip())
            return LoopholeResponse(detected_loopholes=loopholes_list)
            
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="The local model failed to return a cleanly parseable JSON vulnerability breakdown."
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Ollama server connection error: {str(e)}. Ensure Ollama is running locally."
            )

# ==================================================
# MODULE 5: DRAFT GENERATION
# ==================================================

from draft_generator import generate_bail_draft

class DraftRequest(BaseModel):
    case_id: str
    court_level: str = "sessions"
    facts: dict
    loopholes: list
    additional_params: Optional[dict] = None

@app.post("/api/v1/generate-draft")
async def generate_draft(payload: DraftRequest):
    try:
        draft_text = generate_bail_draft(
            court_level=payload.court_level,
            case_id=payload.case_id,
            facts=payload.facts,
            loopholes=payload.loopholes,
            additional_params=payload.additional_params
        )
        return {"draft_text": draft_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))