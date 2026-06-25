import os
import uuid
import pdfplumber
import chromadb

from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter

# =====================================================
# CHROMADB SETUP
# =====================================================

CHROMA_DATA_DIR = os.path.join("data", "chroma_db")

chroma_client = chromadb.PersistentClient(
    path=CHROMA_DATA_DIR
)

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="BAAI/bge-small-en-v1.5"
)

collection = chroma_client.get_or_create_collection(
    name="legal_knowledge_base",
    embedding_function=embedding_fn
)

# =====================================================
# TEXT SPLITTER
# =====================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=200,
    length_function=len
)

# =====================================================
# FILE EXTRACTION
# =====================================================

def extract_pdf_text(file_path: str) -> str:
    """Extract text from PDF using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"❌ Error reading PDF {file_path}: {e}")
    return text


def extract_txt_text(file_path: str) -> str:
    """Extract text from TXT file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error reading TXT {file_path}: {e}")
        return ""


def extract_text(file_path: str) -> str:
    """Wrapper for file extraction with case-insensitive extension check."""
    lower_path = file_path.lower()
    if lower_path.endswith(".pdf"):
        return extract_pdf_text(file_path)
    elif lower_path.endswith(".txt"):
        return extract_txt_text(file_path)
    return ""


# =====================================================
# INGESTION
# =====================================================

def seed_directory(
    directory_path: str,
    doc_type: str,
    legal_category: str
):
    """
    Traverses directories robustly and processes text/pdf files case-insensitively.
    """
    if not os.path.exists(directory_path):
        print(f"⚠️ Directory not found: {directory_path}")
        return

    print(f"\n📂 Processing: {directory_path}")

    # Use os.walk to cleanly grab files, handling hidden subdirectories seamlessly
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # Case-insensitive check for extensions
            if not (filename.lower().endswith(".pdf") or filename.lower().endswith(".txt")):
                continue

            raw_text = extract_text(file_path)

            if not raw_text.strip():
                print(f"⚠️ Skipping empty or unreadable file: {filename}")
                continue

            chunks = text_splitter.split_text(raw_text)

            documents = []
            metadatas = []
            ids = []

            for chunk_index, chunk in enumerate(chunks):
                documents.append(chunk)
                metadatas.append({
                    "source_file": filename,
                    "doc_type": doc_type,
                    "legal_category": legal_category,
                    "chunk_index": chunk_index
                })
                ids.append(
                    f"{filename}_chunk_{chunk_index}_{uuid.uuid4().hex[:8]}"
                )

            try:
                collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                print(f"✅ Indexed {len(chunks)} chunks from {filename} [{doc_type}]")
            except Exception as e:
                print(f"❌ Failed indexing {filename}: {e}")


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    print("🚀 Starting Legal Knowledge Base Seeding")

    # 1. Statutes (BNS / BNSS)
    seed_directory(
        directory_path=os.path.join("data", "knowledge_base", "statutes"),
        doc_type="statute",
        legal_category="procedural_code"
    )

    # 2. Bail Granted Cases
    seed_directory(
        directory_path=os.path.join("data", "knowledge_base", "precedents", "bail_granted"),
        doc_type="precedent",
        legal_category="bail_granted"
    )

    # 3. Bail Rejected Cases
    seed_directory(
        directory_path=os.path.join("data", "knowledge_base", "precedents", "bail_rejected"),
        doc_type="precedent",
        legal_category="bail_rejected"
    )

    print("\n🎉 Knowledge Base Seeding Complete!")
    print(f"📊 Total Chunks in DB: {collection.count()}")