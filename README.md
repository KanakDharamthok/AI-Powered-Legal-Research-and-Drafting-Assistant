```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI-Powered Legal Research & Drafting Assistant</title>
</head>

<body>

<div align="center">

<h1>⚖️ AI-Powered Legal Research & Drafting Assistant (APLRDA)</h1>

<h3>
An End-to-End Courtroom Intelligence System for Legal Research,
Loophole Detection & Automated Bail Draft Generation
</h3>

<p>
<b>AI • Legal Research • Courtroom Intelligence • RAG • Draft Automation</b>
</p>

</div>

<hr>

<h2>🚀 Project Overview</h2>

<p>
<b>AI-Powered Legal Research & Drafting Assistant (APLRDA)</b> is a comprehensive
Legal AI platform designed to assist advocates, interns, and legal researchers
throughout the entire litigation workflow.
</p>

<p>
The platform combines courtroom audio transcription, legal document analysis,
Retrieval-Augmented Generation (RAG), procedural loophole detection, and
automated bail drafting into a single unified legal intelligence ecosystem.
</p>

<p>
Unlike conventional legal chatbots that simply answer questions, APLRDA acts
as a legal co-pilot capable of analyzing FIRs, chargesheets, court orders,
notice board fragments, and courtroom proceedings to identify procedural
violations and generate court-ready legal drafts.
</p>

<hr>

<h2>🛑 Problem Statement</h2>

<ul>
<li>Manual legal research consumes significant time and effort.</li>
<li>Procedural loopholes often remain undetected.</li>
<li>Courtroom documentation is difficult due to multilingual proceedings.</li>
<li>Drafting bail applications requires extensive legal expertise.</li>
<li>Existing legal tools operate in isolated workflows.</li>
</ul>

<hr>

<h2>💡 Solution</h2>

<p>
APLRDA introduces a complete AI-powered legal workflow that automates:
</p>

<ul>
<li>🎙️ Courtroom Audio Intelligence</li>
<li>📄 Legal Document Parsing</li>
<li>📚 Legal Knowledge Retrieval (RAG)</li>
<li>🔍 Procedural Loophole Detection</li>
<li>📝 Automated Bail Draft Generation</li>
</ul>

<hr>

<h2>✨ Core Features</h2>

<h3>🎙️ Courtroom Audio Intelligence</h3>

<ul>
<li>Whisper-based speech recognition</li>
<li>Hindi, Marathi & English courtroom support</li>
<li>Silero Voice Activity Detection</li>
<li>Noise suppression</li>
<li>Transcript normalization using Gemma2</li>
</ul>

<h3>📄 Legal Document Intelligence</h3>

<ul>
<li>FIR Parsing</li>
<li>Chargesheet Analysis</li>
<li>Court Order Processing</li>
<li>PDF Extraction</li>
<li>Notice Board Parsing</li>
<li>Fact Extraction</li>
</ul>

<h3>📚 Legal Knowledge Retrieval (RAG)</h3>

<ul>
<li>BNS Knowledge Base</li>
<li>BNSS Knowledge Base</li>
<li>Bail Granted Judgments</li>
<li>Bail Rejected Judgments</li>
<li>Semantic Search using ChromaDB</li>
</ul>

<h3>🔍 Loophole Detection Engine</h3>

<ul>
<li>Procedural Violations</li>
<li>Evidentiary Gaps</li>
<li>Contradictions</li>
<li>Defense Recommendations</li>
<li>Bail Eligibility Analysis</li>
</ul>

<h3>📝 Automated Draft Generation</h3>

<ul>
<li>Sessions Court Bail Applications</li>
<li>High Court Bail Applications</li>
<li>Supreme Court SLP Drafts</li>
<li>Court-Ready Legal Documents</li>
</ul>

<hr>

<h2>🏗️ System Architecture</h2>

<pre>
Court Audio + Legal Documents
                │
                ▼
      Document & Audio Processing
                │
                ▼
        Fact Extraction Engine
                │
                ▼
        Legal Knowledge Retrieval
             (RAG Layer)
                │
                ▼
       Loophole Detection Engine
                │
                ▼
       Automated Draft Generator
                │
                ▼
      Court-Ready Legal Documents
</pre>

<hr>

<h2>🛠️ Technology Stack</h2>

<table border="1" cellpadding="8">

<tr>
<th>Category</th>
<th>Technology</th>
</tr>

<tr>
<td>Frontend</td>
<td>Streamlit</td>
</tr>

<tr>
<td>Backend</td>
<td>FastAPI, Uvicorn</td>
</tr>

<tr>
<td>Speech AI</td>
<td>Whisper, Silero VAD</td>
</tr>

<tr>
<td>LLM</td>
<td>Ollama, Gemma2</td>
</tr>

<tr>
<td>Vector Database</td>
<td>ChromaDB</td>
</tr>

<tr>
<td>Embeddings</td>
<td>BAAI/bge-small-en-v1.5</td>
</tr>

<tr>
<td>Document Processing</td>
<td>PDFPlumber, OCR Pipeline</td>
</tr>

<tr>
<td>Validation</td>
<td>Pydantic</td>
</tr>

<tr>
<td>Language</td>
<td>Python</td>
</tr>

</table>

<hr>

<h2>📂 Project Directory Structure</h2>

<pre>
APLRDA/
│
├── app.py
├── main.py
├── requirements.txt
├── .env
├── .gitignore
│
├── src/
│   ├── transcription_engine.py
│   ├── document_parser_module2.py
│   ├── llm_parser.py
│   ├── rag_engine.py
│   ├── loophole_detector.py
│   └── draft_generator.py
│
├── data/
│   ├── chroma_db/
│   └── knowledge_base/
│       ├── statutes/
│       └── precedents/
│
├── saved_drafts/
│
└── venv/
</pre>

<hr>

<h2>🤝 Contributions</h2>

<p>
Contributions, feature requests, pull requests, and bug reports are welcome!
</p>

<h3>Contribution Workflow</h3>

<pre>
Fork Repository
      ↓
Create Feature Branch
      ↓
Implement Changes
      ↓
Commit Updates
      ↓
Submit Pull Request
      ↓
Code Review & Merge
</pre>

<p>
<b>Fork → Code → Pull Request ✔️</b>
</p>

<hr>

<h2>📬 Contact</h2>

<p>
👨‍💻 <b>Developer:</b> Kanak Dharamthok
</p>

<p>
📧 <b>Email:</b>
<a href="mailto:your-email@example.com">
your-email@example.com
</a>
</p>

<p>
🐙 <b>GitHub:</b>
<a href="https://github.com/your-github-username">
your-github-username
</a>
</p>

<p>
💼 <b>Domain:</b> AI/ML • Legal AI • NLP • RAG Systems
</p>

<hr>

<div align="center">

<h2>⭐ Support the Project</h2>

<p>
If you find this project useful:
</p>

<p>
⭐ Star the Repository |
🍴 Fork the Project |
📢 Share with Others |
🤝 Contribute
</p>

<br>

<h3>
⚖️ AI-Powered Legal Research & Drafting Assistant (APLRDA)
</h3>

<p>
Transforming Legal Research, Procedural Analysis, and Bail Drafting
through Artificial Intelligence.
</p>

<p>
Made with ❤️ using Python, FastAPI, Streamlit, ChromaDB,
Whisper, Ollama & Gemma2.
</p>

</div>

</body>
</html>
```
