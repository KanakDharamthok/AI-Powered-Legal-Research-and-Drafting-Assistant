<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Powered Legal Research and Drafting Assistant</title>
    <style>
        :root {
            --bg-color: #0d1117;
            --text-color: #c9d1d9;
            --text-muted: #8b949e;
            --accent-color: #58a6ff;
            --border-color: #30363d;
            --code-bg: #161b22;
            --callout-bg: rgba(88, 166, 255, 0.1);
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            padding: 2rem;
            max-width: 950px;
            margin: 0 auto;
        }
        h1, h2, h3 {
            color: #f0f6fc;
            font-weight: 600;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.3em;
        }
        h1 { font-size: 2.25em; border-bottom: 2px solid var(--border-color); margin-bottom: 5px; }
        h2 { font-size: 1.5em; margin-top: 30px; }
        h3 { font-size: 1.25em; border-bottom: none; }
        p, ul, ol { margin-bottom: 16px; }
        ul { padding-left: 2em; list-style-type: disc; }
        li { margin-top: 0.25em; }
        a { color: var(--accent-color); text-decoration: none; }
        a:hover { text-decoration: underline; }
        hr { height: 0.25em; padding: 0; margin: 24px 0; background-color: var(--border-color); border: 0; }
        code {
            font-family: ui-monospace, SFMono-Regular, SF Mono, Consolas, monospace;
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
        }
        pre code {
            background-color: transparent;
            padding: 0;
            font-size: 100%;
            color: #e6edf3;
            display: block;
        }
        .subtitle {
            font-size: 1.25rem;
            color: var(--text-muted);
            margin-bottom: 15px;
            font-weight: 400;
        }
        .callout {
            background-color: var(--callout-bg);
            border-left: 4px solid var(--accent-color);
            padding: 16px;
            border-radius: 0 8px 8px 0;
            margin: 20px 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 16px;
        }
        table th, table td {
            padding: 12px;
            border: 1px solid var(--border-color);
            text-align: left;
        }
        table th {
            background-color: var(--code-bg);
            color: #f0f6fc;
        }
        table tr:nth-child(even) {
            background-color: rgba(110, 118, 129, 0.05);
        }
    </style>
</head>
<body>

    <h1>⚖️ AI-Powered Legal Research and Drafting Assistant</h1>
    <div class="subtitle"><strong>Enterprise-Grade Legal Knowledge Retrieval & Contextual Document Synthesis Hub</strong></div>

    <p>🌐 <strong>Live Prototype Link:</strong> <a href="https://github.com/KanakDharamthok/AI-Powered-Legal-Research-and-Drafting-Assistant" target="_blank">GitHub Repository Workspace</a></p>

    <hr>

    <h2>🚀 Project Overview</h2>
    <p><strong>AI-Powered Legal Research and Drafting Assistant</strong> is a production-tier legal tech framework engineered to automate corporate compliance analysis, case law synthesis, and document drafting pipelines. Moving past basic, hallucination-prone generic LLM completions, this system implements a strict, domain-calibrated <strong>Retrieval-Augmented Generation (RAG)</strong> architecture.</p>
    <p>Optimized using <strong>LangChain</strong> orchestration and fueled by <strong>Meta's Llama 3.1</strong> model via <strong>Groq Cloud's LPU (Language Processing Unit)</strong> hardware-accelerated infrastructure, the system delivers sub-second statutory document extraction and legal brief generation with predictable, deterministic formatting.</p>

    <hr>

    <h2>🛑 Problem Statement</h2>
    <ul>
        <li><strong>The Hallucination Liability:</strong> Standard commercial generative models hallucinate pseudo-legal precedents, creating severe professional liabilities in high-stakes legal situations.</li>
        <li><strong>Citation & Anchoring Deficiencies:</strong> Traditional foundational models lack deep, auditable citation mechanisms to trace structural outputs back to raw legal statutes.</li>
        <li><strong>Document Density Bottlenecks:</strong> Parsing massive multi-page statutory documents or corporate contracts creates token queues that break real-time production UX.</li>
        <li><strong>Structural Rigidity Failure:</strong> Standard AI configurations struggle with the strict linguistic tone, boilerplate logic, and specific visual hierarchies required for legal briefs and agreements.</li>
    </ul>

    <hr>

    <h2>💡 Solution</h2>
    <p>A precision-tuned, high-speed legal co-pilot dashboard providing:</p>
    <ul>
        <li><strong>Context-Bounded Extraction:</strong> Restricts the LLM’s focus exclusively to validated legal datasets, eliminating generic creative fabrications.</li>
        <li><strong>Hardware-Accelerated Token Delivery:</strong> Sub-second processing speeds for multi-page documents via Groq's specialized LPU clusters.</li>
        <li><strong>Dynamic Drafting Templates:</strong> Automated boilerplate structure mapping for contracts, non-disclosure agreements, and petitions.</li>
        <li><strong>Clean Professional Layout:</strong> An intuitive, clutter-free legal research terminal engineered for rapid workspace review.</li>
    </ul>

    <hr>

    <h2>✨ Key Features</h2>
    <ul>
        <li>📁 <strong>Advanced Document Ingestion Workspace:</strong> Seamlessly upload complex statutory papers, PDFs, and legal briefs directly into a localized data processing loop.</li>
        <li>🧠 <strong>Deterministic Citation Mapping:</strong> Pinpoints the exact structural clauses and semantic segments of source data used to assemble responses.</li>
        <li>⚡ <strong>Hyperparameter Optimization Panel:</strong> Adjust parameters like temperature vectors and inference tokens mid-session to balance creative drafting flexibility with hard-coded factual synthesis.</li>
        <li>📖 <strong>Domain-Specific Legal Prompts:</strong> System designs feature layered prompt guardrails that enforce formal courtroom phrasing, precise terminology, and accurate formatting.</li>
        <li>🎨 <strong>Premium CSS Professional Styling:</strong> Modern, high-visibility user dashboard constructed using sleek glassmorphism boundaries, responsive status modules, and focused data layouts.</li>
    </ul>

    <hr>

    <h2>🎯 Dual-Channel Operational Workflows</h2>
    
    <h3>🔍 1. Statutory Deep Research Channel</h3>
    <ul>
        <li>Interactive conversational engine running real-time context streaming.</li>
        <li>Translates text into high-density mathematical vector spaces to query relevant case laws.</li>
        <li>Instantly isolates specific compliance codes or regulatory sections buried in raw data.</li>
    </ul>

    <h3>✍️ 2. Automated Precision Drafting Channel</h3>
    <ul>
        <li>Converts raw analytical research insights directly into legally sound document structures.</li>
        <li>Automatically populates boilerplate legal elements (e.g., *Indemnification, Severability, Governing Law*).</li>
        <li>Generates downloadable, polished outputs pre-formatted to match industry drafting criteria.</li>
    </ul>

    <hr>

    <h2>🧠 Supported Inference Engines & Token Infrastructure</h2>
    <p>The architecture relies on LangChain's <code>ChatGroq</code> connector ecosystem to route incoming context arrays directly into open-weight model pipelines deployed on hardware-accelerated LPU clusters.</p>

    <h3>1. Core Production Architectures</h3>
    <ul>
        <li><strong><code>llama-3.1-8b-instant</code></strong> (Primary Execution Layer): Leverages a massive 128K context window at ultra-low latency. Optimized for instantaneous chat analysis and rapid document lookups.</li>
        <li><strong><code>llama-3.3-70b-versatile</code></strong> (Heavy Reasoning Layer): High-capacity model optimized to handle deep structural analysis, complex logical routing, and comprehensive macro-contract assembly.</li>
    </ul>

    <h3>2. Extensible Cross-Platform Model Catalog</h3>
    <table>
        <thead>
            <tr>
                <th>Model ID Path</th>
                <th>Provider Node</th>
                <th>Context Capacity</th>
                <th>Optimal Operational Profile</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong><code>qwen3-32b</code></strong></td>
                <td>Alibaba (Qwen)</td>
                <td>128K Tokens</td>
                <td>Cross-border regulatory cross-referencing and multi-lingual documentation.</td>
            </tr>
            <tr>
                <td><strong><code>openai/gpt-oss-120b</code></strong></td>
                <td>Open Source Community</td>
                <td>131K Tokens</td>
                <td>High-density multi-party contract logic and macro-chain validation.</td>
            </tr>
            <tr>
                <td><strong><code>gemma-7b-it</code></strong></td>
                <td>Google Architecture</td>
                <td>8K Tokens</td>
                <td>Ultra-lightweight local processing workflows for specific compliance checklists.</td>
            </tr>
        </tbody>
    </table>

    <hr>

    <h2>🛠️ Technology Stack</h2>
    <ul>
        <li><strong>UI Delivery Layer:</strong> Streamlit (Integrated Custom HTML5/CSS3 Style Shell)</li>
        <li><strong>Pipeline Orchestration Framework:</strong> LangChain Core & Advanced Prompt Components</li>
        <li><strong>Vector Processing & Embeddings:</strong> Localized HuggingFace Inference Models</li>
        <li><strong>Hardware Compute Infrastructure:</strong> Groq Cloud LPU Hyper-Speed Engine</li>
        <li><strong>Underlying Models:</strong> Meta Llama 3.1 Suite</li>
        <li><strong>Context Preservation:</strong> Python Environment Dotenv (<code>.env</code> System Isolation)</li>
    </ul>

    <hr>

    <h2>📂 Project Workspace Directory</h2>
    <pre><code>├── .venv/               # Isolated local Python virtual runtime workspace
├── .env                 # Safe environment storage (Masks GROQ_API_KEY & HF_TOKEN)
├── .gitignore           # Keeps API tokens and dependencies out of public repositories
├── app.py               # Central execution file: Streamlit interface, custom CSS, and RAG routing
└── requirements.txt     # Locked production-level dependencies file</code></pre>

    <hr>

    <h2>⚡ Rapid Local Deployment</h2>
    
    <p>Ensure you have <code>Python 3.10+</code> configured in your environment before running installation commands.</p>

    <h3>1. Clone the Source Repository</h3>
    <pre><code>git clone https://github.com/KanakDharamthok/AI-Powered-Legal-Research-and-Drafting-Assistant.git
cd AI-Powered-Legal-Research-and-Drafting-Assistant</code></pre>

    <h3>2. Launch an Isolated Virtual Workspace</h3>
    <pre><code>python -m venv .venv
# Linux / macOS Activation
source .venv/bin/activate
# Windows PowerShell Activation
.\.venv\Scripts\Activate.ps1</code></pre>

    <h3>3. Install Core Production Libraries</h3>
    <pre><code>pip install --upgrade pip
pip install -r requirements.txt</code></pre>

    <h3>4. Set Up Environment Secrets</h3>
    <p>Create a <code>.env</code> file in the project's root folder:</p>
    <pre><code>GROQ_API_KEY=gsk_your_live_production_lpu_key_here
HUGGINGFACEHUB_API_TOKEN=hf_your_active_token_here</code></pre>

    <h3>5. Launch the Application Instance</h3>
    <pre><code>streamlit run app.py</code></pre>
    <div class="callout">
        <p>🚀 <strong>System Note:</strong> The local development server will spin up instantly. Open your browser and navigate to the local hosting port at <code>http://localhost:8501</code> to access the dashboard.</p>
    </div>

</body>
</html>
