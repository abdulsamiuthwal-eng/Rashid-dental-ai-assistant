# Rashid Dental AI Assistant

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0--alpha-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688)
![License](https://img.shields.io/badge/license-MIT-yellow)
![Status](https://img.shields.io/badge/status-In%20Development-orange)

**An intelligent AI-powered dental assistant for Rashid Dental Clinic, built with RAG, Gemini, and FastAPI.**

*DEVFORGE AI/ML Internship — Project 2*

</div>

---

## Table of Contents

- [Project Overview](#project-overview)
- [Objectives](#objectives)
- [Planned Features](#planned-features)
- [Tech Stack](#tech-stack)
- [Project Architecture](#project-architecture)
- [Folder Structure](#folder-structure)
- [Development Roadmap](#development-roadmap)
- [Setup Instructions](#setup-instructions)
- [Day 3 — Retrieval Pipeline](#day-3--retrieval-pipeline)
- [Day 4 — AI Chat Backend](#day-4--ai-chat-backend)
- [Day 5 — Frontend & Chatbot Widget](#day-5--frontend--chatbot-widget)
- [Security Notes](#security-notes)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

The **Rashid Dental AI Assistant** is an intelligent chatbot application designed for Rashid Dental Clinic. It answers patient questions using a verified Markdown knowledge base, powered by a **Retrieval-Augmented Generation (RAG)** pipeline with Google Gemini as the language model.

The system is purpose-built to:

- Provide accurate, knowledge-grounded responses (no hallucination).
- Assist patients with clinic information, services, and appointment requests.
- Operate safely within medical guardrails — it **never** gives diagnoses or prescriptions.
- Surface answers **only** from verified clinic documentation.

> **Disclaimer:** This AI assistant is an informational tool only. It is not a substitute for professional dental advice, diagnosis, or treatment. Always consult a qualified dentist.

---

## Objectives

| # | Objective |
|---|-----------|
| 1 | Build a production-ready AI chatbot for a dental clinic |
| 2 | Implement RAG pipeline using FAISS + Gemini |
| 3 | Ground all answers in verified Markdown knowledge base |
| 4 | Enable appointment request collection via conversation |
| 5 | Deliver a premium, responsive clinic website with chatbot widget |
| 6 | Enforce medical safety guardrails and ethical AI practices |
| 7 | Maintain full deployment readiness with documentation |

---

## Planned Features

> **Note:** Features marked 🔜 are planned for future development phases. Only completed features are marked ✅.

### Foundation (Day 1)
- ✅ Professional project architecture
- ✅ Clean, modular folder structure
- ✅ Markdown knowledge base (clinic information)
- ✅ System prompt with medical safety guardrails
- ✅ Development roadmap and documentation

### Backend (Days 2–4) ✅
- ✅ FastAPI REST API with versioning (Core Foundation)
- ✅ Structured logging with Loguru
- ✅ PostgreSQL database with SQLAlchemy ORM (Core database layer)
- ✅ RAG pipeline — Markdown document loading
- ✅ Heading-based text chunking
- ✅ Google Embedding-001 embedding generation
- ✅ FAISS vector store integration (build, persist, load, auto-rebuild)
- ✅ Semantic similarity retrieval engine with source attribution
- ✅ Google Gemini LLM integration (via `POST /api/v1/chat`)
- ✅ Conversation memory management (session-based, in-memory)
- ✅ Source attribution with every AI response
- ✅ Safety guardrails (no diagnosis, no medication, injection detection)
- ✅ Appointment request collection system (API + database + chatbot flow)
- ✅ Emergency detection and escalation
- 🔜 Alembic database migrations
- 🔜 Rate limiting and security middleware (SlowAPI rate limiter configurations)

### Frontend (Day 5) ✅
- ✅ Premium responsive clinic website (hero, services, about, why-choose-us, contact, footer)
- ✅ Floating chatbot widget with open/close, typing indicator, auto-scroll
- ✅ Smooth animations (fade-up, card hover, scroll reveal, chatbot spring-open)
- ✅ Services showcase with hover cards
- ✅ Suggested questions with one-click sending
- ✅ Mobile-first responsive design (desktop, tablet, mobile)
- ✅ Accessibility (ARIA labels, keyboard nav, semantic HTML, contrast)
- ✅ Backend integration with `POST /api/v1/chat` via Fetch API

### Quality & Deployment (Days 7–8) 🔜
- 🔜 Comprehensive unit and integration tests
- 🔜 Docker containerization
- 🔜 Nginx reverse proxy configuration
- 🔜 CI/CD pipeline
- 🔜 Complete API documentation
- 🔜 Deployment to cloud platform

---

## Tech Stack

### Backend
| Component | Technology |
|-----------|-----------|
| Web Framework | FastAPI 0.111 |
| ASGI Server | Uvicorn |
| Language Model | Google Gemini 1.5 Flash/Pro |
| RAG Orchestration | LangChain |
| Vector Store | FAISS (CPU) |
| Database ORM | SQLAlchemy 2.0 (async) |
| Database Driver | AsyncPG + Psycopg2 |
| Database | PostgreSQL 15+ |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Authentication | JWT (python-jose) |
| Logging | Loguru |

### Frontend
| Component | Technology |
|-----------|-----------|
| Markup | HTML5 + Semantic Elements |
| Styling | Vanilla CSS (Custom Properties) |
| Scripting | Vanilla JavaScript (ES2022+) |
| Design System | Custom — Healthcare Premium Theme |
| Font | Inter (Google Fonts) |

### AI / ML
| Component | Technology |
|-----------|-----------|
| LLM | Google Gemini 1.5 Flash |
| Embeddings | Google Embedding-001 |
| Vector Search | FAISS |
| Pipeline | LangChain RAG |
| Knowledge Base | Markdown files |
| Chunking | Heading-based chunking |

### DevOps
| Component | Technology |
|-----------|-----------|
| Containerization | Docker + Docker Compose |
| Reverse Proxy | Nginx |
| Environment | Python-dotenv |
| Testing | Pytest + Pytest-AsyncIO |
| Linting | Ruff + MyPy |
| Git Hooks | Pre-commit |

---

## Project Architecture

The project follows **Clean Architecture** principles with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                        USER / PATIENT                        │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP / WebSocket
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    WEBSITE (Frontend)                        │
│           Premium Clinic Landing Page + Chatbot Widget       │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST API calls
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  API Layer   │  │  Middleware  │  │  Rate Limiting   │  │
│  │  (Routes)    │  │  (CORS/Auth) │  │  (SlowAPI)       │  │
│  └──────┬───────┘  └──────────────┘  └──────────────────┘  │
│         │                                                    │
│  ┌──────▼───────────────────────────────────────────────┐   │
│  │                  Service Layer                        │   │
│  │  ┌───────────────────┐  ┌────────────────────────┐   │   │
│  │  │   RAG Service     │  │  Appointment Service    │   │   │
│  │  │  ┌─────────────┐  │  │  (Collection + Store)  │   │   │
│  │  │  │ Doc Loader  │  │  └────────────────────────┘   │   │
│  │  │  │ (Markdown)  │  │                               │   │
│  │  │  ├─────────────┤  │  ┌────────────────────────┐   │   │
│  │  │  │  Chunker    │  │  │   AI Service           │   │   │
│  │  │  │ (Heading)   │  │  │   (Gemini Client)      │   │   │
│  │  │  ├─────────────┤  │  └────────────────────────┘   │   │
│  │  │  │  Embedder   │  │                               │   │
│  │  │  │  (Google)   │  │  ┌────────────────────────┐   │   │
│  │  │  ├─────────────┤  │  │   Memory Service       │   │   │
│  │  │  │   FAISS     │  │  │   (Conversation)       │   │   │
│  │  │  │  Retriever  │  │  └────────────────────────┘   │   │
│  │  │  ├─────────────┤  │                               │   │
│  │  │  │   Gemini    │  │                               │   │
│  │  │  │    LLM      │  │                               │   │
│  │  │  └─────────────┘  │                               │   │
│  │  └───────────────────┘                               │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                 Data Layer                            │   │
│  │  ┌───────────────┐      ┌─────────────────────────┐  │   │
│  │  │  FAISS Index  │      │   PostgreSQL Database   │  │   │
│  │  │  (Vectors)    │      │   (Appointments/Logs)   │  │   │
│  │  └───────────────┘      └─────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Architecture Decisions

| Decision | Rationale |
|----------|-----------|
| **Clean Architecture** | Separates business logic from infrastructure; enables testing without real DB/AI |
| **RAG over Fine-tuning** | Knowledge base updates don't require model retraining; verifiable sources |
| **FAISS over cloud vector DB** | No API cost, runs locally, sufficient for clinic-scale data |
| **Heading-based chunking** | Preserves semantic context; prevents mid-sentence splits |
| **PostgreSQL** | ACID compliance for appointment data; production-grade reliability |
| **Markdown knowledge base** | Human-readable; easy to update by non-technical staff |
| **Pydantic v2** | Runtime validation; auto-generates API docs; type safety |
| **Async SQLAlchemy** | Non-blocking DB operations; supports high concurrency |

---

## Folder Structure

```
Rashid-Dental-AI-Assistant/
│
├── backend/                          # FastAPI application
│   └── app/
│       ├── api/v1/
│       │   ├── endpoints/            # Route handlers (chat, appointments, health)
│       │   └── middleware/           # Request/response middleware
│       ├── core/                     # App configuration, security, logging
│       ├── models/                   # SQLAlchemy ORM models
│       ├── schemas/                  # Pydantic request/response schemas
│       ├── services/
│       │   ├── ai/                   # Gemini client, embeddings
│       │   ├── rag/                  # RAG pipeline (loader, chunker, retriever)
│       │   └── appointment/          # Appointment business logic
│       ├── repositories/             # Data access layer (DB operations)
│       ├── utils/                    # Shared utilities
│       └── exceptions/               # Custom exception classes
│
├── knowledge-base/                   # Markdown knowledge base (Single Source of Truth)
│   ├── clinic-overview.md
│   ├── services.md
│   ├── dentists.md
│   ├── timings-and-location.md
│   ├── appointments.md
│   ├── pricing.md
│   ├── frequently-asked-questions.md
│   ├── emergency-guidance.md
│   └── chatbot-safety-policy.md
│
├── database/
│   ├── migrations/                   # Alembic migration files
│   ├── seeds/                        # Database seed scripts
│   └── schemas/                      # Schema documentation
│
├── frontend/                         # Website + chatbot widget
│   ├── public/                       # Static assets
│   └── src/
│       ├── components/               # UI components
│       ├── styles/                   # CSS stylesheets
│       └── scripts/                  # JavaScript modules
│
├── tests/
│   ├── unit/                         # Unit tests (isolated, no external deps)
│   ├── integration/                  # Integration tests (with DB/API)
│   ├── e2e/                          # End-to-end tests
│   └── fixtures/                     # Shared test data
│
├── docs/
│   ├── api/                          # API reference documentation
│   ├── architecture/                 # Architecture diagrams and decisions
│   ├── deployment/                   # Deployment guides
│   └── development/                  # Developer setup guides
│
├── assets/
│   ├── brand/                        # Logos, color palettes
│   ├── mockups/                      # UI/UX wireframes and mockups
│   └── diagrams/                     # Architecture diagrams
│
├── deployment/
│   ├── docker/                       # Dockerfiles
│   ├── nginx/                        # Nginx configuration
│   └── scripts/                      # Deployment automation scripts
│
├── scripts/                          # Developer utility scripts
├── config/                           # Environment-specific configuration
│
├── .gitignore
├── .env.example
├── requirements.txt
└── README.md
```

---

## Development Roadmap

### Day 1 — Project Foundation ✅
**Objective:** Establish a professional, scalable project foundation.
- ✅ Architecture design (Clean Architecture, SOLID)
- ✅ Professional folder structure
- ✅ requirements.txt (all dependencies)
- ✅ .gitignore and .env.example
- ✅ Markdown knowledge base (all 9 documents)
- ✅ AI system prompt with safety guardrails
- ✅ Architecture diagram
- ✅ Development roadmap
- ✅ UI/UX design guidelines

### Day 2 — Backend Core 🔜
**Objective:** Build the FastAPI application core and configuration layer.
- FastAPI application factory with lifespan management
- Configuration management (Pydantic Settings)
- Structured logging (Loguru)
- Custom exception handlers
- Health check endpoint
- CORS and security middleware
- Database connection pool (async SQLAlchemy)
- Alembic migration setup

### Day 3 — Retrieval Foundation ✅
**Objective:** Build the complete knowledge retrieval pipeline.
- ✅ Markdown document loader — discovers and reads all `.md` files from `knowledge-base/`
- ✅ Markdown cleaner — strips noise while preserving headings, lists, tables, paragraphs
- ✅ Heading-based text chunker — splits documents at heading boundaries with metadata
- ✅ Google Embedding-001 integration — generates dense vectors for documents and queries
- ✅ FAISS vector store — build, persist, load, and auto-rebuild on knowledge-base changes
- ✅ Semantic similarity retriever — returns top-k relevant chunks with cosine similarity scores
- ✅ Source attribution — every chunk retains filename, heading, subheading, chunk_id
- ✅ Index builder CLI (`python scripts/build_index.py` — supports `--mock` and `--force` flags)
- ✅ Pipeline testing with sample queries via the index builder script

### Day 4 — AI Chat Backend ✅
**Objective:** Implement the AI Chat Backend using the RAG pipeline.
- ✅ Chat endpoint (`POST /api/v1/chat`) — accepts `message` and optional `session_id`
- ✅ Gemini API integration — secure key loading from `.env`, never exposed in logs
- ✅ Complete RAG flow — retrieve → build context → prompt → Gemini → respond with sources
- ✅ Source attribution — every response includes source filename and heading
- ✅ Conversation memory — session-based in-memory history with configurable window
- ✅ Safety guardrails — injection detection, system query blocking, no diagnosis/medication
- ✅ Input validation — rejects empty/whitespace-only messages
- ✅ Error handling — missing API key, Gemini failures, retrieval failures, empty input
- ✅ Professional JSON error responses with error codes

### Day 5 — Frontend: Landing Page & Chatbot Widget ✅
**Objective:** Build a premium, responsive healthcare website and integrate the chatbot widget.
- ✅ Premium landing page with Hero, About, Services, Why Choose Us, Contact, Footer sections
- ✅ Semantic HTML5 structure with ARIA labels and accessibility best practices
- ✅ Responsive design (desktop / tablet / mobile) with CSS Grid and media queries
- ✅ Floating chatbot widget with open/close button, message bubbles, typing indicator, auto-scroll
- ✅ Backend integration via Fetch API to `POST /api/v1/chat`
- ✅ Suggested questions with one-click interaction
- ✅ Smooth CSS animations (fade-up, card hover lift, scroll reveal, chatbot spring animation)
- ✅ Error handling for server unavailable, network failure, and empty input
- ✅ Contact form with success feedback (frontend-only UI)

### Day 6 — Appointment System & Safety ✅
**Objective:** Implement the Appointment Request System and complete healthcare safety requirements.
- ✅ Appointment API (`POST /api/v1/appointments`) — accepts name, contact, date, time, service, reason
- ✅ Pydantic input validation — date must be today/future, time must be morning/afternoon/evening
- ✅ SQLAlchemy model (`appointments` table) with pending status tracking
- ✅ Repository layer — create, list, and retrieve appointment records
- ✅ Service layer — business logic with professional confirmation message
- ✅ Appointment confirmation — explicitly states REQUEST only, not a confirmed booking
- ✅ Emergency keyword detection — flags severe bleeding, facial trauma, breathing issues
- ✅ Healthcare safety guardrails — no diagnosis, no medication, no treatment guarantees
- ✅ System prompt updated — never guarantee outcomes, never confirm appointments

### Day 7 — Testing & Quality Assurance 🔜
**Objective:** Achieve comprehensive test coverage.
- Unit tests: RAG service, appointment service
- Integration tests: API endpoints
- Mock FAISS and Gemini for unit tests
- Pytest configuration
- Code coverage report (target: 80%+)
- Ruff linting and MyPy type checking
- Performance testing (response time benchmarks)

### Day 8 — Deployment & Documentation 🔜
**Objective:** Prepare for production deployment.
- Dockerfile (backend)
- Docker Compose (backend + PostgreSQL)
- Nginx configuration
- Environment-specific settings
- Full API documentation (OpenAPI/Swagger)
- Deployment guide
- Final README update
- Project presentation preparation

---

## Setup Instructions

> **Note:** These instructions will be expanded as development progresses. Currently only the project structure has been established (Day 1).

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.11+ |
| PostgreSQL | 15+ |
| Git | 2.x+ |

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/rashid-dental-ai-assistant.git
cd rashid-dental-ai-assistant
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env and fill in your credentials
```

### 5. Build the FAISS Vector Index

```bash
# Mock mode (offline, no API key needed)
python scripts/build_index.py --mock

# Live mode (requires GOOGLE_API_KEY in .env)
python scripts/build_index.py

# Force rebuild even if index is up-to-date
python scripts/build_index.py --force
```

### 6. Run the Application

```bash
uvicorn backend.app.main:app --reload
```

---

## Day 3 — Retrieval Pipeline

The knowledge retrieval pipeline is built as a set of independent, composable modules under `backend/app/rag/`. Each module has a single responsibility and can be used standalone or orchestrated together.

### Module Overview

| Module | File | Responsibility |
|--------|------|----------------|
| **Loader** | `backend/app/rag/loader.py` | Discovers and reads `.md` files from the knowledge-base directory. Returns `RawDocument` objects with content and file metadata. |
| **Cleaner** | `backend/app/rag/cleaner.py` | Removes HTML tags, image syntax, link URLs, code fences, and horizontal rules. Preserves headings, lists, tables, and paragraph structure. |
| **Chunker** | `backend/app/rag/chunker.py` | Splits cleaned documents at heading boundaries (H1–H6). Tracks heading hierarchy. Merges very short sections (<50 chars) into the previous chunk. |
| **Embedder** | `backend/app/rag/embedder.py` | Wraps Google's `models/embedding-001` API. Supports LIVE mode (real API with retry logic) and MOCK mode (deterministic random vectors for offline testing). Batch size: 50. |
| **Vector Store** | `backend/app/rag/vector_store.py` | Manages the FAISS `IndexFlatIP` lifecycle. Builds, persists (`.index` + `.pkl`), loads, and auto-rebuilds the index when knowledge-base files change. |
| **Retriever** | `backend/app/rag/retriever.py` | High-level semantic search. Embeds the query, searches FAISS, returns ranked results with source attribution metadata (filename, heading, subheading, chunk_id). |

### Data Flow

```
knowledge-base/*.md
       │
       ▼
  ┌──────────┐
  │  Loader  │  → RawDocument (filename, content, size, mtime)
  └────┬─────┘
       │
       ▼
  ┌──────────┐
  │ Cleaner  │  → Cleaned text (noise removed, structure preserved)
  └────┬─────┘
       │
       ▼
  ┌──────────┐
  │ Chunker  │  → DocumentChunk[] (chunk_id, heading, subheading, content, counts)
  └────┬─────┘
       │
       ▼
  ┌──────────┐
  │ Embedder │  → float[][] (768-dim vectors via Google Embedding-001)
  └────┬─────┘
       │
       ▼
  ┌──────────────┐
  │ Vector Store │  → FAISS IndexFlatIP (saved to backend/vector_store/)
  │  (FAISS)     │
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │  Retriever   │  → RetrievalResult[] (chunk + score + rank + attribution)
  └──────────────┘
         │
         ▼
  Ranked chunks (used by downstream RAG pipeline)
```

### Chunk Metadata

Each `DocumentChunk` includes:

| Field | Description |
|-------|-------------|
| `chunk_id` | Unique ID: `{filename_stem}_{index}_{uuid_short}` |
| `filename` | Source `.md` file basename (e.g. `services.md`) |
| `heading` | Top-level heading for this section |
| `subheading` | Nearest sub-heading (H2+) if applicable |
| `content` | Cleaned text content |
| `char_count` | Character count |
| `word_count` | Word count |
| `created_at` | UTC timestamp of chunk creation |
| `document_type` | Category derived from filename stem (e.g. `services`, `pricing`) |

### FAISS Index

- **Index type:** `IndexFlatIP` — exact inner-product search (equivalent to cosine similarity after L2 normalization)
- **Storage:** `backend/vector_store/faiss.index` (index) + `backend/vector_store/chunks.pkl` (chunk metadata)
- **Auto-rebuild:** The `VectorStore.auto_rebuild_if_stale()` method compares knowledge-base file modification times against the index timestamp. If any file is newer, the index is automatically rebuilt on next load.
- **CLI:** Use `python scripts/build_index.py` to manually build or rebuild the index

### Usage Example

```python
from backend.app.rag.retriever import RetrievalEngine

engine = RetrievalEngine.from_disk()
results = engine.retrieve("What are your clinic hours?", top_k=3)
for r in results:
    print(f"[{r.rank}] score={r.score:.4f} | {r.chunk.filename} → {r.chunk.heading}")
```

To build the index manually:

```bash
# Offline test with mock embeddings
python scripts/build_index.py --mock

# Production with Google API
python scripts/build_index.py
```

---

## Day 4 — AI Chat Backend

The AI Chat Backend enables conversational interaction with the RAG pipeline. It accepts user messages, retrieves relevant knowledge, sends a constructed prompt to Gemini, and returns the response with source attribution.

### Chat API

**Endpoint:** `POST /api/v1/chat`

**Request Format:**

```json
{
  "message": "What are your clinic hours?",
  "session_id": "optional-session-uuid"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | User's question (min 1 character) |
| `session_id` | string | No | For conversation continuity; auto-generated if omitted |

**Response Format:**

```json
{
  "message": "Our clinic is open Monday–Friday, 9:00 AM to 6:00 PM...",
  "session_id": "a1b2c3d4...",
  "sources": [
    {
      "filename": "timings-and-location.md",
      "heading": "Opening Hours",
      "chunk_id": "timings-and-location_0_a1b2c3d4"
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `message` | string | AI-generated response text |
| `session_id` | string | Session identifier for follow-up messages |
| `sources` | array | List of knowledge-base documents used for the answer |

### RAG Flow

```
User Message
     │
     ▼
Input Validation ─── Reject empty/whitespace-only messages
     │
     ▼
Prompt Injection Detection ─── Polite refusal if detected
     │
     ▼
System Query Detection ─── Refuse if asking about internal config
     │
     ▼
FAISS Retrieval ─── Semantic search over knowledge-base chunks
     │
     ▼
Context Assembly ─── Build context with source attribution
     │
     ▼
Prompt Construction ─── System prompt + context + history + query
     │
     ▼
Gemini Generation ─── Call Gemini LLM with assembled prompt
     │
     ▼
Response ─── AI answer + source list + session_id
```

### Architecture

| Component | File | Responsibility |
|-----------|------|----------------|
| **Chat Schema** | `backend/app/schemas/chat.py` | Pydantic models for request/response |
| **Chat Endpoint** | `backend/app/api/v1/endpoints/chat.py` | HTTP handler for `POST /api/v1/chat` |
| **RAG Pipeline** | `backend/app/services/rag/rag_pipeline.py` | Orchestrates retrieval → prompt → generation |
| **Gemini Client** | `backend/app/services/ai/gemini_client.py` | Wraps Google Generative AI SDK |
| **Conversation Memory** | `backend/app/services/ai/memory.py` | In-memory session-based history |

### Safety Guardrails

The chatbot enforces these rules at the application level:

- **Prompt injection detection** — keywords like `ignore previous instructions`, `you are now`, etc. trigger a polite refusal
- **System query detection** — asks about system prompt, API keys, or internal config are refused
- **No diagnosis** — the system prompt explicitly forbids diagnosing conditions
- **No medication** — the system prompt explicitly forbids recommending medications or dosages
- **Knowledge-grounded answers** — responses use only retrieved context; no invented clinic information
- **Emergency escalation** — the system prompt directs patients to call emergency services for life-threatening situations

### Error Responses

| Status | Error Code | Scenario |
|--------|------------|----------|
| 422 | `VALIDATION_ERROR` | Empty or whitespace-only message |
| 503 | `SERVICE_UNAVAILABLE` | RAG pipeline not initialized (missing API key or index) |
| 500 | `INTERNAL_ERROR` | Unexpected server or Gemini API failure |

---

## Day 5 — Frontend & Chatbot Widget

The frontend is a premium, responsive healthcare landing page with an integrated floating AI chatbot widget. It connects to the FastAPI backend via the `POST /api/v1/chat` endpoint.

### File Structure

```
frontend/
├── index.html                        # Main landing page
└── src/
    ├── styles/
    │   ├── variables.css             # CSS custom properties (colors, typography, spacing)
    │   ├── reset.css                 # CSS reset with reduced-motion support
    │   ├── main.css                  # Page styles (hero, services, contact, footer)
    │   └── chatbot.css               # Chatbot widget styles
    └── scripts/
        ├── main.js                   # Page interactions (nav scroll, mobile menu, scroll reveal, form)
        └── chatbot.js                # Chatbot widget logic (API calls, message rendering, error handling)
```

### Design System

| Token | Value | Usage |
|-------|-------|-------|
| Background | `hsl(60, 20%, 98%)` | Page background |
| Surface | `hsl(36, 22%, 95%)` | Card backgrounds |
| Accent | `hsl(180, 36%, 46%)` | CTAs, highlights |
| Accent Light | `hsl(180, 36%, 93%)` | Hover states |
| Text Primary | `hsl(0, 0%, 18%)` | Body text |
| Text Secondary | `hsl(0, 0%, 42%)` | Supporting text |
| Font | Inter (Google Fonts) | Clean, modern typography |

### Landing Page Sections

| Section | Description |
|---------|-------------|
| **Navigation** | Fixed glassmorphism nav with scroll shadow, mobile hamburger menu |
| **Hero** | Full-viewport hero with badge, headline, CTA buttons, dental illustration |
| **Trust Bar** | 3-column trust indicators (Expert Team, Modern Tech, Gentle Care) |
| **AI Assistant** | Feature highlights for the AI chatbot with visual illustration |
| **Services** | 6 service cards with hover lift animation |
| **Why Choose Us** | 6 feature cards with icons and descriptions |
| **Contact** | 2-column layout: contact details + inquiry form |
| **Footer** | 4-column footer with links, branding, copyright |

### Chatbot Widget

| Feature | Implementation |
|---------|---------------|
| **Trigger Button** | Fixed bottom-right, teal circle, pulse animation after 5s idle |
| **Chat Window** | 380×600px (desktop), 90vh full-width (mobile), spring open animation |
| **Message Bubbles** | User (teal right), Assistant (cream left) with source attribution |
| **Typing Indicator** | 3-dot bouncing animation during API calls |
| **Suggested Questions** | 4 clickable chips (services, hours, booking, location) |
| **Error Handling** | Inline error bar + fallback assistant message for network/server errors |
| **Restart Button** | Clears messages and session, shows welcome message |
| **Auto-scroll** | Scrolls to latest message on new content |

### API Integration

The chatbot communicates with the backend via the Fetch API:

```
POST /api/v1/chat
Content-Type: application/json

{
  "message": "What are your opening hours?",
  "session_id": null
}
```

Responses include `message` (AI text), `session_id` (for conversation continuity), and `sources` (array of source attributions).

### Animations

| Animation | Duration | Elements |
|-----------|----------|----------|
| Page entrance (fade-up) | 600ms | Hero content, hero visual |
| Scroll reveal (fade-up) | 600ms | Trust items, service cards, feature cards, sections |
| Card hover lift | 250ms | Service cards (translateY -4px + shadow) |
| Button hover | 150ms | All buttons (translateY -1px) |
| Chat window open | 300ms | Spring cubic-bezier open/close |
| Message appear | 200ms | New chat messages |
| Typing indicator | 1.2s | 3-dot bouncing animation |

All animations respect `prefers-reduced-motion`.

### Accessibility

- Semantic HTML5 elements (`<nav>`, `<section>`, `<footer>`, `<main>`)
- ARIA labels on navigation, chatbot, and interactive elements
- `aria-live="polite"` on chat message area for screen readers
- Keyboard-navigable chatbot (Enter to send)
- Proper color contrast ratios (WCAG 2.1 AA target)
- Responsive typography in `rem` units
- Focus indicators on all interactive elements

---

## Day 6 — Appointment System & Healthcare Safety

The Appointment Request System allows patients to submit appointment requests through a dedicated API. The chatbot guides patients through information collection, and the system stores requests in PostgreSQL for clinic staff review.

### Appointment API

**Endpoint:** `POST /api/v1/appointments`

**Request Format:**

```json
{
  "patient_name": "John Doe",
  "contact_number": "+1234567890",
  "preferred_date": "2026-07-20",
  "preferred_time": "morning",
  "requested_service": "General Checkup",
  "reason": "Routine dental checkup"
}
```

| Field | Type | Validation |
|-------|------|------------|
| `patient_name` | string | 1–200 characters |
| `contact_number` | string | 1–50 characters |
| `preferred_date` | date (ISO 8601) | Must be today or a future date |
| `preferred_time` | string | Must be `morning`, `afternoon`, or `evening` |
| `requested_service` | string | 1–200 characters |
| `reason` | string | 1–2000 characters |

**Response (201 Created):**

```json
{
  "id": 1,
  "patient_name": "John Doe",
  "contact_number": "+1234567890",
  "preferred_date": "2026-07-20",
  "preferred_time": "morning",
  "requested_service": "General Checkup",
  "reason": "Routine dental checkup",
  "status": "pending",
  "message": "Your appointment request has been received successfully. Please note that this is only a request and is not confirmed until Rashid Dental Clinic staff review and approve it. The clinic will contact you to confirm your appointment."
}
```

### Database Schema

| Column | Type | Notes |
|--------|------|-------|
| `id` | INTEGER | Primary key, auto-increment |
| `patient_name` | VARCHAR(200) | Patient's full name |
| `contact_number` | VARCHAR(50) | Contact phone number |
| `preferred_date` | DATE | Requested appointment date |
| `preferred_time` | VARCHAR(20) | Time slot (morning/afternoon/evening) |
| `requested_service` | VARCHAR(200) | Dental service requested |
| `reason` | TEXT | Reason for visit |
| `status` | VARCHAR(20) | Default: `pending` |
| `created_at` | TIMESTAMPTZ | Auto-generated timestamp |

### Architecture

| Layer | File | Responsibility |
|-------|------|----------------|
| **Model** | `backend/app/models/appointment.py` | SQLAlchemy ORM model |
| **Schema** | `backend/app/schemas/appointment.py` | Pydantic request/response validation |
| **Repository** | `backend/app/repositories/appointment.py` | Database CRUD operations |
| **Service** | `backend/app/services/appointment/service.py` | Business logic and confirmation messaging |
| **Endpoint** | `backend/app/api/v1/endpoints/appointments.py` | FastAPI route handler |

### Appointment Flow

```
Patient (via chatbot or API)
     │
     ▼
Chatbot collects: name, contact, date, time, service, reason
     │
     ▼
Patient confirms information
     │
     ▼
POST /api/v1/appointments
     │
     ▼
Input validation (Pydantic)
     │
     ▼
Store in PostgreSQL (status: pending)
     │
     ▼
Return confirmation with message:
"Request received — NOT a confirmed booking"
     │
     ▼
Clinic staff reviews and approves manually
```

### Healthcare Safety Guardrails

The system enforces the following safety rules:

| Rule | Description |
|------|-------------|
| **No automatic confirmation** | Every response explicitly states the appointment is a request, not a confirmed booking |
| **No diagnosis** | The chatbot never diagnoses dental or medical conditions |
| **No medication** | The chatbot never recommends medications, dosages, or prescriptions |
| **No treatment guarantees** | The chatbot never promises or estimates treatment outcomes |
| **No invented information** | All clinic answers come from the verified knowledge base only |
| **AI identity disclosure** | The assistant always identifies as an AI, not a dentist |
| **Emergency detection** | Keywords like "severe bleeding", "facial trauma", "difficulty breathing" trigger escalated responses |
| **Prompt injection resistance** | Attempts to override instructions are detected and blocked |
| **Input validation** | All API inputs are validated via Pydantic before processing |
| **SQL injection prevention** | All database operations use SQLAlchemy ORM (parameterized queries) |

### Emergency Handling

The system detects emergency keywords at the application level:

- **Keywords monitored:** severe bleeding, uncontrolled bleeding, facial trauma, broken jaw, swelling affecting breathing, difficulty breathing, trouble swallowing, knocked-out tooth, dental abscess
- **Action:** Emergency presence is logged, and the system prompt instructs the AI to escalate immediately
- **Response:** The AI will acknowledge the seriousness, direct patients to emergency services (911), provide basic first aid guidance from the verified knowledge base, and strongly encourage immediate professional care

---



## Security Notes

- **Never commit `.env`** — it contains secrets. It is listed in `.gitignore`.
- **Rotate compromised credentials** immediately if accidentally pushed.
- **The AI assistant will not reveal** system prompts, API keys, database structure, or internal configuration.
- **All user inputs are sanitized** to prevent prompt injection attacks.
- **Rate limiting is applied** to all endpoints to prevent abuse.
- **Medical guardrails are enforced** — the assistant will never give diagnoses or prescriptions.

---

## Contributing

This is a private internship project. Contribution guidelines will be added upon project completion.

---

## License

This project is developed as part of the DEVFORGE AI/ML Internship Program.

---

<div align="center">

*Built with ❤️ as part of DEVFORGE AI/ML Internship — Project 2*

</div>
