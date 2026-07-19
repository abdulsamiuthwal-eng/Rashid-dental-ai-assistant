# Rashid Dental AI Assistant

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0--alpha-blue)
![Python](https://img.shields.io/badge/python-3.12+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688)
![License](https://img.shields.io/badge/license-MIT-yellow)
![Status](https://img.shields.io/badge/status-Deployed-success)

**An intelligent AI-powered dental assistant for Rashid Dental Clinic — built with RAG, Gemini, and FastAPI.**

*DEVFORGE AI/ML Internship — Project 2*

---

## Live Links

| Resource | URL |
|----------|-----|
| 🌐 **Live Website** | [https://rashid-dental-ai-assistant-3.onrender.com](https://rashid-dental-ai-assistant-3.onrender.com) |
| 📡 **Backend API** | [https://rashid-dental-ai-assistant-3.onrender.com/api/v1](https://rashid-dental-ai-assistant-3.onrender.com/api/v1) |
| 📊 **API Docs (Swagger)** | [https://rashid-dental-ai-assistant-3.onrender.com/docs](https://rashid-dental-ai-assistant-3.onrender.com/docs) |
| 📋 **API Docs (ReDoc)** | [https://rashid-dental-ai-assistant-3.onrender.com/redoc](https://rashid-dental-ai-assistant-3.onrender.com/redoc) |
| 💚 **Health Check** | [https://rashid-dental-ai-assistant-3.onrender.com/api/v1/health](https://rashid-dental-ai-assistant-3.onrender.com/api/v1/health) |
| 🐙 **GitHub Repository** | [https://github.com/abdulsamiuthwal-eng/Rashid-dental-ai-assistant](https://github.com/abdulsamiuthwal-eng/Rashid-dental-ai-assistant) |

</div>

---

## Project Objective

Build and deploy an AI chatbot for **Rashid Dental Clinic** that can be embedded into the clinic's website. The chatbot answers clinic-related questions using verified Markdown files, collects appointment requests, provides source-aware answers, and safely transfers users toward human assistance when required.

---

## Features

### Chatbot Capabilities
- ✅ Professional welcome with AI assistant identity
- ✅ Answer questions using verified Markdown knowledge base
- ✅ Provide clinic information (timings, location, services, pricing)
- ✅ Collect appointment requests via conversational flow
- ✅ Maintain conversation context within a session
- ✅ Display suggested questions for easy interaction
- ✅ Source attribution with every response
- ✅ Handle unavailable information safely (no hallucination)
- ✅ Refuse diagnosis/medication requests
- ✅ Recognize urgent warning signs & escalate

### Website Features
- ✅ Premium responsive clinic landing page
- ✅ Floating chatbot widget with open/close animation
- ✅ Services showcase, team section, contact form
- ✅ Mobile-first responsive design
- ✅ Accessibility (ARIA labels, keyboard nav, semantic HTML)

### Technical Features
- ✅ RAG pipeline (FAISS + Google Gemini)
- ✅ Markdown document loader with heading-based chunking
- ✅ FAISS vector store for semantic search
- ✅ Source-aware responses with citations
- ✅ Conversation session management
- ✅ Appointment database (PostgreSQL on Neon)
- ✅ Input validation, error handling, safety guardrails
- ✅ Rate limiting with SlowAPI

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | FastAPI 0.111 |
| **ASGI Server** | Uvicorn |
| **LLM** | Google Gemini 1.5 Flash |
| **Embeddings** | Google Embedding-001 |
| **Vector Store** | FAISS (CPU) |
| **Database** | PostgreSQL 15 (Neon) |
| **ORM** | SQLAlchemy 2.0 (async) |
| **Validation** | Pydantic v2 |
| **Frontend** | Vanilla JS/HTML/CSS |
| **Logging** | Loguru |
| **Rate Limiting** | SlowAPI |
| **Deployment** | Render + Neon |

---

## Architecture

```
User/Browser → FastAPI Backend → FAISS Search → Google Gemini → Response
                    ↕
            PostgreSQL (Neon)
```

The system uses **Retrieval-Augmented Generation (RAG)**:
1. User sends a question via the chatbot widget
2. Question is embedded using Google Embedding-001
3. FAISS index retrieves top-K relevant document chunks
4. Retrieved context + conversation history + system prompt is sent to Gemini
5. Gemini generates a sourced response → displayed in chatbot

---

## Project Structure

```
Rashid-Dental-AI-Assistant/
├── backend/
│   └── app/
│       ├── api/v1/endpoints/   # Route handlers (chat, appointments, health)
│       ├── core/               # Config, logging, database, security
│       ├── models/             # SQLAlchemy ORM models
│       ├── schemas/            # Pydantic schemas
│       ├── services/
│       │   ├── ai/             # Gemini client, memory service
│       │   ├── rag/            # RAG pipeline components
│       │   └── appointment/    # Appointment service
│       ├── repositories/       # Data access layer
│       └── rag/                # Loader, chunker, embedder, vector store
├── frontend/
│   ├── index.html              # Main landing page
│   └── src/                    # CSS, JS scripts (chatbot, main, enhancements)
├── knowledge-base/             # Markdown clinic information files
├── docs/                       # Documentation, architecture diagram
├── tests/                      # Unit and integration tests
├── scripts/                    # Build scripts (FAISS index builder)
├── database/                   # Alembic migrations
├── deployment/                 # Docker, Nginx configs
├── .env.example                # Environment variables template
├── render.yaml                 # Render deployment config
└── requirements.txt            # Python dependencies
```

---

## Knowledge Base

The chatbot answers are grounded in verified Markdown files:

| File | Content |
|------|---------|
| `clinic-overview.md` | Clinic introduction and contact |
| `services.md` | Dental services offered |
| `dentists.md` | Staff and dentist information |
| `timings-and-location.md` | Opening hours and address |
| `appointments.md` | Appointment booking process |
| `pricing.md` | Treatment costs |
| `frequently-asked-questions.md` | Common patient FAQs |
| `emergency-guidance.md` | Emergency care instructions |
| `chatbot-safety-policy.md` | AI safety guardrails |

---

## Safety Guardrails

- ❌ No medical diagnosis or prescriptions
- ❌ No medication recommendations
- ❌ No invented information — only answers from verified docs
- ⚠️ Detects emergency keywords and escalates to human contact
- 🛡️ Prompt injection detection
- 🔒 All API keys stored in environment variables (never in code)

---

## Local Setup

### Prerequisites
- Python 3.12+
- PostgreSQL (or use Neon cloud)
- Google Gemini API key ([get one free](https://aistudio.google.com/app/apikey))

### Installation

```bash
# Clone the repository
git clone https://github.com/abdulsamiuthwal-eng/Rashid-dental-ai-assistant.git
cd Rashid-dental-ai-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and database URL

# Build FAISS index
python scripts/build_index.py --mock

# Run the server
uvicorn backend.app.main:app --reload
```

Visit `http://127.0.0.1:8000` in your browser.

---

## Deployment

### Backend (Render)
The backend is deployed on Render's free tier:
- **Service Type:** Web Service
- **Build Command:** `pip install -r requirements.txt && python scripts/build_index.py --mock`
- **Start Command:** `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`

### Database (Neon)
PostgreSQL database hosted on [Neon](https://neon.tech) (free tier).

### Environment Variables (set in Render Dashboard)
| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | Neon PostgreSQL connection string |
| `GEMINI_API_KEY` | Google Gemini API key |
| `PYTHON_VERSION` | `3.12.0` |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/chat` | Send chat message |
| POST | `/api/v1/appointments` | Submit appointment request |
| GET | `/api/v1/appointments` | List appointments (auth) |

---

## Testing

```bash
pytest tests/ -v
```

Test report available at: [TEST_REPORT.md](TEST_REPORT.md)

---

## Evaluation Criteria Coverage

| Area | Status |
|------|--------|
| Chatbot functionality & conversation quality | ✅ |
| Markdown processing & knowledge retrieval | ✅ |
| Medical-safety guardrails | ✅ |
| FastAPI, database & appointment system | ✅ |
| Website integration & responsive interface | ✅ |
| Testing & prompt-injection handling | ✅ |
| Documentation & deployment | ✅ |

---

## Security

- ✅ All API keys in environment variables (`.env` / Render dashboard)
- ✅ `.env.example` provided — `.env` in `.gitignore`
- ✅ Input validation on all endpoints
- ✅ Rate limiting (SlowAPI)
- ✅ CORS configured
- ✅ Prompt injection detection
- ✅ No sensitive data in logs

---

## License

MIT — DEVFORGE Internship — Project 2

---

*Built with ❤️ by Abdul Sami | DEVFORGE AI/ML Internship 2026*
