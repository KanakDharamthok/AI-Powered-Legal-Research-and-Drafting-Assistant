import streamlit as st
import requests
import json
import os
from datetime import datetime
from streamlit_mic_recorder import mic_recorder

# --- CONFIGURATION ---
BACKEND_URL = "http://127.0.0.1:8000"
SAVED_DRAFTS_DIR = "./saved_drafts"

if not os.path.exists(SAVED_DRAFTS_DIR):
    os.makedirs(SAVED_DRAFTS_DIR)

st.set_page_config(page_title="AI Powered Legal Research & Drafting Assistant", page_icon="⚖️", layout="wide")

# --- CENTRALIZED STATE MANAGEMENT ---
# State variables to carry data across sequential stages
INITIAL_STATES = {
    "current_stage": "Role Selection",
    "user_role": None,
    "case_id": "",
    "courtroom_transcript": "",
    "extracted_facts": {},
    "retrieved_laws": [],
    "detected_loopholes": [],
    "final_draft": ""
}

for key, value in INITIAL_STATES.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- APPLICATION WIZARD PROGRESS BAR ---
stages = ["Role Selection", "Document Upload", "Audio Processing", "RAG & Loophole Analysis", "Draft & Save"]
current_index = stages.index(st.session_state["current_stage"])

st.title("⚖️ AI Legal Research & Drafting Assistant")
st.progress((current_index + 1) / len(stages))

# --- HELPER FUNCTIONS FOR NAVIGATION ---
def move_to(stage_name):
    st.session_state["current_stage"] = stage_name
    st.rerun()

def reset_pipeline():
    for key, value in INITIAL_STATES.items():
        st.session_state[key] = value
    st.rerun()

# ==========================================
# STAGE 1: ROLE SELECTION & LOGIN
# ==========================================
if st.session_state["current_stage"] == "Role Selection":
    st.header("🔐 Step 1: User Identity Verification")
    st.write("Please select your operational role to define data governance and viewing permissions.")
    
    role = st.selectbox("Select Access Role:", ["Senior Advocate", "Junior Advocate", "Intern"])
    case_id = st.text_input("Enter Unique Case Reference ID (e.g., BAIL-2026-004):", value="BAIL-2026-XYZ")
    
    if st.button("Proceed to Case Profile ➡️"):
        if case_id.strip() == "":
            st.error("A valid Case Reference ID is required to secure local database integrity.")
        else:
            st.session_state["user_role"] = role
            st.session_state["case_id"] = case_id
            move_to("Document Upload")

# ==========================================
# STAGE 2: DOCUMENT UPLOAD (MODULE 2) - CORRECTED ENDPOINTS
# ==========================================
elif st.session_state["current_stage"] == "Document Upload":
    st.header(f"📄 Step 2: Document Ingestion Pipeline [Case: {st.session_state['case_id']}]")
    st.info(f"Logged in as: `{st.session_state['user_role']}`")
    
    ingestion_mode = st.radio("Choose Input Type:", ["Official Paperwork (PDF)", "Notice Board Fragment (Manual Text)"])
    
    if ingestion_mode == "Official Paperwork (PDF)":
        uploaded_pdf = st.file_uploader("Upload Prosecution Papers (FIR, Chargesheet, Orders):", type=["pdf"])
        if st.button("⚡ Parse & Extract Case Metrics"):
            if uploaded_pdf:
                with st.spinner("Extracting parameters with secure blind processing validations..."):
                    try:
                        #  CORRECTED HEADER MATCHING FASTAPI EXPECTATIONS
                        files = {"files": (uploaded_pdf.name, uploaded_pdf.getvalue(), "application/pdf")}
                        headers = {"role": st.session_state["user_role"]}
                        response = requests.post(f"{BACKEND_URL}/api/v1/secure-parse", files=files, headers=headers) 
                        
                        if response.status_code == 200:
                            st.session_state["extracted_facts"] = response.json()
                            st.success("Document structure indexed into application state cache!")
                        else:
                            st.error(f"Backend Ingestion Failure: {response.text}")
                    except Exception as e:
                        st.error(f"Connection Error: {str(e)}")
            else:
                st.warning("Please upload a PDF file.")
    else:
        notice_board_input = st.text_area("Paste Notice Board Fragment:")
        if st.button("⚡ Normalize Scrap Data"):
            if notice_board_input.strip():
                with st.spinner("Formatting fragment data structure..."):
                    try:
                        payload = {"snippet_text": notice_board_input}
                        
                        # CORRECTED: Pointing to /api/v1/parse-notice-board instead of /api/v1/parse-fragment
                        response = requests.post(f"{BACKEND_URL}/api/v1/parse-notice-board", params=payload)
                        
                        if response.status_code == 200:
                            st.session_state["extracted_facts"] = response.json()
                            st.success("Fragment parsed successfully!")
                        else:
                            st.error(f"Backend Error: {response.text}")
                    except Exception as e:
                        st.error(f"Connection Error: {str(e)}")

    # Display status window depending on role visibility constraints
    if st.session_state["extracted_facts"]:
        st.markdown("#### Current State Cache View")
        if st.session_state["user_role"] == "Intern":
            st.warning("🔒 Confidential Metrics Obfuscated. System holds variables securely without frontend display.")
        else:
            st.json(st.session_state["extracted_facts"])
            
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Back to Authentication"): move_to("Role Selection")
        with col2:
            if st.button("Proceed to Audio Transcription ➡️"): move_to("Audio Processing")

# ==========================================
# STAGE 3: AUDIO PROCESSING (MODULE 1)
# ==========================================
elif st.session_state["current_stage"] == "Audio Processing":

    st.header("🎙️ Step 3: Courtroom Audio Transcription")

    st.write(
        "Record live courtroom proceedings and transcribe them using Whisper."
    )

    audio = mic_recorder(
        start_prompt="Start Recording",
        stop_prompt="Stop Recording",
        just_once=False,
        use_container_width=True
    )

    if audio:

        st.audio(audio["bytes"], format="audio/wav")

        if st.button("🚀 Transcribe Audio"):

            with st.spinner("Executing Whisper transcription..."):

                try:

                    files = {
                        "file": (
                            "courtroom_recording.wav",
                            audio["bytes"],
                            "audio/wav"
                        )
                    }

                    response = requests.post(
                        f"{BACKEND_URL}/api/v1/transcribe",
                        files=files
                    )

                    if response.status_code == 200:

                        st.session_state["courtroom_transcript"] = (
                            response.json().get("transcript", "")
                        )

                        st.success(
                            "Acoustic normalization complete!"
                        )

                    else:

                        st.error(
                            f"Backend Transcription Error: {response.text}"
                        )

                except Exception as e:

                    st.error(
                        f"Transcription connection crashed: {str(e)}"
                    )

    else:

        st.info(
            "Record audio and stop recording to enable transcription."
        )

    if st.session_state["courtroom_transcript"]:

        st.text_area(
            "Calculated Transcript Summary:",
            st.session_state["courtroom_transcript"],
            height=200
        )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back to Document Step"):
            move_to("Document Upload")

    with col2:
        if st.button("Proceed to Analysis (RAG & Loopholes) ➡️"):
            move_to("RAG & Loophole Analysis")

# ==========================================
# STAGE 4: RAG & LOOPHOLE DETECTION (MODULES 3 & 4)
# ==========================================
elif st.session_state["current_stage"] == "RAG & Loophole Analysis":
    st.header("🔍 Step 4: Analytical Processing Layer")
    st.write("Merging collected documentation with statutory definitions and querying local Ollama instance.")

    if st.button("🧠 Run Loophole Detection Engine"):
     with st.spinner("Connecting ChromaDB contexts and invoking Ollama model weights..."):
        try:
            facts = st.session_state["extracted_facts"]
            raw_text = facts.get("raw_extracted_text", "")
            transcript = st.session_state["courtroom_transcript"]

            # Build payload matching LoopholeInputPayload schema exactly
            payload = {
                "extracted_facts": {
                    "accused_name": facts.get("accused_name", "Unknown"),
                    "offence": f"{facts.get('offence_sections', [])} | Transcript: {transcript[:300]}",
                    "arrest_date_time": None,
                    "magistrate_presentation_time": None,
                    "witness_statements": [],
                    "evidentiary_items": [raw_text[:500]] if raw_text else [],
                    "sections_applied": facts.get("offence_sections", [])
                },
                "retrieved_context": {
                    "statutory_provisions": st.session_state.get("retrieved_laws", [
                        "BNSS Section 187: Accused must be presented before magistrate within 24 hours.",
                        "BNS Section 303: Punishment for theft.",
                        "BNSS Section 173: Investigation procedures and timelines."
                    ]),
                    "case_precedents": [
                        "Arnesh Kumar v. State of Bihar (2014): Arrest must be justified and necessary.",
                        "Satender Kumar Antil v. CBI (2021): Default bail if chargesheet not filed in time."
                    ]
                }
            }

            response = requests.post(
                f"{BACKEND_URL}/api/v1/detect-loopholes",
                json=payload
            )

            if response.status_code == 200:
                results = response.json()
                st.session_state["detected_loopholes"] = results.get("detected_loopholes", [])
                st.success("Analysis complete! Vulnerabilities discovered.")
            else:
                st.error(f"Loophole Engine Error ({response.status_code}): {response.text}")
        except Exception as e:
            st.error(f"Failed to contact Ollama Gateway: {str(e)}")

    if st.session_state["detected_loopholes"]:
        st.subheader("⚠️ Identified Procedural Flaws & Discrepancies")
        st.json(st.session_state["detected_loopholes"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Transcription"): move_to("Audio Processing")
    with col2:
        if st.button("Proceed to Final Legal Draft ➡️"): move_to("Draft & Save")

# ==========================================
# STAGE 5: DRAFT GENERATION & SAVING SYSTEM (MODULE 5)
# ==========================================
elif st.session_state["current_stage"] == "Draft & Save":
    st.header("📝 Step 5: Final Submission Draft & Archival System")

    # Court level selector
    court_level = st.selectbox(
        "Select Court Level:",
        ["sessions", "high_court", "supreme_court"],
        format_func=lambda x: {
            "sessions": "Sessions Court",
            "high_court": "High Court",
            "supreme_court": "Supreme Court (SLP)"
        }[x]
    )

    # Optional extra fields
    with st.expander("⚙️ Additional Court Details (Optional but Recommended)"):
        fir_number     = st.text_input("FIR Number", "As per records")
        police_station = st.text_input("Police Station", "Concerned Police Station")
        district       = st.text_input("District", "Concerned District")
        advocate_name  = st.text_input("Advocate Name", "Counsel for the Applicant")
        state          = st.text_input("State", "State")
        sessions_order = st.text_input("Sessions Court Order Date (required for High Court / Supreme Court)", "")
        hc_bench       = st.text_input("High Court Bench Name (required for High Court / Supreme Court)", "")
        hc_order       = st.text_input("High Court Order Date (required for Supreme Court only)", "")

    if st.button("🏗️ Assemble Bail Application Draft"):
        with st.spinner("Mapping elements to statutory judicial draft formats..."):
            try:
                payload = {
                    "case_id": st.session_state["case_id"],
                    "court_level": court_level,
                    "facts": st.session_state["extracted_facts"],
                    "loopholes": st.session_state["detected_loopholes"],
                    "additional_params": {
                        "fir_number": fir_number,
                        "police_station": police_station,
                        "district": district,
                        "advocate_name": advocate_name,
                        "state": state,
                        "sessions_court_order_date": sessions_order,
                        "high_court_bench": hc_bench,
                        "high_court_order_date": hc_order
                    }
                }
                response = requests.post(f"{BACKEND_URL}/api/v1/generate-draft", json=payload)
                if response.status_code == 200:
                    st.session_state["final_draft"] = response.json().get("draft_text", "")
                    st.success("Draft assembled successfully!")
                else:
                    st.error(f"Draft Generation Error ({response.status_code}): {response.text}")

            except Exception as e:
                st.error(f"Connection Error: {str(e)}")

    if st.session_state["final_draft"]:
        st.subheader("📋 Output Preview Document Window")
        editable_draft = st.text_area(
            "Live Document Workspace:",
            st.session_state["final_draft"],
            height=600
        )
        st.session_state["final_draft"] = editable_draft  # Save manual edits

        # SAVE & ARCHIVE CAPABILITY
        st.markdown("### 💾 Archival Options")
        col_s1, col_s2 = st.columns(2)

        with col_s1:
            st.download_button(
                label="📥 Download Draft as Text File",
                data=st.session_state["final_draft"],
                file_name=f"Bail_Draft_{st.session_state['case_id']}_{court_level}.txt",
                mime="text/plain"
            )

        with col_s2:
            if st.button("💾 Archive Permanently on System Drive"):
                filepath = os.path.join(
                    SAVED_DRAFTS_DIR,
                    f"{st.session_state['case_id']}_{court_level}_draft.txt"
                )
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(st.session_state["final_draft"])
                st.success(f"Successfully archived to: `{filepath}`")

    st.markdown("---")
    if st.button("🔄 Start New Case (Reset Complete Pipeline State)"):
        reset_pipeline()