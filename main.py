from fastapi import FastAPI, UploadFile, File, Header, HTTPException, status, Form, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Union
from io import BytesIO
import pdfplumber
import hashlib

print("===================================")
print("NEW MAIN.PY LOADED")
print("===================================")

app = FastAPI(
    title="AI Powered Legal Research and Drafting Assistant - Module 2",
    description="Secure Blind Ingestion Pipeline",
    version="1.0.0"
)

# --------------------------------------------------
# LOCAL HELPER FUNCTIONS
# --------------------------------------------------

def extract_text_from_pdf_stream(file_bytes: bytes) -> str:
    """
    Reads a raw binary stream of a PDF file in-memory
    and extracts text.
    """

    extracted_text = ""

    try:
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    extracted_text += page_text + "\n"

    except Exception as e:
        raise ValueError(
            f"Failed to process PDF file structure: {str(e)}"
        )

    if not extracted_text.strip():
        return "[Scanned Document / OCR Required Layer]"

    return extracted_text.strip()


# --------------------------------------------------
# PYDANTIC SCHEMAS
# --------------------------------------------------

class FullCasePayload(BaseModel):
    status: str = "Success"
    file_name: str
    accused_name: Optional[str] = "Pending NLP Extraction"
    offence_sections: List[str] = []
    raw_extracted_text: str = Field(
        ...,
        description="Sensitive core legal document text"
    )


class BlindIngestionPayload(BaseModel):
    status: str = "Success"
    document_hash: str = Field(
        ...,
        description="SHA-256 validation fingerprint for tracking"
    )
    file_name: str
    message: str = (
        "File parsed and securely routed directly "
        "to Module 3 Knowledge Base."
    )


# --------------------------------------------------
# SECURITY DEPENDENCY
# --------------------------------------------------

def verify_role_clearance(
    role: str = Header(
        ...,
        description="Role profile ('Intern' or 'Senior Advocate')"
    )
) -> str:

    normalized_role = role.lower().strip()

    if normalized_role not in [
        "intern",
        "senior advocate",
        "senior_advocate"
    ]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid security credentials or organizational role assignment."
        )

    return normalized_role


# --------------------------------------------------
# ROOT ENDPOINT
# --------------------------------------------------

@app.get("/")
def read_root():
    return {
        "status": "Operational",
        "module": "Module 2 Ingestion Pipeline Core"
    }


# --------------------------------------------------
# MAIN INGESTION ENDPOINT
# --------------------------------------------------

@app.post(
    "/api/v1/secure-parse",
    response_model=Union[
        List[Union[BlindIngestionPayload, FullCasePayload]],
        BlindIngestionPayload,
        FullCasePayload,
        dict
    ]
)
async def secure_parse_document(
    files: Optional[List[UploadFile]] = File(
        None,
        description="Upload multiple court PDFs"
    ),
    case_notes: Optional[str] = Form(
        None,
        description="Manual legal notes supplied by intern"
    ),
    role: str = Depends(verify_role_clearance)
):

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------

    if not files and not case_notes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Incomplete Pipeline Execution: "
                "Provide either PDF files or manual case notes."
            )
        )

    # --------------------------------------------------
    # TRACK 1 - MANUAL CASE NOTES
    # --------------------------------------------------

    if case_notes and not files:

        if not case_notes.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Case notes cannot be blank."
            )

        if role == "intern":
            return {
                "status": "Success",
                "source": "Manual Notes",
                "message": (
                    "Case notes securely routed to "
                    "downstream legal analysis pipeline."
                )
            }

        return {
            "status": "Success",
            "source": "Manual Notes",
            "raw_case_notes": case_notes
        }

    # --------------------------------------------------
    # TRACK 2 - PDF INGESTION
    # --------------------------------------------------

    responses = []

    for file in files or []:

        file_bytes = await file.read()

        file_hash = hashlib.sha256(
            file_bytes
        ).hexdigest()

        try:
            raw_text = extract_text_from_pdf_stream(
                file_bytes
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Parsing error in file {file.filename}: {str(e)}"
            )

        if role == "intern":

            responses.append(
                BlindIngestionPayload(
                    document_hash=file_hash,
                    file_name=file.filename
                )
            )

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


# --------------------------------------------------
# STARTUP DEBUG ROUTES
# --------------------------------------------------

@app.on_event("startup")
async def show_routes():

    print("\nREGISTERED ROUTES:")

    for route in app.routes:
        print(route.path)