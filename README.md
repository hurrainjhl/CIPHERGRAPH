# CipherGraph — Automated CTI Knowledge Graph Platform

<p align="center">
  <strong>Turn unstructured Cyber Threat Intelligence reports into an interactive, searchable knowledge graph.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Project-CipherGraph-6f42c1?style=for-the-badge" alt="CipherGraph">
  <img src="https://img.shields.io/badge/Domain-Cyber%20Threat%20Intelligence-0b7285?style=for-the-badge" alt="CTI">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge" alt="FastAPI">
  <img src="https://img.shields.io/badge/Graph-Neo4j-008CC1?style=for-the-badge" alt="Neo4j">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/LLM-GPT--4o--mini-412991?style=flat-square" alt="GPT-4o-mini">
  <img src="https://img.shields.io/badge/Frontend-HTML%20%7C%20Tailwind%20%7C%20JavaScript-F7DF1E?style=flat-square" alt="Frontend">
  <img src="https://img.shields.io/badge/Visualization-vis--network-2ea44f?style=flat-square" alt="vis-network">
  <img src="https://img.shields.io/badge/Containerization-Docker%20Compose-2496ED?style=flat-square" alt="Docker">
</p>

---

## 📌 Overview

**CipherGraph** is an automated Cyber Threat Intelligence (CTI) knowledge graph platform designed to transform raw threat reports into structured, explorable intelligence.

The platform accepts unstructured CTI reports through text input or file upload, uses an LLM to extract entities and relationships, stores the resulting information as a graph, and presents the intelligence through an interactive web interface.

The project was developed as a Cyber Threat Intelligence semester project and reached a fully functional prototype state.

---
## Screenshots

<p align="center">
  <img width="100%" alt="CipherGraph Dashboard" src="https://github.com/hurrainjhl/CIPHERGRAPH/blob/main/Screenshot%202026-08-15%20013445.png?raw=true" />
</p>
---

## 🎯 The Problem

CTI information is often scattered across reports, blogs, PDFs, and other sources. Analysts may need to manually identify and correlate:

- Threat actors
- Malware and tools
- Indicators of compromise
- Victims and targeted sectors
- Techniques
- Relationships between entities

CipherGraph addresses this problem by automatically converting unstructured intelligence into a graph that can be searched and investigated.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
|  **Report Ingestion** | Accept plain text or upload `.txt`, `.md`, and `.json` reports |
|  **LLM Extraction** | Extract entities and relationships automatically using GPT-4o-mini |
|  **Knowledge Graph** | Store CTI entities and relationships in Neo4j |
|  **Demo Mode** | Fall back to in-memory storage when Neo4j is unavailable |
|  **Async Processing** | Process long LLM extractions without blocking the UI |
|  **Search & Filtering** | Search entity names and filter by entity type |
|  **Entity Resolution** | Normalize aliases such as _Fancy Bear_, _APT-28_, and _FancyBear_ |
|  **Investigation Panel** | Explore relationships and receive natural‑language summaries |
|  **Multi‑Tenancy** | Isolate workspaces using `group_id` |
|  **Optional Authentication** | Protect API requests using `X-CipherGraph-Key` |
|  **Health Check** | Verify application availability through `/health` |
|  **Graceful Degradation** | Continue operating in demo mode without Neo4j or other optional services |
|  **Interactive Graph** | Zoom, pan, click nodes, and explore relationships |

---

##  Architecture

CipherGraph uses an async-first three-tier architecture:

```
┌───────────────────────────────┐
│       Web Browser / UI        │
│ HTML + Tailwind + JavaScript  │
│        vis-network            │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│        FastAPI Backend        │
│                               │
│  • REST API                   │
│  • Async ingestion            │
│  • Task polling               │
│  • Entity resolution          │
│  • Authentication             │
└───────────────┬───────────────┘
                │
       ┌────────┴─────────┐
       ▼                  ▼
┌───────────────┐  ┌────────────────┐
│     Neo4j     │  │ In-Memory Mode  │
│ Persistent DB │  │   Demo/Fallback │
└───────────────┘  └────────────────┘
                │
                ▼
        ┌─────────────────┐
        │ LLM Extraction  │
        │ GPT-4o-mini via │
        │   OpenRouter    │
        └─────────────────┘
```

  
##  Technology Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python, FastAPI, Uvicorn, httpx, asynchronous APIs |
| **Intelligence Extraction** | GPT-4o-mini via OpenRouter, structured JSON extraction |
| **Graph Database** | Neo4j, async Neo4j driver, Cypher queries |
| **Optional Embeddings** | Ollama, `mxbai-embed-large` |
| **Frontend** | HTML5, Tailwind CSS, Vanilla JavaScript, vis‑network |
| **Deployment** | Docker, Docker Compose |

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <YOUR-REPOSITORY-URL>
cd CipherGraph
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

- **Windows:** `.venv\Scripts\activate`
- **Linux/macOS:** `source .venv/bin/activate`

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Credentials

If the project configuration requires an LLM provider, configure the required API key through the environment/configuration mechanism used by the repository.

For example:

```env
OPENROUTER_API_KEY=your_api_key_here
```

>  **Never commit API keys, passwords, database credentials, or other secrets to GitHub.**

### 5. Start the Application

The backend is designed to serve the frontend itself. Use the appropriate startup command. For example:

```bash
uvicorn main:app --reload
```

Then open:

```
http://127.0.0.1:8000
```

---

##  Docker

CipherGraph supports Docker Compose for services such as Neo4j and optional Ollama components.

**Typical workflow:**

```bash
docker compose up --build
```

**To run in the background:**

```bash
docker compose up -d --build
```

**To stop the services:**

```bash
docker compose down
```

## Suggested Project Structure

```
CipherGraph/
│
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── tests/
│
├── README.md
└── .env.example
```

## Future Improvements

Potential future enhancements include:

-  Unit tests with `pytest` and mocking
-  API rate limiting
-  Structured JSON logging
-  Full‑text search using Elasticsearch or Neo4j‑native search
-  Vector similarity / semantic search
-  JWT authentication with refresh tokens
- STIX/TAXII import and export
- Role‑based access control
-  Improved graph scalability
-  Production deployment support

---

##  Contributors

* **[Hoor ul ein Soomro](https://github.com/hurrainjhl)** 
* **[Affaf Ahmad](https://github.com/Affafahmad)** 
* **[Sumaiya Arshad](https://github.com/pickachu19)** 
* **[Marryum Afzaal](https://github.com/marryum2004)**



---

##  License

*MIT License*

---

## Acknowledgements

CipherGraph builds upon the following technologies and concepts:

- FastAPI
- Neo4j
- OpenAI GPT-4o-mini
- OpenRouter
- Ollama
- Tailwind CSS
- vis‑network
- Docker
- Python

Special thanks to the **Cyber Threat Intelligence course/project environment** for providing the context in which CipherGraph was designed and developed.

---

<p align="center">
  <strong>🕸️ CipherGraph — Connect the Threat Intelligence.</strong>
</p>

<p align="center">
  <strong>Built with ❤️ for the cybersecurity community</strong>
</p>
```

