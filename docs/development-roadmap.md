# Rashid Dental AI Assistant — Development Roadmap

**Version:** 1.0
**Project:** DEVFORGE AI/ML Internship — Project 2
**Duration:** 8 Days
**Last Updated:** 2026-07-13

---

## Overview

This roadmap covers the complete development lifecycle of the Rashid Dental AI Assistant, from project foundation to deployment-ready system. Each day has defined objectives, deliverables, and expected outputs.

---

## Phase Summary

| Phase | Days | Focus |
|-------|------|-------|
| Foundation | Day 1 | Architecture, structure, knowledge base, planning |
| Backend Core | Day 2 | FastAPI application, config, middleware, DB setup |
| RAG Pipeline | Day 3 | Document loading, embeddings, FAISS, retrieval |
| Chat & Business Logic | Day 4 | Chat API, memory, appointments, security |
| Frontend — Structure | Day 5 | Website HTML, CSS design system, layout |
| Frontend — Chat Widget | Day 6 | Chatbot widget, API integration |
| Testing & QA | Day 7 | Unit tests, integration tests, linting, coverage |
| Deployment & Docs | Day 8 | Docker, Nginx, CI/CD, documentation, delivery |

---

## Day 1 — Project Foundation ✅

**Status:** Complete

### Objectives
- Establish a professional, scalable project foundation.
- Define architecture before writing any functional code.
- Create the knowledge base that will serve as the chatbot's source of truth.
- Prepare all configuration files.

### Deliverables
- [x] Clean Architecture design document
- [x] Professional folder structure (`backend/`, `frontend/`, `knowledge-base/`, etc.)
- [x] `requirements.txt` with all project dependencies
- [x] `.gitignore` — comprehensive, production-grade
- [x] `.env.example` — all variables with documentation
- [x] `README.md` — professional initial version
- [x] Architecture diagram (text-based and visual)
- [x] Markdown knowledge base — all 9 documents
- [x] AI system prompt with complete safety guardrails
- [x] UI/UX design planning document
- [x] Development roadmap (this document)

### Expected Output
A complete, navigable project structure with no functional code — only the foundation that all future phases will build upon.

---

## Day 2 — Backend Core 🔜

**Status:** Planned

### Objectives
- Build the FastAPI application core.
- Set up configuration management, logging, and database connectivity.
- Establish middleware and error handling patterns.

### Deliverables
- [ ] `backend/app/main.py` — complete FastAPI application factory with lifespan
- [ ] `backend/app/core/config.py` — Pydantic Settings configuration
- [ ] `backend/app/core/logging.py` — Loguru structured logging setup
- [ ] `backend/app/core/security.py` — JWT utilities
- [ ] `backend/app/core/database.py` — Async SQLAlchemy engine and session factory
- [ ] `backend/app/core/exceptions.py` — Custom exception classes
- [ ] `backend/app/api/v1/middleware/` — CORS, rate limiting, request logging
- [ ] `backend/app/api/v1/endpoints/health.py` — Health check endpoint
- [ ] `database/migrations/` — Alembic initialised
- [ ] Docker Compose stub — PostgreSQL service for local development
- [ ] Verification: `uvicorn backend.app.main:app --reload` runs without error
- [ ] Verification: `/health` endpoint returns 200 OK

### Expected Output
A running FastAPI server with working health check, database connection pool, and all middleware active.

---

## Day 3 — RAG Pipeline 🔜

**Status:** Planned

### Objectives
- Build the complete knowledge retrieval pipeline.
- Implement document loading, heading-based chunking, embeddings, and FAISS.

### Deliverables
- [ ] `backend/app/services/rag/document_loader.py` — Markdown file loader
- [ ] `backend/app/services/rag/chunker.py` — Heading-based text splitter
- [ ] `backend/app/services/rag/embedder.py` — Google Embedding-001 integration
- [ ] `backend/app/services/rag/vector_store.py` — FAISS build, persist, and load
- [ ] `backend/app/services/rag/retriever.py` — Semantic similarity retrieval
- [ ] `backend/app/services/rag/rag_pipeline.py` — Full RAG chain orchestration
- [ ] `backend/app/services/ai/gemini_client.py` — Gemini API client wrapper
- [ ] `scripts/build_index.py` — CLI script to (re)build FAISS index
- [ ] Unit tests for chunker and loader
- [ ] Verification: CLI script builds FAISS index from knowledge base
- [ ] Verification: Query returns relevant document chunks with source attribution

### Expected Output
A fully functional RAG pipeline that can retrieve relevant knowledge base chunks and generate grounded responses.

---

## Day 4 — Chat API & Business Logic 🔜

**Status:** Planned

### Objectives
- Implement the chat endpoint with conversation memory.
- Build the appointment request collection and storage system.
- Apply security — rate limiting, input sanitisation, injection detection.

### Deliverables
- [ ] `backend/app/schemas/chat.py` — ChatRequest and ChatResponse Pydantic schemas
- [ ] `backend/app/schemas/appointment.py` — AppointmentRequest schema
- [ ] `backend/app/models/appointment.py` — SQLAlchemy Appointment ORM model
- [ ] `backend/app/models/conversation.py` — Conversation log ORM model
- [ ] `database/migrations/versions/001_initial.py` — Initial Alembic migration
- [ ] `backend/app/repositories/appointment_repository.py` — CRUD operations
- [ ] `backend/app/services/appointment/appointment_service.py` — Business logic
- [ ] `backend/app/services/ai/memory_service.py` — Windowed conversation memory
- [ ] `backend/app/api/v1/endpoints/chat.py` — `POST /api/v1/chat` endpoint
- [ ] `backend/app/api/v1/endpoints/appointments.py` — `POST /api/v1/appointments`
- [ ] Input sanitisation and prompt injection detection
- [ ] Integration tests for chat and appointment endpoints
- [ ] Verification: Full conversation with memory across multiple turns
- [ ] Verification: Appointment data saved to PostgreSQL

### Expected Output
A complete, secure backend with working chat API (RAG + memory) and appointment collection.

---

## Day 5 — Frontend Structure & Design 🔜

**Status:** Planned

### Objectives
- Build the premium, responsive clinic website structure.
- Implement the design system (CSS custom properties, typography, spacing).
- Create all page sections in HTML.

### Deliverables
- [ ] `frontend/src/styles/variables.css` — Design system tokens (colors, fonts, spacing)
- [ ] `frontend/src/styles/reset.css` — CSS reset and base styles
- [ ] `frontend/src/styles/main.css` — Global styles
- [ ] `frontend/src/styles/components.css` — Component styles
- [ ] `frontend/public/index.html` — Complete HTML structure (semantic, accessible)
- [ ] Hero section — Premium headline, subheadline, CTA
- [ ] Services section — Service cards with icons
- [ ] "Why Choose Us" section — Trust indicators
- [ ] Team/Dentists section
- [ ] Contact section with clinic details
- [ ] Footer
- [ ] Responsive layout (mobile, tablet, desktop breakpoints)
- [ ] Google Fonts integration (Inter)
- [ ] Verification: Website renders correctly on all screen sizes

### Expected Output
A visually premium, fully responsive clinic website (static — no chatbot yet).

---

## Day 6 — Chatbot Widget & API Integration 🔜

**Status:** Planned

### Objectives
- Build the floating chatbot widget and integrate it with the backend API.
- Implement appointment collection flow within the chat.

### Deliverables
- [ ] `frontend/src/components/chatbot/widget.css` — Chat widget styles
- [ ] `frontend/src/components/chatbot/widget.js` — Widget toggle, open/close
- [ ] `frontend/src/components/chatbot/chat.js` — Message sending, receiving, rendering
- [ ] `frontend/src/components/chatbot/api.js` — Backend API integration (fetch)
- [ ] `frontend/src/scripts/main.js` — Application entry point
- [ ] Message Markdown rendering
- [ ] Loading state indicators
- [ ] Error handling (network errors, API errors)
- [ ] Session management (conversation ID)
- [ ] Appointment collection flow in chat UI
- [ ] Accessibility (ARIA labels, keyboard navigation, focus management)
- [ ] Verification: Complete end-to-end chat from browser to backend and back
- [ ] Verification: Appointment request submitted and saved to database

### Expected Output
A complete, working frontend — premium website with fully functional chatbot widget.

---

## Day 7 — Testing & Quality Assurance 🔜

**Status:** Planned

### Objectives
- Achieve comprehensive test coverage.
- Enforce code quality standards.
- Validate system behaviour with edge cases and adversarial inputs.

### Deliverables
- [ ] `tests/unit/services/test_rag_pipeline.py` — RAG service unit tests
- [ ] `tests/unit/services/test_appointment_service.py` — Appointment service tests
- [ ] `tests/unit/api/test_chat_endpoint.py` — Chat endpoint tests (mocked AI)
- [ ] `tests/unit/api/test_appointment_endpoint.py` — Appointment endpoint tests
- [ ] `tests/integration/test_chat_flow.py` — Full chat integration test
- [ ] `tests/integration/test_appointment_flow.py` — Appointment integration test
- [ ] `tests/fixtures/` — Shared test data and fixtures
- [ ] `pytest.ini` — Pytest configuration
- [ ] `.ruff.toml` — Ruff linting configuration
- [ ] `mypy.ini` — MyPy type checking configuration
- [ ] Code coverage report (target: ≥80%)
- [ ] Adversarial test cases (prompt injection, out-of-scope queries)
- [ ] Verification: All tests pass; linting and type checks pass

### Expected Output
A fully tested, linted, and type-safe codebase with ≥80% coverage.

---

## Day 8 — Deployment & Final Documentation 🔜

**Status:** Planned

### Objectives
- Package the application for production deployment.
- Write complete documentation.
- Prepare project for internship evaluation.

### Deliverables
- [ ] `deployment/docker/Dockerfile` — Backend Docker image
- [ ] `deployment/docker/docker-compose.yml` — Full stack (backend + PostgreSQL + Nginx)
- [ ] `deployment/nginx/nginx.conf` — Nginx reverse proxy configuration
- [ ] `deployment/scripts/deploy.sh` — Deployment automation script
- [ ] `.github/workflows/ci.yml` — GitHub Actions CI pipeline (lint + test)
- [ ] `docs/api/` — Complete OpenAPI documentation export
- [ ] `docs/deployment/deployment-guide.md` — Step-by-step deployment guide
- [ ] `docs/development/setup-guide.md` — Developer setup guide
- [ ] `README.md` — Final version (all features documented as completed)
- [ ] Environment-specific configuration validation
- [ ] Security hardening review (secrets, HTTPS, headers)
- [ ] Verification: Docker Compose brings up all services successfully
- [ ] Verification: End-to-end test against production-like environment

### Expected Output
A deployment-ready application with complete documentation, ready for professional evaluation.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Gemini API quota limits | Medium | Medium | Implement response caching; use gemini-1.5-flash |
| FAISS index size | Low | Low | Clinic knowledge base is small; not a concern |
| PostgreSQL connectivity | Low | High | Local Docker fallback; connection retry logic |
| Knowledge base gaps | High | Medium | Clearly marked placeholders; clinic to provide data |
| Frontend browser compatibility | Low | Medium | Test on Chrome, Firefox, Safari |

---

## Success Criteria

The project will be considered complete when:

1. ✅ All 8 days of deliverables are met.
2. ✅ The chatbot never fabricates clinic information.
3. ✅ The chatbot never provides a diagnosis or medication recommendation.
4. ✅ The system resists common prompt injection attempts.
5. ✅ Appointment requests are reliably stored in the database.
6. ✅ The website is responsive on mobile, tablet, and desktop.
7. ✅ Test coverage is ≥80%.
8. ✅ The application deploys cleanly with Docker Compose.
9. ✅ All documentation is complete and accurate.

---

*DEVFORGE AI/ML Internship — Project 2 | Rashid Dental AI Assistant*
*Roadmap Version 1.0 — 2026-07-13*
