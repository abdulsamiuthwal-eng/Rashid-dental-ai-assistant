# Rashid Dental AI Assistant — Architecture Diagram

**Document Type:** Architecture Reference
**Version:** 1.0 | 2026-07-13

---

## Full System Architecture Diagram

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    RASHID DENTAL AI ASSISTANT — SYSTEM ARCHITECTURE         ║
╚══════════════════════════════════════════════════════════════════════════════╝

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                             USER / PATIENT                              │
  │                    (Browser — Desktop or Mobile)                        │
  └─────────────────────────────────┬───────────────────────────────────────┘
                                    │
                          HTTPS Requests
                                    │
  ┌─────────────────────────────────▼───────────────────────────────────────┐
  │                        NGINX REVERSE PROXY                              │
  │                   (TLS termination, static files)                       │
  └──────────────────────────┬──────────────────────┬───────────────────────┘
                             │                      │
                    API Requests              Static Assets
                    /api/v1/*                /frontend/*
                             │                      │
  ┌──────────────────────────▼──────────┐  ┌────────▼────────────────────────┐
  │          FRONTEND WEBSITE           │  │     BACKEND — FastAPI           │
  │                                     │  │                                  │
  │  ┌────────────────────────────────┐ │  │  ┌──────────────────────────┐   │
  │  │       Landing Page             │ │  │  │      API Layer (v1)      │   │
  │  │  • Hero Section                │ │  │  │  ┌────────────────────┐  │   │
  │  │  • Services Showcase           │ │  │  │  │  /chat  (POST)     │  │   │
  │  │  • Why Choose Us               │ │  │  │  │  /appointments     │  │   │
  │  │  • Team Section                │ │  │  │  │  /health   (GET)   │  │   │
  │  │  • Contact & Booking           │ │  │  │  └────────────────────┘  │   │
  │  └────────────────────────────────┘ │  │  │                          │   │
  │                                     │  │  │  Middleware:              │   │
  │  ┌────────────────────────────────┐ │  │  │  • CORS                  │   │
  │  │      Chatbot Widget            │ │◄─┼─►│  • Rate Limiting         │   │
  │  │  • Floating trigger button     │ │  │  │  • Request Logging       │   │
  │  │  • Chat window                 │ │  │  │  • Auth (JWT)            │   │
  │  │  • Message bubbles             │ │  │  │  • Error Handling        │   │
  │  │  • Appointment flow            │ │  │  └──────────────────────────┘   │
  │  └────────────────────────────────┘ │  │                                  │
  └─────────────────────────────────────┘  │  ┌──────────────────────────┐   │
                                           │  │     Service Layer         │   │
                                           │  │                          │   │
                                           │  │  ┌────────────────────┐  │   │
                                           │  │  │   RAG Service      │  │   │
                                           │  │  │                    │  │   │
                                           │  │  │  1. Query arrives  │  │   │
                                           │  │  │  2. Embed query    │  │   │
                                           │  │  │  3. Search FAISS   │  │   │
                                           │  │  │  4. Get top-k docs │  │   │
                                           │  │  │  5. Build prompt   │  │   │
                                           │  │  │  6. Call Gemini    │  │   │
                                           │  │  │  7. Return answer  │  │   │
                                           │  │  └────────────────────┘  │   │
                                           │  │                          │   │
                                           │  │  ┌────────────────────┐  │   │
                                           │  │  │  Memory Service    │  │   │
                                           │  │  │  (Conversation     │  │   │
                                           │  │  │   History Window)  │  │   │
                                           │  │  └────────────────────┘  │   │
                                           │  │                          │   │
                                           │  │  ┌────────────────────┐  │   │
                                           │  │  │ Appointment Service │  │   │
                                           │  │  │  • Data collection │  │   │
                                           │  │  │  • Validation      │  │   │
                                           │  │  │  • DB storage      │  │   │
                                           │  │  └────────────────────┘  │   │
                                           │  │                          │   │
                                           │  │  ┌────────────────────┐  │   │
                                           │  │  │   AI Service       │  │   │
                                           │  │  │  (Gemini Client)   │  │   │
                                           │  │  └────────────────────┘  │   │
                                           │  └──────────────────────────┘   │
                                           │                                  │
                                           │  ┌──────────────────────────┐   │
                                           │  │     Data Layer            │   │
                                           │  └──────────────────────────┘   │
                                           └──────────────┬───────────────────┘
                                                          │
                           ┌──────────────────────────────┼──────────────────────────────┐
                           │                              │                              │
              ┌────────────▼───────────┐    ┌────────────▼──────────┐   ┌──────────────▼──────┐
              │    KNOWLEDGE BASE      │    │   FAISS VECTOR STORE  │   │  POSTGRESQL DATABASE │
              │    (Markdown Files)    │    │   (Persisted Index)   │   │  (Appointments/Logs) │
              │                        │    │                       │   │                      │
              │  clinic-overview.md   │    │  ┌─────────────────┐  │   │  Tables:             │
              │  services.md          │───►│  │  Document       │  │   │  • appointments      │
              │  dentists.md          │    │  │  Embeddings     │  │   │  • conversations     │
              │  timings-location.md  │    │  │  (768-dim)      │  │   │  • chat_logs         │
              │  appointments.md      │    │  └─────────────────┘  │   │                      │
              │  pricing.md           │    │                       │   │                      │
              │  faq.md               │    │  ┌─────────────────┐  │   │                      │
              │  emergency-guidance.md│    │  │  FAISS Index    │  │   │                      │
              │  safety-policy.md     │    │  │  (L2/Cosine)    │  │   │                      │
              └────────────────────────┘    │  └─────────────────┘  │   └──────────────────────┘
                                           └───────────────────────┘

                           ┌──────────────────────────────────────────┐
                           │          GOOGLE GEMINI API               │
                           │       (External — via HTTPS)             │
                           │                                          │
                           │  • gemini-1.5-flash (Chat completions)   │
                           │  • embedding-001    (Text embeddings)    │
                           └──────────────────────────────────────────┘
```

---

## RAG Pipeline — Detailed Flow

```
USER QUERY: "What are your opening hours?"
                     │
                     ▼
           ┌─────────────────────┐
           │  Input Validation   │
           │  & Sanitisation     │
           │  (injection check)  │
           └──────────┬──────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │  Load Conversation  │
           │  History (Window)   │
           └──────────┬──────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │  Embed Query        │
           │  → Google           │
           │    Embedding-001    │
           │  → 768-dim vector   │
           └──────────┬──────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │  Search FAISS       │
           │  (cosine similarity)│
           │  → Top-K chunks     │
           └──────────┬──────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │  Filter by          │
           │  Similarity Score   │
           │  (threshold: 0.7)   │
           └──────────┬──────────┘
                      │
                      ▼
           ┌─────────────────────────────────────────────────┐
           │  Build Prompt                                    │
           │                                                 │
           │  [System Prompt]                                │
           │  [Conversation History]                         │
           │  [Retrieved Context]:                           │
           │    - timings-and-location.md#Opening-Hours      │
           │    - clinic-overview.md#Contact-Information     │
           │  [User Query]: "What are your opening hours?"   │
           └──────────────────────────────┬──────────────────┘
                                          │
                                          ▼
                              ┌──────────────────────┐
                              │   Google Gemini API  │
                              │   (gemini-1.5-flash) │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │   Generated Response │
                              │   + Source Citations │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │  Response Validation │
                              │  (safety check)      │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │  Save to Conversation│
                              │  History             │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │  Return to Frontend  │
                              │  (with sources)      │
                              └──────────────────────┘
```

---

## Appointment Request Flow

```
USER: "I'd like to book an appointment"
              │
              ▼
  ┌────────────────────────┐
  │  AI detects intent:    │
  │  APPOINTMENT REQUEST   │
  └────────────┬───────────┘
               │
               ▼
  ┌────────────────────────┐
  │  Collect information   │
  │  (conversational flow) │
  │                        │
  │  Step 1: Full name     │
  │  Step 2: Phone number  │
  │  Step 3: Email (opt.)  │
  │  Step 4: Preferred date│
  │  Step 5: Preferred time│
  │  Step 6: Visit reason  │
  │  Step 7: New/returning │
  └────────────┬───────────┘
               │
               ▼
  ┌────────────────────────┐
  │  Validate collected    │
  │  data (Pydantic)       │
  └────────────┬───────────┘
               │
               ▼
  ┌────────────────────────┐
  │  Save to PostgreSQL    │
  │  (appointments table)  │
  └────────────┬───────────┘
               │
               ▼
  ┌────────────────────────┐
  │  Confirm to user:      │
  │  "Request submitted.   │
  │   Clinic will contact  │
  │   you to confirm."     │
  └────────────────────────┘
```

---

## Module Dependency Map

```
backend/app/
│
├── main.py
│   └── imports: core/config, api/v1/router, core/logging
│
├── core/
│   ├── config.py          (no internal imports)
│   ├── logging.py         (imports: config)
│   ├── database.py        (imports: config)
│   ├── security.py        (imports: config)
│   ├── system_prompt.py   (no imports)
│   └── exceptions.py      (no imports)
│
├── api/v1/
│   ├── router.py          (imports: endpoints/*)
│   └── endpoints/
│       ├── health.py      (imports: core/config)
│       ├── chat.py        (imports: services/rag, services/ai, schemas/chat)
│       └── appointments.py(imports: services/appointment, schemas/appointment)
│
├── services/
│   ├── rag/
│   │   ├── document_loader.py (imports: core/config)
│   │   ├── chunker.py         (imports: core/config)
│   │   ├── embedder.py        (imports: core/config, services/ai)
│   │   ├── vector_store.py    (imports: core/config, services/rag/embedder)
│   │   ├── retriever.py       (imports: services/rag/vector_store)
│   │   └── rag_pipeline.py    (imports: all rag services, services/ai)
│   ├── ai/
│   │   ├── gemini_client.py   (imports: core/config, core/system_prompt)
│   │   └── memory_service.py  (imports: core/config)
│   └── appointment/
│       └── appointment_service.py (imports: repositories/appointment)
│
├── repositories/
│   └── appointment_repository.py  (imports: core/database, models/appointment)
│
├── models/
│   ├── appointment.py     (imports: core/database)
│   └── conversation.py    (imports: core/database)
│
└── schemas/
    ├── chat.py            (no internal imports — Pydantic only)
    └── appointment.py     (no internal imports — Pydantic only)
```

---

## Technology Decision Log

| Decision | Options Considered | Chosen | Rationale |
|----------|-------------------|--------|-----------|
| LLM Provider | OpenAI GPT, Anthropic Claude, Google Gemini | **Gemini** | Google ecosystem, free tier, multimodal capability |
| Vector Store | Pinecone, Chroma, Weaviate, FAISS | **FAISS** | No API cost, runs locally, sufficient scale |
| Database | MySQL, MongoDB, PostgreSQL | **PostgreSQL** | ACID, JSON support, best-in-class reliability |
| ORM | SQLAlchemy, Tortoise ORM, Databases | **SQLAlchemy 2.0** | Async support, mature, comprehensive |
| Framework | Django, Flask, FastAPI | **FastAPI** | Async, auto-docs, Pydantic, production-grade |
| Chunking | Fixed-size, Semantic, Heading-based | **Heading-based** | Preserves document structure, best for Markdown |
| Frontend | React, Vue, Vanilla | **Vanilla JS/HTML** | No build step, fast, sufficient for scope |

---

*Architecture v1.0 — 2026-07-13 | DEVFORGE Internship — Project 2*
