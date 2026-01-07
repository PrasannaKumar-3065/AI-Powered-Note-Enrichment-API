# 📝 Notes API - Python Backend Engineer Assessment

A production-ready, async REST API built with **FastAPI** and **PostgreSQL** that demonstrates clean architecture, external API integration, and robust error handling through an AI-powered notes management system.

---

## 🎯 Overview

This project implements a notes management system with automatic AI-powered summarization. When users create or update notes, the system generates intelligent summaries using external LLM providers (OpenAI/Gemini) with built-in fallback mechanisms for reliability.

### Key Features

- ✅ Full CRUD operations for notes management
- 🤖 Automatic AI summary generation using LLM providers
- 🔄 Resilient external API integration with fallback strategy
- 🗄️ PostgreSQL database with async SQLAlchemy
- ✨ Clean layered architecture (API → Service → Repository → DB)
- 🧪 Comprehensive test suite with pytest
- 📚 Auto-generated API documentation (Swagger/OpenAPI)
- 🛡️ Robust validation and error handling

---

## 🏗️ Architecture & Design

### System Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
┌──────▼──────────────────────────────────┐
│          FastAPI Application             │
├──────────────────────────────────────────┤
│  ┌────────────────────────────────────┐  │
│  │         API Layer (Routes)         │  │
│  └────────────┬───────────────────────┘  │
│               │                          │
│  ┌────────────▼───────────────────────┐  │
│  │      Service Layer (Logic)         │  │
│  │  ┌──────────────┐  ┌────────────┐  │  │
│  │  │ Note Service │  │  Summary   │  │  │
│  │  │              │  │  Service   │  │  │
│  │  └──────┬───────┘  └─────┬──────┘  │  │
│  └─────────┼────────────────┼─────────┘  │
│            │                │            │
│  ┌─────────▼────────┐  ┌────▼─────────┐  │
│  │   Repository     │  │  External    │  │
│  │     Layer        │  │  LLM APIs    │  │
│  └─────────┬────────┘  │ (OpenAI/     │  │
│            │           │  Gemini)     │  │
└────────────┼───────────└──────────────┘  │
             │                             │
┌────────────▼────────┐                    │
│   PostgreSQL DB     │                    │
└─────────────────────┘                    │
```

### Project Structure

```
app/
├── api/
│   ├── __init__.py
│   └── notes.py              # API route definitions
├── core/
│   ├── __init__.py
│   ├── config.py             # Configuration management
│   ├── database.py           # Database connection & session
│   └── exceptions.py         # Custom exception classes
├── models/
│   ├── __init__.py
│   └── note.py               # SQLAlchemy models
├── repositories/
│   ├── __init__.py
│   └── note_repository.py    # Data access layer
├── schemas/
│   ├── __init__.py
│   └── note.py               # Pydantic models (validation)
├── services/
│   ├── __init__.py
│   ├── note_service.py       # Business logic
│   └── summary_service.py    # External API integration
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Test fixtures
│   └── test_notes.py         # API integration tests
└── main.py                   # Application entry point
```

### Database Schema

```sql
CREATE TABLE notes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title           VARCHAR(255) NOT NULL,
    content         TEXT NOT NULL,
    ai_summary      TEXT,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP
);
```

**Design Decisions:**
- **UUIDs** for distributed-system-safe identifiers
- **Separate `ai_summary`** column for clear data lineage
- **Timestamps** for audit trail
- **Minimal schema** focusing on clarity and assessment requirements

---

## 🔄 Data Flow & API Operations

### Create Note Flow

```
1. Client → POST /notes {title, content}
2. FastAPI validates request (Pydantic)
3. SummaryService generates AI summary
   ├─ Try OpenAI API
   ├─ Fallback to Gemini API
   └─ Fallback to default message
4. NoteRepository saves to PostgreSQL
5. Return 201 Created with note + summary
```

### Update Note Flow

```
1. Client → PUT /notes/{id} {title, content}
2. Check note exists (404 if not)
3. Regenerate AI summary
4. Update database record
5. Return 200 OK with updated note
```

### Read & Delete Operations

- **GET /notes/{id}**: Retrieve single note (404 if not found)
- **GET /notes**: List all notes
- **DELETE /notes/{id}**: Remove note (204 No Content)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL 13+
- OpenAI API Key
- Google Gemini API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd notes-api
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/notes_db
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   MAX_TOKENS=1000
   ```

5. **Initialize the database**
   ```bash
   # Create database
   createdb notes_db
   
   # Tables will be created automatically on first run
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

---

## 📚 API Documentation

### Interactive Documentation

Once running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/notes` | Create a new note with AI summary |
| GET | `/notes` | List all notes |
| GET | `/notes/{id}` | Get a specific note by ID |
| PUT | `/notes/{id}` | Update a note (regenerates summary) |
| DELETE | `/notes/{id}` | Delete a note |

### Example Requests

#### Create Note
```bash
curl -X POST http://localhost:8000/notes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Meeting Notes",
    "content": "Discussed Q1 objectives and key performance indicators for the engineering team."
  }'
```

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Meeting Notes",
  "content": "Discussed Q1 objectives and key performance indicators for the engineering team.",
  "ai_summary": "Summary: Q1 engineering team goals and KPIs discussion.",
  "created_at": "2024-01-07T10:30:00",
  "updated_at": "2024-01-07T10:30:00"
}
```

#### Get Note
```bash
curl http://localhost:8000/notes/550e8400-e29b-41d4-a716-446655440000
```

#### Update Note
```bash
curl -X PUT http://localhost:8000/notes/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Meeting Notes",
    "content": "Revised Q1 objectives with focus on performance optimization."
  }'
```

#### Delete Note
```bash
curl -X DELETE http://localhost:8000/notes/550e8400-e29b-41d4-a716-446655440000
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest app/tests/test_notes.py -v
```

### Test Strategy

- **Integration Tests**: End-to-end API testing using HTTPX AsyncClient
- **Mocked External APIs**: AI services are mocked to avoid real API calls
- **Test Coverage**: CRUD operations, validation, error cases
- **CI-Ready**: No external dependencies in test suite

**Test Scenarios:**
- ✅ Create note with valid data
- ✅ Retrieve existing note
- ✅ Handle 404 for non-existent notes
- ✅ Update note content and summary
- ✅ Delete note successfully
- ✅ Validate request payload constraints

---

## 🛡️ Error Handling & Resilience

### Exception Handling Strategy

1. **Custom Domain Exceptions**: Centralized error types in `core/exceptions.py`
2. **Global Exception Handler**: FastAPI middleware for consistent error responses
3. **Validation Errors**: Automatic Pydantic validation with clear error messages
4. **External API Failures**: Graceful degradation with fallback mechanisms

### External API Resilience

```python
OpenAI (Primary)
    ↓ (on failure)
Google Gemini (Fallback)
    ↓ (on failure)
Default Message (Safe Fallback)
```

**Implemented Safeguards:**
- Token limit enforcement
- Timeout handling
- Logged failures for debugging
- User-friendly error messages
- No unhandled exceptions exposed to clients

---

## 🔒 Security & Best Practices

### Implemented

- ✅ Environment-based configuration (no hardcoded secrets)
- ✅ Input validation using Pydantic
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ UUID-based identifiers (non-sequential)
- ✅ Async/await for I/O operations
- ✅ Connection pooling for database

### Out of Scope (As Per Assessment)

- Authentication/Authorization
- Rate limiting
- CORS configuration (can be added easily)
- Production-grade logging (structured logs)

---

## 📋 Key Design Decisions

### Architecture Patterns

- **Layered Architecture**: Clear separation of concerns
- **Repository Pattern**: Abstract data access from business logic
- **Service Pattern**: Encapsulate business rules and external integrations
- **Dependency Injection**: FastAPI's built-in DI for testability