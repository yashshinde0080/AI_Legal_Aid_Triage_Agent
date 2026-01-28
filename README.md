# AI LEGAL AID TRIGE AGENT

# 🏛️ AI Legal Aid Triage Agent

<!-- [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) -->
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-00a393.svg)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)](https://python.langchain.com/)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://react.dev/)

> **A stateful, agentic legal triage system with memory, guardrails, and auditability**

This is not a chatbot. This is a production-grade AI system that helps citizens understand legal procedures through intelligent questioning, classification, and verified document retrieval.

![System Architecture](https://via.placeholder.com/800x400.png?text=System+Architecture+Diagram)

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Architecture](#-architecture)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Agent System](#-agent-system)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Development](#-development)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Ethics & Safety](#-ethics--safety)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 Problem Statement

Most citizens fail before legal action even begins because:

- **Lack of Domain Knowledge**: They don't know which legal domain applies to their situation
- **Authority Confusion**: They don't know the correct authority to approach
- **Cost Barriers**: Lawyers are expensive just to explain basic procedures
- **Information Asymmetry**: Legal language is inaccessible to common citizens

### Impact

- Dropped cases due to procedural errors
- Exploitation of uninformed citizens
- Delayed justice
- Overburdened legal aid systems

**This is an access-to-justice problem, not an AI demo problem.**

---

## 💡 Solution

A **stateful AI agent system** that:

1. ✅ Maintains conversation memory (ChatGPT-like experience)
2. ✅ Actively asks clarifying questions through autonomous loops
3. ✅ Classifies legal issues with confidence thresholds
4. ✅ Retrieves procedures from verified legal documents (RAG)
5. ✅ Enforces strict safety guardrails
6. ✅ Logs every step for auditability and transparency

### Key Differentiators

- **Agentic**: True autonomous reasoning loops, not predetermined flows
- **Stateful**: Persistent memory across sessions
- **Grounded**: All responses backed by verified legal documents
- **Safe**: Multi-layer guardrails prevent legal advice
- **Auditable**: Complete logging for compliance and improvement

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Vite + React)                  │
│                     shadcn/ui + TailwindCSS                 │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS/WSS
┌────────────────────────▼────────────────────────────────────┐
│                    FastAPI Backend                          │
│              JWT Auth + Request Validation                  │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│              LangGraph Agent Orchestrator                   │
│                  (State Machine Loop)                       │
├─────────────────────────────────────────────────────────────┤
│  Intake → Classifier → Clarification → RAG → Response       │
│              ↓                ↑                             │
│         Safety Validator ─────┘                             │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
┌───────▼────────┐              ┌────────▼─────────┐
│   Supabase     │              │   LLM Provider   │
├────────────────┤              ├──────────────────┤
│ • Auth (JWT)   │              │ • OpenAI API     │
│ • PostgreSQL   │              │ • OpenRouter     │
│ • pgvector     │              │ • Gemini         │
│ • Storage      │              └──────────────────┘
└────────────────┘
```

### Architecture Principles

- **Separation of Concerns**: Clear boundaries between agents, tools, and data
- **Fail-Safe Design**: Guardrails at every output point
- **Observability**: Comprehensive logging and metrics
- **Scalability**: Stateless API design with external state management

---

## ✨ Features

### Core Capabilities

- 🔄 **Autonomous Agent Loops**: Self-directed questioning until sufficient information is gathered
- 🧠 **Persistent Memory**: ChatGPT-style conversation threads that persist across sessions
- 🎯 **Intelligent Classification**: Multi-level legal issue classification with confidence scoring
- 📚 **RAG-Powered Responses**: All guidance backed by verified legal documents
- 🛡️ **Multi-Layer Safety**: Prevents legal advice, predictions, and harmful outputs
- 📊 **Full Auditability**: Every agent decision and state transition is logged

### User Experience

- 💬 **Natural Conversation**: Friendly, accessible language
- 🔍 **Smart Clarification**: Targeted questions, never open-ended confusion
- 📖 **Source Citations**: Every response includes relevant act and section references
- 📱 **Mobile-First UI**: Responsive design built with shadcn/ui
- 🔐 **Secure Authentication**: Supabase Auth with JWT tokens

### Technical Features

- ⚡ **Real-Time Typing Indicators**: WebSocket support for live updates
- 💾 **Session Management**: Create, resume, and manage conversation threads
- 🔄 **Context Retention**: Automatic conversation summarization for long threads
- 📈 **Performance Monitoring**: Latency tracking and error reporting
- 🌍 **Multi-Language Support**: Extensible i18n framework (planned)

---

## 🛠️ Technology Stack

### Backend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | FastAPI | High-performance async API |
| **Agent Framework** | LangChain + LangGraph | Agent orchestration and state management |
| **LLM Provider** | OpenAI / OpenRouter / Gemini | Natural language processing |
| **Vector Database** | Supabase pgvector | Semantic search over legal documents |
| **Database** | PostgreSQL (Supabase) | Session and conversation storage |
| **Authentication** | Supabase Auth | JWT-based user authentication |
| **Language** | Python 3.11+ | Core application logic |

### Frontend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | React 18 + Vite | Modern, fast frontend |
| **UI Library** | shadcn/ui | Accessible, customizable components |
| **Styling** | TailwindCSS | Utility-first styling |
| **State Management** | React Hooks + Context | Local state management |
| **API Client** | Supabase JS | Backend communication |
| **Type Safety** | TypeScript | Static type checking |

### Infrastructure

- **Hosting**: Vercel (Frontend) + Railway/Render (Backend)
- **Database**: Supabase Cloud
- **Monitoring**: Sentry (Error tracking)
- **CI/CD**: GitHub Actions

---

## 🤖 Agent System

### Agent Lineup

This system uses **7 specialized agents**, each with a specific responsibility:

#### 1. 🧠 Legal Triage Orchestrator
**Type**: LangGraph State Machine  
**Role**: Central coordinator that manages agent flow and state transitions

```python
# Controls routing decisions
"classify" → "clarify" → "retrieve" → "respond" → "validate"
```

#### 2. 🧾 Intake & Context Agent
**Purpose**: Normalize input and attach memory context  
**Key Functions**:
- Clean and structure user input
- Load relevant conversation history
- Detect follow-up vs. new issue

#### 3. 🧭 Legal Issue Classifier Agent
**Purpose**: Categorize legal issues with confidence scoring  
**Output Example**:
```json
{
  "domain": "Consumer Law",
  "sub_domain": "Defective Product",
  "confidence": 0.78,
  "missing_fields": ["purchase_date", "seller_type"]
}
```

#### 4. ❓ Clarification Question Agent
**Purpose**: Ask targeted follow-up questions  
**Behavior**:
- One question at a time
- Loops until confidence ≥ 0.7
- Never asks open-ended questions

#### 5. 📚 Legal Retrieval Agent (RAG)
**Purpose**: Fetch verified legal procedures  
**Sources**:
- IPC/CrPC bare acts
- Consumer Protection Act
- Labour laws
- Government portals
- Legal Services Authority FAQs

#### 6. ✍️ Procedural Response Agent
**Purpose**: Generate user-facing guidance  
**Constraints**:
- Procedural language only
- Must cite sources
- Never runs without retrieved documents

#### 7. 🚨 Safety Validator Agent
**Purpose**: Final safety checkpoint  
**Checks**:
- Detects legal advice language
- Blocks predictions
- Enforces ethical guidelines
- Triggers refusal when necessary

### Agent State Schema

```python
class LegalAgentState(TypedDict):
    user_input: str
    chat_history: list
    classification: dict | None
    confidence: float
    retrieved_docs: list
    response: str
    needs_clarification: bool
    session_id: str
    user_id: str
```

---

## 📁 Project Structure

### Backend Structure

```
backend/
├── app/
│   ├── main.py                      # FastAPI application entry
│   ├── config.py                    # Environment configuration
│   │
│   ├── api/                         # API endpoints
│   │   ├── auth.py                  # Authentication routes
│   │   ├── chat.py                  # Chat endpoints
│   │   └── health.py                # Health check
│   │
│   ├── agent/                       # Core agent logic
│   │   ├── state.py                 # LangGraph state schema
│   │   ├── graph.py                 # LangGraph wiring
│   │   ├── nodes.py                 # Agent node implementations
│   │   ├── tools.py                 # LangChain tools
│   │   └── prompts.py               # System prompts
│   │
│   ├── agents/                      # Individual agent modules
│   │   ├── intake_agent.py
│   │   ├── classifier_agent.py
│   │   ├── clarification_agent.py
│   │   ├── retriever_agent.py
│   │   ├── response_agent.py
│   │   ├── safety_agent.py
│   │   └── memory_agent.py
│   │
│   ├── memory/                      # Memory management
│   │   ├── short_term.py            # ConversationBufferMemory
│   │   ├── long_term.py             # Supabase persistence
│   │   └── summarizer.py            # Context summarization
│   │
│   ├── rag/                         # RAG pipeline
│   │   ├── loader.py                # Document ingestion
│   │   ├── chunker.py               # Text chunking
│   │   ├── embedder.py              # Embedding generation
│   │   └── retriever.py             # Vector search
│   │
│   ├── db/                          # Database layer
│   │   ├── supabase.py              # Supabase client
│   │   ├── models.py                # Data models
│   │   └── vector.py                # Vector operations
│   │
│   └── utils/                       # Utilities
│       ├── guardrails.py            # Safety checks
│       ├── logger.py                # Logging setup
│       └── confidence.py            # Confidence scoring
│
├── scripts/                         # Utility scripts
│   ├── ingest_documents.py          # Document ingestion
│   ├── build_embeddings.py          # Embedding generation
│   └── summarize_sessions.py        # Session summarization
│
├── tests/                           # Test suite
│   ├── test_agents.py
│   ├── test_api.py
│   └── test_rag.py
│
├── requirements.txt                 # Python dependencies
└── README.md
```

### Frontend Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── chat/                    # Chat components
│   │   │   ├── ChatWindow.tsx
│   │   │   ├── ChatBubble.tsx
│   │   │   ├── MessageInput.tsx
│   │   │   └── TypingIndicator.tsx
│   │   │
│   │   ├── sidebar/                 # Sidebar components
│   │   │   ├── SessionList.tsx
│   │   │   └── NewChatButton.tsx
│   │   │
│   │   └── ui/                      # shadcn components
│   │       ├── button.tsx
│   │       ├── card.tsx
│   │       └── ...
│   │
│   ├── pages/                       # Page components
│   │   ├── Login.tsx
│   │   └── Chat.tsx
│   │
│   ├── lib/                         # Utility libraries
│   │   ├── supabase.ts              # Supabase client
│   │   ├── api.ts                   # API client
│   │   └── types.ts                 # TypeScript types
│   │
│   ├── hooks/                       # Custom React hooks
│   │   ├── useChat.ts               # Chat management
│   │   ├── useSession.ts            # Session management
│   │   └── useAuth.ts               # Authentication
│   │
│   ├── App.tsx                      # Root component
│   └── main.tsx                     # Entry point
│
├── public/                          # Static assets
├── index.html
├── tailwind.config.ts               # Tailwind configuration
├── components.json                  # shadcn configuration
├── tsconfig.json                    # TypeScript configuration
└── package.json
```

---

## 🚀 Installation

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL** (via Supabase)
- **OpenAI API Key** (or OpenRouter/Gemini)

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-legal-aid-triage.git
cd ai-legal-aid-triage/backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Initialize database**
```bash
python scripts/init_db.py
```

6. **Ingest legal documents**
```bash
python scripts/ingest_documents.py
```

7. **Run the server**
```bash
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd ../frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Set up environment variables**
```bash
cp .env.example .env.local
# Edit .env.local with your Supabase credentials
```

4. **Run development server**
```bash
npm run dev
```

5. **Access the application**
```
http://localhost:5173
```

---

## ⚙️ Configuration

### Environment Variables

#### Backend (.env)

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_service_key

# LLM Provider
OPENAI_API_KEY=your_openai_key
# OR
OPENROUTER_API_KEY=your_openrouter_key
# OR
GOOGLE_API_KEY=your_gemini_key

# LangChain
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langchain_key
LANGCHAIN_PROJECT=legal-aid-triage

# Agent Configuration
CONFIDENCE_THRESHOLD=0.7
MAX_CLARIFICATION_LOOPS=3
RETRIEVAL_TOP_K=5

# Embeddings
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSION=1536

# Safety
ENABLE_GUARDRAILS=true
LOG_ALL_REQUESTS=true
```

#### Frontend (.env.local)

```bash
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
VITE_API_BASE_URL=http://localhost:8000
```

### Database Schema

#### chat_sessions

```sql
CREATE TABLE chat_sessions (
    session_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id),
    title TEXT,
    summary TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    last_updated TIMESTAMP DEFAULT NOW()
);
```

#### chat_messages

```sql
CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    session_id UUID NOT NULL REFERENCES chat_sessions(session_id),
    role TEXT NOT NULL CHECK (role IN ('user', 'agent')),
    content TEXT NOT NULL,
    metadata JSONB,
    timestamp TIMESTAMP DEFAULT NOW()
);
```

#### legal_chunks

```sql
CREATE TABLE legal_chunks (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(1536),
    metadata JSONB,
    act TEXT,
    section TEXT,
    source_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX ON legal_chunks USING ivfflat (embedding vector_cosine_ops);
```

#### agent_logs

```sql
CREATE TABLE agent_logs (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(session_id),
    agent_name TEXT NOT NULL,
    input_state JSONB,
    output_state JSONB,
    confidence FLOAT,
    timestamp TIMESTAMP DEFAULT NOW()
);
```

---

## 📖 Usage

### Basic Workflow

1. **User Login**: Authenticate via Supabase Auth
2. **Start Conversation**: Create new chat session or resume existing one
3. **Describe Issue**: User describes their legal situation in natural language
4. **Agent Interaction**: System asks clarifying questions if needed
5. **Receive Guidance**: System provides procedural steps with legal citations
6. **Follow Up**: Continue conversation with follow-up questions

### Example Interaction

```
User: "A shopkeeper sold me a defective phone and refuses to refund"

Agent: "I understand you purchased a defective phone. To help you better, 
       could you tell me:
       1. When did you purchase the phone?
       2. Do you have the receipt or bill?"

User: "I bought it 2 weeks ago and I have the bill"

Agent: "Based on your situation, this falls under Consumer Protection law. 
       Here's what you can do:
       
       Step 1: Send a written complaint to the shopkeeper citing the 
               Consumer Protection Act, 2019, Section 18 (right to be heard).
       
       Step 2: If no response within 30 days, file a complaint with the 
               District Consumer Forum.
       
       Step 3: You'll need:
               • Copy of the bill
               • Written complaint describing the defect
               • Any correspondence with the seller
       
       Would you like details on how to file with the Consumer Forum?"
```

### API Examples

#### Create Chat Session

```bash
curl -X POST http://localhost:8000/api/chat/sessions \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

#### Send Message

```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "uuid-here",
    "message": "I have a consumer complaint"
  }'
```

#### Get Session History

```bash
curl -X GET http://localhost:8000/api/chat/sessions/uuid-here \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 🧪 Development

### Running Tests

#### Backend Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

#### Frontend Tests

```bash
cd frontend
npm run test
```

### Code Quality

```bash
# Backend linting
cd backend
ruff check .
black --check .
mypy app/

# Frontend linting
cd frontend
npm run lint
npm run type-check
```

### Pre-commit Hooks

```bash
pre-commit install
pre-commit run --all-files
```

---

## 🧪 Testing

### Test Coverage Goals

- **Unit Tests**: 80%+ coverage
- **Integration Tests**: Critical paths
- **E2E Tests**: Core user flows

### Test Categories

#### Agent Tests
- Classification accuracy
- Clarification logic
- RAG retrieval quality
- Safety guardrails

#### API Tests
- Authentication flows
- Session management
- Error handling
- Rate limiting

#### Frontend Tests
- Component rendering
- User interactions
- State management
- Error boundaries

---

## 🚢 Deployment

### Backend Deployment (Railway/Render)

1. **Connect GitHub repository**
2. **Set environment variables**
3. **Deploy**

```bash
# Using Railway CLI
railway up
```

### Frontend Deployment (Vercel)

1. **Connect GitHub repository**
2. **Configure build settings**:
   - Build Command: `npm run build`
   - Output Directory: `dist`
3. **Set environment variables**
4. **Deploy**

### Database Deployment

- Use **Supabase Cloud** for managed PostgreSQL + pgvector
- Enable Row Level Security (RLS) policies
- Set up automated backups

### Monitoring

- **Backend**: Sentry for error tracking
- **Frontend**: Vercel Analytics
- **Database**: Supabase Dashboard
- **Logs**: CloudWatch or equivalent

---

## 🛡️ Ethics & Safety

### Core Principles

1. **No Legal Advice**: System provides procedural guidance only
2. **No Predictions**: Never predicts case outcomes
3. **No Lawyer Recommendations**: Does not recommend specific lawyers
4. **Clear Disclaimers**: Every response includes appropriate disclaimers
5. **Human Escalation**: Encourages consulting qualified legal professionals

### Safety Mechanisms

#### Input Safety
- Detects sensitive personal information
- Filters inappropriate content
- Rate limiting to prevent abuse

#### Output Safety
- Multi-layer guardrail checks
- Blocklist for advice language
- Confidence-based refusal
- Mandatory source citations

#### Audit Trail
- All agent decisions logged
- Classification confidence tracked
- Response sources recorded
- User actions timestamped

### Compliance

- **Data Privacy**: GDPR and local data protection laws
- **Accessibility**: WCAG 2.1 AA compliance
- **Transparency**: Open-source guardrails
- **Accountability**: Complete audit logs

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow existing code style
- Write tests for new features
- Update documentation
- Keep commits atomic and well-described

### Areas for Contribution

- 🌍 **Multi-language support**
- 📚 **Additional legal domains**
- 🔍 **Improved classification models**
- 🎨 **UI/UX enhancements**
- 📊 **Analytics and metrics**
- 🧪 **Test coverage**

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **LangChain & LangGraph**: For the agent framework
- **Supabase**: For the backend infrastructure
- **shadcn/ui**: For the beautiful UI components
- **Legal Services Authorities**: For verified legal documents
- **Open Source Community**: For the tools that made this possible

---

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-legal-aid-triage/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-legal-aid-triage/discussions)
- **Email**: support@legalaidai.com
- **Documentation**: [Full Documentation](https://docs.legalaidai.com)

---

## 🗺️ Roadmap

### Phase 1 (Current)
- ✅ Core agent system
- ✅ RAG implementation
- ✅ Basic UI
- ✅ Authentication

### Phase 2 (Q2 2026)
- 🔄 Multi-language support
- 🔄 Mobile applications
- 🔄 Voice interface
- 🔄 Advanced analytics

### Phase 3 (Q3 2026)
- 📋 Integration with legal aid organizations
- 📋 Government portal integration
- 📋 Case tracking features
- 📋 Document generation

### Phase 4 (Q4 2026)
- 🎯 AI model fine-tuning
- 🎯 Regional customization
- 🎯 Enterprise features
- 🎯 API marketplace

---

## ⚠️ Disclaimer

This system provides **procedural guidance only** and does not constitute legal advice. Users should consult qualified legal professionals for advice specific to their situation. The developers and contributors are not liable for any decisions made based on information provided by this system.

---

**Built with ❤️ for access to justice**

*If you find this project useful, please consider giving it a ⭐ on GitHub!*