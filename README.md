<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Powered Legal Research and Drafting Assistant - Documentation</title>
    <style>
        :root {
            --bg-color: #0d1117;
            --text-color: #c9d1d9;
            --text-muted: #8b949e;
            --accent-color: #58a6ff;
            --border-color: #30363d;
            --code-bg: #161b22;
            --header-bg: #161b22;
            --accent-glow: rgba(88, 166, 255, 0.1);
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            margin: 0;
            padding: 2rem 1rem;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 0 20px;
        }
        h1, h2, h3, h4 {
            color: #f0f6fc;
            font-weight: 600;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.3em;
        }
        h1 { font-size: 2.25em; border-bottom: 2px solid var(--border-color); }
        h2 { font-size: 1.5em; margin-top: 24px; }
        h3 { font-size: 1.25em; border-bottom: none; }
        p, ul, ol { margin-top: 0; margin-bottom: 16px; }
        ul, ol { padding-left: 2em; }
        li { margin-top: 0.25em; }
        a { color: var(--accent-color); text-decoration: none; }
        a:hover { text-decoration: underline; }
        code {
            font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
            background-color: rgba(110, 118, 129, 0.2);
            padding: 0.2em 0.4em;
            border-radius: 6px;
            font-size: 85%;
        }
        pre {
            background-color: var(--code-bg);
            padding: 16px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            overflow: auto;
            margin-bottom: 16px;
        }
        pre code {
            background-color: transparent;
            padding: 0;
            font-size: 100%;
            color: #e6edf3;
            display: block;
            line-height: 1.45;
        }
        .badge-container {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 25px;
        }
        .badge {
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 4px 12px;
            font-size: 0.85rem;
            color: var(--text-muted);
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .badge strong { color: var(--accent-color); }
        .tech-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .tech-card {
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 15px;
            text-align: center;
        }
        .tech-card h4 { margin: 0 0 8px 0; padding: 0; border: none; color: var(--accent-color); }
        .tech-card p { margin: 0; font-size: 0.9rem; color: var(--text-muted); }
        .callout {
            background-color: var(--accent-glow);
            border-left: 4px solid var(--accent-color);
            padding: 16px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 20px;
        }
        .callout p { margin: 0; }
        .architecture-step {
            margin-left: 10px;
            border-left: 2px dashed var(--border-color);
            padding-left: 20px;
            position: relative;
        }
        .architecture-step::before {
            content: "•";
            position: absolute;
            left: -6px;
            top: 0;
            color: var(--accent-color);
            background: var(--bg-color);
            width: 10px;
            height: 10px;
            text-align: center;
            line-height: 10px;
        }
    </style>
</head>
<body>

<div class="container">

    <h1>AI-Powered Legal Research and Drafting Assistant</h1>

    <div class="badge-container">
        <span class="badge">Architecture: <strong>Advanced RAG Pipeline</strong></span>
        <span class="badge">LLM Core: <strong>Llama 3.1</strong></span>
        <span class="badge">Inference: <strong>Groq API Fast Compute</strong></span>
        <span class="badge">Embeddings: <strong>HuggingFace Inference</strong></span>
        <span class="badge">Orchestration: <strong>LangChain Ecosystem</strong></span>
        <span class="badge">Interface: <strong>Streamlit</strong></span>
    </div>

    <div class="callout">
        <p><strong>Senior Developer Review Note:</strong> This repository demonstrates a production-grade blueprint for Domain-Specific Retrieval-Augmented Generation (RAG). By decoupling high-speed compute (Groq) from robust factual orchestration (LangChain) and local open-source embeddings, it addresses the critical legal tech requirements: low latency, high context fidelity, and predictable document structure extraction.</p>
    </div>

    <h2>1. Core Project Vision & Ideation</h2>
    <p>Legal practitioners are continuously bottlenecked by two highly resource-intensive phases: deep jurisprudential research across vast corpuses of statutory law/precedents, and the subsequent contextual drafting of precision legal instruments (memorandums, contracts, petitions). Standard commercial LLMs are ill-equipped for this out-of-the-box due to <em>hallucination tendencies</em>, <em>lack of deterministic citations</em>, and <em>domain-specific structural rigidities</em>.</p>
    <p>This system bridges that operational gap through an intelligent assistant that processes custom legal knowledge stores, isolates relevant statutory clauses, maps precedents, and generates high-fidelity legal drafts with auditable contextual grounding.</p>

    <h2>2. System Architecture & Technical Stack</h2>
    <p>The application relies on an enterprise-ready modular RAG stack designed to process unstructured documents and convert them into deterministic vector spaces for localized LLM reasoning.</p>

    <div class="tech-grid">
        <div class="tech-card">
            <h4>Orchestration</h4>
            <p><strong>LangChain</strong></p>
            <p>Manages robust document pipelines, memory context tracking, and semantic search routing templates.</p>
        </div>
        <div class="tech-card">
            <h4>Inference Engine</h4>
            <p><strong>Llama 3.1 via Groq</strong></p>
            <p>Utilizes ultra-low latency LPU hardware infrastructure to serve state-of-the-art token output speeds.</p>
        </div>
        <div class="tech-card">
            <h4>Vector Embeddings</h4>
            <p><strong>HuggingFace</strong></p>
            <p>Leverages deep transformer models locally or via endpoint to translate legal prose into geometric coordinates.</p>
        </div>
        <div class="tech-card">
            <h4>Delivery Front-End</h4>
            <p><strong>Streamlit UI</strong></p>
            <p>An intuitive, secure, responsive application layout engineered for lawyers and legal analysts.</p>
        </div>
    </div>

    <h3>Data Flight & Vectorization Lifecycle</h3>
    <div class="architecture-step">
        <p><strong>Ingestion & Parsing:</strong> Raw statutory files, PDF legal briefs, or contract templates are consumed and programmatically passed through optimized document loaders.</p>
    </div>
    <div class="architecture-step">
        <p><strong>Recursive Chunking:</strong> Text blocks are cleanly divided using overlapping text splits optimized to preserve complete legal definitions, entity linkages, and case clauses without fragmenting meaning.</p>
    </div>
    <div class="architecture-step">
        <p><strong>Mathematical Embedding:</strong> HuggingFace model architecture evaluates the semantic layers of each block, generating vector descriptions stored in an efficient system database.</p>
    </div>
    <div class="architecture-step">
        <p><strong>Contextual Querying:</strong> When a researcher asks a legal question or requests a draft, LangChain computes the mathematical match, retrieves the exact statutory paragraphs, maps them cleanly to a system prompt, and passes the context straight to Llama 3.1 via Groq.</p>
    </div>

    <h2>3. Production Installation & Local Setup</h2>
    <p>Ensure your infrastructure environment contains <code>Python 3.10+</code> before performing configuration steps.</p>

    <h3>Step 1: Clone the Target Repository</h3>
    <pre><code>git clone https://github.com/KanakDharamthok/AI-Powered-Legal-Research-and-Drafting-Assistant.git
cd AI-Powered-Legal-Research-and-Drafting-Assistant</code></pre>

    <h3>Step 2: Establish an Isolated Virtual Workspace</h3>
    <pre><code># Create virtual environment
python -m venv venv

# Activate on Linux/macOS
source venv/bin/activate

# Activate on Windows Power-shell
.\venv\Scripts\Activate.ps1</code></pre>

    <h3>Step 3: Install Required Dependencies</h3>
    <pre><code>pip install --upgrade pip
pip install -r requirements.txt</code></pre>

    <h3>Step 4: Environment Variables Setup (<code>.env</code>)</h3>
    <p>Create a fresh hidden environment parameters file in the project workspace directory root:</p>
    <pre><code>touch .env</code></pre>
    <p>Populate the file with your active service access provider keys:</p>
    <pre><code>GROQ_API_KEY=gsk_your_production_secret_key_here
HUGGINGFACEHUB_API_TOKEN=hf_your_active_token_here</code></pre>

    <h2>4. Execution & Running the Model</h2>
    <p>Once configuration settings evaluate successfully, initialize the core execution agent loop via Streamlit:</p>
    <pre><code>streamlit run app.py</code></pre>
    
    <p>The system launcher automatically handles service routing, prints active local port assignments, and routes the application straight to your primary browser workspace window:</p>
    <pre><code>Network URL: http://localhost:8501</code></pre>

    <h2>5. Advanced Operational Usage</h2>
    <ul>
        <li><strong>Factual Legal Q&A:</strong> Drop document archives into the app context window. Ask specific questions (e.g., <em>"What are the specific conditions precedent for contract termination under Section 12?"</em>). The application extracts the exact target clauses without processing extraneous data.</li>
        <li><strong>Precision Drafting:</strong> Pass legal templates or raw notes, choose the document output style guidelines, and allow the Llama 3.1 execution loop to structure clean boilerplate files complete with clear citation paths.</li>
    </ul>

    <h2>6. Architectural Best Practices & Security Guidelines</h2>
    <ul>
        <li><strong>Deterministic Prompts:</strong> System configuration instructions explicitly prevent the model from generating information outside the provided text, mitigating typical generative AI risks.</li>
        <li><strong>API Safety Management:</strong> Sensitive system variables remain protected inside local hardware storage layers using <code>python-dotenv</code>, isolating them from public repository mirrors.</li>
    </ul>

</div>

</body>
</html>
