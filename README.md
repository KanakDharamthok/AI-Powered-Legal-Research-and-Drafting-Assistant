<div align="center">

# ⚖️ AI-Powered Legal Research & Drafting Assistant (APLRDA)

### Intelligent Courtroom Analysis • Legal Research • Procedural Loophole Detection • Automated Bail Draft Generation

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-orange)
![Whisper](https://img.shields.io/badge/OpenAI-Whisper-purple)
![Ollama](https://img.shields.io/badge/Ollama-Gemma2-black)

</div>

---

## 🚀 Project Overview

**AI-Powered Legal Research & Drafting Assistant (APLRDA)** is an end-to-end Legal AI platform designed to assist advocates, legal interns, and researchers throughout the litigation lifecycle.

The platform combines courtroom audio intelligence, legal document analysis, Retrieval-Augmented Generation (RAG), procedural loophole detection, and automated bail drafting into a single workflow-driven application.

Unlike traditional legal search tools that merely retrieve information, APLRDA acts as an intelligent legal assistant capable of:

- Parsing FIRs, Chargesheets, and Court Orders
- Processing Court Notice Board Fragments
- Transcribing Courtroom Proceedings
- Retrieving Relevant Statutes & Precedents
- Identifying Procedural Loopholes
- Generating Court-Ready Bail Applications

---

# 🛑 Problem Statement

The Indian legal ecosystem faces several operational challenges:

### 📚 Manual Legal Research

Advocates and interns spend substantial time searching statutes, precedents, and procedural provisions before drafting applications.

### 🔍 Hidden Procedural Violations

Critical procedural defects often remain unnoticed, weakening legal strategies.

### 🎙️ Courtroom Documentation Difficulties

Court proceedings frequently involve multilingual conversations, ambient noise, and fragmented records.

### 📝 Time-Consuming Draft Preparation

Drafting bail applications requires extensive legal research, precedent analysis, and procedural verification.

### 🔄 Fragmented Workflow

Most legal solutions solve isolated problems rather than supporting the entire litigation workflow.

---

# 💡 Solution

APLRDA provides a unified AI-driven legal workflow that automates:

- Courtroom Audio Intelligence
- Legal Document Parsing
- Legal Research using RAG
- Procedural Loophole Detection
- Automated Bail Draft Generation

The system transforms unstructured legal data into structured legal intelligence and actionable legal outputs.

---

# 🎯 End-to-End Workflow

```text
Role Verification
        │
        ▼
Document Upload
(PDF / Notice Board)
        │
        ▼
Fact Extraction
        │
        ▼
Courtroom Audio Processing
        │
        ▼
Legal Research (RAG)
        │
        ▼
Loophole Detection
        │
        ▼
Bail Draft Generation
        │
        ▼
Download & Archive
```

---

# ✨ Core Features

---

## 🔐 Role-Based Access Control

The platform implements access-based visibility and governance controls.

### Senior Advocate

- Complete system access
- View all extracted facts
- Access loophole reports
- Generate final drafts

### Junior Advocate

- Legal research access
- Draft review capabilities
- Procedural analysis support

### Intern

- Restricted visibility
- Sensitive information masking
- Observation and learning mode

---

## 📄 Legal Document Intelligence

### Official Document Processing

Supports:

- FIRs
- Chargesheets
- Court Orders
- Legal PDFs

Features:

- PDF Text Extraction
- Fact Identification
- Legal Entity Recognition
- Structured Data Conversion

---

### Notice Board Fragment Parsing

The system can process fragmented court notice board information and extract:

- Case Numbers
- Party Names
- Court Hall Information
- Hearing Stages
- Procedural Flags

Example:

```text
C.C. No. 453/2026
Rahul vs State
Court Hall No. 4
Arguments Stage
```

Converted into structured JSON automatically.

---

## 🎙️ Courtroom Audio Intelligence

### Live Courtroom Recording

Supports real-time courtroom audio capture.

### Speech Recognition

Powered by:

- OpenAI Whisper
- Multilingual Recognition
- Hindi Support
- Marathi Support
- English Support

### Noise Suppression

Powered by Silero Voice Activity Detection (VAD):

- Filters side conversations
- Removes ambient noise
- Eliminates microphone testing chatter
- Retains legal arguments

### Transcript Normalization

Gemma2 converts noisy multilingual transcripts into:

- Formal Legal English
- Chronological Courtroom Scripts
- Structured Proceedings

---

## 📚 Retrieval-Augmented Legal Research (RAG)

APLRDA maintains a local legal knowledge base.

### Knowledge Sources

#### Statutes

- Bharatiya Nyaya Sanhita (BNS)
- Bharatiya Nagarik Suraksha Sanhita (BNSS)

#### Judicial Precedents

- Bail Granted Cases
- Bail Rejected Cases

---

### Retrieval Pipeline

```text
User Facts
      │
      ▼
Embedding Generation
      │
      ▼
ChromaDB Search
      │
      ▼
Relevant Statutes
      │
      ▼
Relevant Judgments
```

---

## 🔍 Loophole Detection Engine

One of the core innovations of APLRDA.

The engine automatically analyzes extracted facts against statutes and precedents to identify:

### Procedural Violations

Examples:

- Failure to produce accused within 24 hours
- Investigation delays
- Illegal arrest procedures

### Evidentiary Gaps

Examples:

- Missing evidence
- Weak witness statements
- Documentary inconsistencies

### Contradictions

Examples:

- Timeline conflicts
- Witness inconsistencies
- Procedural mismatches

---

### Generated Output

Each loophole includes:

- Category
- Finding
- Legal Basis
- Defense Strategy

Example:

```json
{
  "category": "Procedural Non-Compliance",
  "finding": "Accused was produced after 24 hours.",
  "legal_basis": "BNSS Section 187",
  "defense_strategy": "Seek bail citing unlawful detention."
}
```

---

## 📝 Automated Bail Draft Generation

Automatically generates:

### Sessions Court Bail Applications

### High Court Bail Applications

### Supreme Court SLP Drafts

Generated drafts include:

- Case Information
- Legal Grounds
- Relevant Statutes
- Supporting Judgments
- Procedural Violations
- Defense Arguments
- Prayer Clause

---

## 💾 Draft Archival System

Generated drafts can be:

### Downloaded

```text
Bail_Draft_CASEID.txt
```

### Archived

Stored locally using:

```text
saved_drafts/
```

This ensures:

- Draft Persistence
- Case-Based Organization
- Offline Access

---

# 🧠 System Architecture

```text
                     ┌─────────────────────┐
                     │     Streamlit UI    │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │      FastAPI        │
                     └──────────┬──────────┘
                                │
 ┌───────────────┬──────────────┼───────────────┬───────────────┐

 ▼               ▼              ▼               ▼

Role         Document       Audio          RAG
Control      Parser         Engine         Engine

                 │             │
                 ▼             ▼

            Fact Extraction

                    │

                    ▼

            ChromaDB Retrieval

                    │

                    ▼

          Loophole Detection

                    │

                    ▼

           Draft Generator

                    │

                    ▼

      Court-Ready Bail Draft
```

---

# 🛠️ Technology Stack

| Category | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Backend | FastAPI |
| Speech Recognition | OpenAI Whisper |
| Noise Filtering | Silero VAD |
| LLM Framework | Ollama |
| Language Model | Gemma2 |
| Vector Database | ChromaDB |
| Embeddings | BAAI/bge-small-en-v1.5 |
| PDF Processing | PDFPlumber |
| Validation | Pydantic |
| ML Framework | PyTorch |
| Language | Python |

---

# 📂 Project Structure

```text
APLRDA/
│
├── app.py
├── main.py
├── requirements.txt
├── run.bat
├── .env
├── .gitignore
│
├── src/
│   ├── document_parser_module2.py
│   ├── llm_parser.py
│   ├── transcription_engine.py
│   ├── loophole_detector.py
│   ├── draft_generator.py
│   ├── rag_engine.py
│   └── schemas.py
│
├── data/
│   ├── chroma_db/
│   └── knowledge_base/
│       ├── statutes/
│       └── precedents/
│           ├── bail_granted/
│           └── bail_rejected/
│
├── saved_drafts/
│
├── chroma_db/
│
└── venv/
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/APLRDA.git
cd APLRDA
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

## Start Backend

```bash
uvicorn main:app --reload --port 8000
```

## Start Frontend

```bash
streamlit run app.py
```

Or use:

```bash
run.bat
```

---

# 🔮 Future Enhancements

- OCR for scanned FIRs
- Courtroom speaker identification
- E-Filing integration
- Judgment prediction system
- Citation verification engine
- Multi-language draft generation
- Cloud deployment support
- AI-powered case outcome analysis

---

# 🤝 Contributions

Contributions, feature ideas, pull requests, and bug reports are welcome!

### Contribution Workflow

```text
Fork Repository
      ↓
Create Branch
      ↓
Implement Feature
      ↓
Commit Changes
      ↓
Submit Pull Request
      ↓
Review & Merge
```

# Fork → Code → Pull Request ✔️

---

# 📬 Contact

👨‍💻 **Developer:** Kanak Dharamthok

📧 **Email:** ms.kanak.dharamthok@gmail.com

🐙 **GitHub:** https://github.com/KanakDharamthok

💼 **Domain:** AI/ML • Legal AI • NLP • RAG Systems

---

# ⭐ Support

If you find this project useful:

- ⭐ Star the Repository
- 🍴 Fork the Repository
- 🤝 Contribute
- 📢 Share with Others

---

<div align="center">

## ⚖️ AI-Powered Legal Research & Drafting Assistant (APLRDA)

Transforming Legal Research, Courtroom Intelligence, and Bail Drafting through Artificial Intelligence.

</div>
