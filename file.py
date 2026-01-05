from pathlib import Path

PROJECT_ROOT = Path("ai-legal-aid-triage")

DIRS = [
    # root
    PROJECT_ROOT / "backend",
    PROJECT_ROOT / "frontend",
    PROJECT_ROOT / "docs",
    PROJECT_ROOT / "scripts",

    # backend app
    PROJECT_ROOT / "backend/app",
    PROJECT_ROOT / "backend/app/api",
    PROJECT_ROOT / "backend/app/agents",
    PROJECT_ROOT / "backend/app/rag",
    PROJECT_ROOT / "backend/app/db",
    PROJECT_ROOT / "backend/app/services",
    PROJECT_ROOT / "backend/app/utils",
    PROJECT_ROOT / "backend/app/constants",

    # backend scripts
    PROJECT_ROOT / "backend/scripts",

    # frontend
    PROJECT_ROOT / "frontend/src",
    PROJECT_ROOT / "frontend/src/components",
    PROJECT_ROOT / "frontend/src/components/ui",
    PROJECT_ROOT / "frontend/src/pages",
    PROJECT_ROOT / "frontend/src/services",
    PROJECT_ROOT / "frontend/src/hooks",
    PROJECT_ROOT / "frontend/src/context",
    PROJECT_ROOT / "frontend/src/styles",
    PROJECT_ROOT / "frontend/src/lib",
]

FILES = [
    # root
    PROJECT_ROOT / "README.md",

    # backend core
    PROJECT_ROOT / "backend/requirements.txt",
    PROJECT_ROOT / "backend/.env.example",
    PROJECT_ROOT / "backend/agent.py",

    # backend app
    PROJECT_ROOT / "backend/app/__init__.py",
    PROJECT_ROOT / "backend/app/main.py",
    PROJECT_ROOT / "backend/app/config.py",

    # api
    PROJECT_ROOT / "backend/app/api/__init__.py",
    PROJECT_ROOT / "backend/app/api/auth.py",
    PROJECT_ROOT / "backend/app/api/chat.py",
    PROJECT_ROOT / "backend/app/api/health.py",

    # agents
    PROJECT_ROOT / "backend/app/agents/__init__.py",
    PROJECT_ROOT / "backend/app/agents/triage_agent.py",
    PROJECT_ROOT / "backend/app/agents/clarification_agent.py",
    PROJECT_ROOT / "backend/app/agents/retrieval_agent.py",
    PROJECT_ROOT / "backend/app/agents/validation_agent.py",
    PROJECT_ROOT / "backend/app/agents/agent_orchestrator.py",
    PROJECT_ROOT / "backend/app/agents/prompts.py",

    # rag
    PROJECT_ROOT / "backend/app/rag/__init__.py",
    PROJECT_ROOT / "backend/app/rag/embedder.py",
    PROJECT_ROOT / "backend/app/rag/retriever.py",
    PROJECT_ROOT / "backend/app/rag/chunker.py",
    PROJECT_ROOT / "backend/app/rag/loader.py",

    # db
    PROJECT_ROOT / "backend/app/db/__init__.py",
    PROJECT_ROOT / "backend/app/db/supabase.py",
    PROJECT_ROOT / "backend/app/db/vector_store.py",
    PROJECT_ROOT / "backend/app/db/models.py",

    # services
    PROJECT_ROOT / "backend/app/services/__init__.py",
    PROJECT_ROOT / "backend/app/services/classifier.py",
    PROJECT_ROOT / "backend/app/services/logger.py",

    # utils
    PROJECT_ROOT / "backend/app/utils/__init__.py",
    PROJECT_ROOT / "backend/app/utils/confidence.py",
    PROJECT_ROOT / "backend/app/utils/text_cleaner.py",

    # constants
    PROJECT_ROOT / "backend/app/constants/__init__.py",
    PROJECT_ROOT / "backend/app/constants/legal_categories.py",

    # backend scripts
    PROJECT_ROOT / "backend/scripts/ingest_documents.py",
    PROJECT_ROOT / "backend/scripts/create_embeddings.py",
    PROJECT_ROOT / "backend/scripts/test_queries.py",

    # frontend root
    PROJECT_ROOT / "frontend/index.html",
    PROJECT_ROOT / "frontend/package.json",
    PROJECT_ROOT / "frontend/.env.example",

    # frontend src
    PROJECT_ROOT / "frontend/src/App.jsx",
    PROJECT_ROOT / "frontend/src/main.jsx",

    # frontend lib
    PROJECT_ROOT / "frontend/src/lib/utils.js",

    # frontend ui components
    PROJECT_ROOT / "frontend/src/components/ui/button.jsx",
    PROJECT_ROOT / "frontend/src/components/ui/input.jsx",
    PROJECT_ROOT / "frontend/src/components/ui/card.jsx",
    PROJECT_ROOT / "frontend/src/components/ui/scroll-area.jsx",
    PROJECT_ROOT / "frontend/src/components/ui/avatar.jsx",
    PROJECT_ROOT / "frontend/src/components/ui/toast.jsx",

    # frontend components
    PROJECT_ROOT / "frontend/src/components/ChatBox.jsx",
    PROJECT_ROOT / "frontend/src/components/Message.jsx",
    PROJECT_ROOT / "frontend/src/components/Loading.jsx",
    PROJECT_ROOT / "frontend/src/components/Navbar.jsx",
    PROJECT_ROOT / "frontend/src/components/SourceCard.jsx",
    PROJECT_ROOT / "frontend/src/components/DisclaimerBanner.jsx",

    # frontend pages
    PROJECT_ROOT / "frontend/src/pages/Login.jsx",
    PROJECT_ROOT / "frontend/src/pages/Register.jsx",
    PROJECT_ROOT / "frontend/src/pages/Chat.jsx",
    PROJECT_ROOT / "frontend/src/pages/About.jsx",
    PROJECT_ROOT / "frontend/src/pages/Home.jsx",

    # frontend services
    PROJECT_ROOT / "frontend/src/services/supabaseClient.js",
    PROJECT_ROOT / "frontend/src/services/api.js",

    # frontend hooks
    PROJECT_ROOT / "frontend/src/hooks/useAuth.js",
    PROJECT_ROOT / "frontend/src/hooks/useChat.js",

    # frontend context
    PROJECT_ROOT / "frontend/src/context/AuthContext.jsx",

    # frontend styles
    PROJECT_ROOT / "frontend/src/styles/chat.css",
]


def main():
    for d in DIRS:
        d.mkdir(parents=True, exist_ok=True)

    for f in FILES:
        f.parent.mkdir(parents=True, exist_ok=True)
        f.touch(exist_ok=True)

    print("Project structure created successfully.")


if __name__ == "__main__":
    main()
