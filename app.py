import streamlit as st
import requests

st.set_page_config(page_title="Secure Legal Data Ingestion", layout="wide")

st.title("⚖️ Indian Court Ingestion Portal (Module 2)")
st.write("Secure ingestion processing gateway for legal artifacts and manual case notes.")

# ---------------------------
# SIDEBAR
# ---------------------------

st.sidebar.header("User Access Security Settings")

user_role = st.sidebar.selectbox(
    "Simulated Session Role:",
    ["intern", "senior_advocate"]
)

st.sidebar.markdown(
    f"**Current Clearances:** `{user_role.upper()}`"
)

if user_role == "intern":
    st.sidebar.warning(
        "🔒 Secure Blind Mode Enabled: Sensitive content will remain concealed."
    )
else:
    st.sidebar.success(
        "🔓 Full Visualization Active."
    )

API_BASE_URL = "http://127.0.0.1:8000"

# ---------------------------
# TABS
# ---------------------------

tab1, tab2 = st.tabs(
    [
        "📄 PDF Upload",
        "📝 Manual Case Notes"
    ]
)

# =====================================================
# TAB 1 - PDF INGESTION
# =====================================================

with tab1:

    st.header("Document File Upload Matrix")

    uploaded_file = st.file_uploader(
        "Upload Legal PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        if st.button("Execute Secure Parse Ingestion"):

            with st.spinner(
                "Processing document safely inside private backend stream..."
            ):

                files = [
                    (
                        "files",
                        (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf"
                        )
                    )
                ]

                headers = {
                    "role": user_role
                }

                try:

                    response = requests.post(
                        f"{API_BASE_URL}/api/v1/secure-parse",
                        files=files,
                        headers=headers
                    )

                    if response.status_code == 200:

                        st.success(
                            "Ingestion Sequence Successfully Executed!"
                        )

                        st.json(
                            response.json()
                        )

                    else:

                        st.error(
                            f"Ingestion Aborted ({response.status_code}): {response.text}"
                        )

                except Exception as e:

                    st.error(
                        f"Could not connect to FastAPI server backend: {str(e)}"
                    )

# =====================================================
# TAB 2 - MANUAL CASE NOTES
# =====================================================

with tab2:

    st.header("Manual Case Notes Intake")

    st.info(
        "Use this mode when no FIR, charge sheet, or court PDF is available."
    )

    case_notes = st.text_area(
        label="Paste Client Facts / Hearing Notes / Investigation Notes",
        height=300,
        placeholder="""
Client Name: Rahul Sharma

Police Station: Nashik Road

Incident:
Mobile theft reported on 14 June 2026.

Current Status:
Accused in judicial custody.

Objective:
Prepare regular bail application.
"""
    )

    if st.button("Process Case Notes"):

        if not case_notes.strip():

            st.warning(
                "Please enter case notes before submitting."
            )

        else:

            with st.spinner(
                "Routing case notes through secure ingestion pipeline..."
            ):

                headers = {
                    "role": user_role
                }

                form_data = {
                    "case_notes": case_notes
                }

                try:

                    response = requests.post(
                        f"{API_BASE_URL}/api/v1/secure-parse",
                        data=form_data,
                        headers=headers
                    )

                    if response.status_code == 200:

                        st.success(
                            "Case Notes Successfully Processed!"
                        )

                        st.json(
                            response.json()
                        )

                    else:

                        st.error(
                            f"Processing Failed ({response.status_code}): {response.text}"
                        )

                except Exception as e:

                    st.error(
                        f"Could not connect to FastAPI server backend: {str(e)}"
                    )