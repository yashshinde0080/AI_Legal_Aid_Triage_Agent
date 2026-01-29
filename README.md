# ⚖️ AI Legal Aid Triage Agent

![Project Status](https://img.shields.io/badge/Status-Active_Development-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white&style=for-the-badge)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0%2B-3178C6?logo=typescript&logoColor=white&style=for-the-badge)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black&style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-009688?logo=fastapi&logoColor=white&style=for-the-badge)

> **Empowering Legal Aid with Intelligent Automation.**
>
> An advanced, AI-powered system designed to streamline the intake and triage process for legal aid organizations. Leveraging Large Language Models (LLMs) and a modern web stack, this agent helps categorize legal issues, extract critical information from documents, and prioritize cases efficiently.

---

## 📑 Table of Contents

- [✨ Features](#-features)
- [🏗️ Architecture](#-architecture)
- [🛠️ Tech Stack](#-tech-stack)
- [🚀 Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [🔑 Environment Variables](#-environment-variables)
- [🖼️ Screenshots](#-screenshots)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

- **🤖 Intelligent Triage**: Automatically categorizes legal inquiries using advanced LLMs (Gemini, OpenAI, etc.).
- **📄 Document Analysis**: Extracts key entities and summaries from PDFs and DOCX files.
- **💬 Interactive Chat Interface**:  Guided conversation flow to gather missing case details.
- **⚡ Real-time Updates**: Instant feedback and status tracking for submitted cases.
- **🔒 Secure Authentication**: Robust user management via Supabase Auth.
- **📊 Admin Dashboard**: Comprehensive view for legal professionals to review and manage cases.

---

## 🏗️ Architecture

The system follows a modern client-server architecture:

```mermaid
graph TD
    User[End User] -->|Browsers| FE[Frontend (React/Vite)]
    FE -->|API Requests| BE[Backend (FastAPI)]
    FE -->|Auth & Data| DB[(Supabase DB & Auth)]
    
    subgraph Backend Services
        BE -->|Orchestration| LG[LangChain / LangGraph]
        LG -->|Inference| LLM[LLM Providers (Google/OpenAI)]
        LG -->|Vector Search| Vec[Vector Store]
    end
    
    BE -->|Store/Retrieve| DB
```

---

## � Project Structure

```
AI_Legal_Aid_Triage_Agent/
├── backend/            # FastAPI Server & AI Logic
├── frontend/           # React Dashboard Application
├── landing_page/       # Marketing Landing Page
├── scripts/            # Utility scripts
└── README.md           # Project Documentation
```

---

## �🛠️ Tech Stack

### **Frontend**
- **Framework**: [React](https://react.dev/) + [Vite](https://vitejs.dev/)
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **Styling**: [Tailwind CSS v4](https://tailwindcss.com/) + [Radix UI](https://www.radix-ui.com/)
- **Icons**: [Lucide React](https://lucide.dev/)
- **State/Data**: Supabase Client

### **Backend**
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **AI Orchestration**: [LangChain](https://www.langchain.com/) + [LangGraph](https://langchain-ai.github.io/langgraph/)
- **Package Manager**: [uv](https://github.com/astral-sh/uv) (Blazing fast Python package installer)
- **Validation**: [Pydantic](https://docs.pydantic.dev/)
- **Testing**: Pytest

### **Infrastructure & AI**
- **Database & Auth**: [Supabase](https://supabase.com/)
- **LLMs**: Google Gemini, OpenAI GPT-4, or OpenRouter
- **Embeddings**: HuggingFace / Sentence Transformers

---

## 🚀 Getting Started

Follow these steps to set up the project locally.

### Prerequisites

- **Node.js** (v18+)
- **Python** (v3.10+)
- **Supabase Account** (for database and auth)

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment and install dependencies:**
   We recommend using `uv` for speed, but standard `pip` works too.
   ```bash
   # Using pip
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   Copy the example environment file and fill in your keys.
   ```bash
   cp .env.example .env
   ```
   *See [Environment Variables](#-environment-variables) for details.*

4. **Initialize System:**
   Run the setup scripts to prepare the database and knowledge base.
   ```bash
   # Setup Database Schema
   python scripts/setup_database.py
   
   # Ingest Legal Documents
   python scripts/ingest_documents.py
   ```

5. **Run the Server:**
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure Environment:**
   ```bash
   cp .env.example .env
   ```

4. **Start the Development Server:**
   ```bash
   npm run dev
   ```
   The app will run at `http://localhost:5173`.

---

## 🔑 Environment Variables

### Backend (`backend/.env`)

| Variable | Description |
|----------|-------------|
| `APP_NAME` | Name of the application |
| `SUPABASE_URL` | Your Supabase Project URL |
| `SUPABASE_KEY` | Supabase Anon Key |
| `SUPABASE_SERVICE_KEY` | Supabase Service Role Key |
| `LLM_PROVIDER` | Selected provider (e.g., `gemini`, `openai`) |
| `GOOGLE_API_KEY` | API Key for Google Gemini |
| `OPENAI_API_KEY` | API Key for OpenAI |
| `JWT_SECRET` | Secret key for JWT signing |

### Frontend (`frontend/.env`)

| Variable | Description |
|----------|-------------|
| `VITE_SUPABASE_URL` | Your Supabase Project URL |
| `VITE_SUPABASE_ANON_KEY` | Supabase Anon Key |
| `VITE_API_URL` | Backend API URL (default: `http://localhost:8000`) |

---

## 🖼️ Screenshots

<div align="center">
  <img src="https://placehold.co/800x450/EEE/31343C?font=montserrat&text=Dashboard+Preview" alt="Dashboard" width="800" />
  <br/><br/>
  <div style="display: flex; justify-content: center; gap: 20px;">
    <img src="https://placehold.co/380x250/EEE/31343C?font=montserrat&text=Triage+Interface" alt="Triage" width="380" />
    <img src="https://placehold.co/380x250/EEE/31343C?font=montserrat&text=Case+Management" alt="Cases" width="380" />
  </div>
</div>

> *Add actual screenshots of your application here to showcase the UI.*

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.