# File Tree: AI_Legal_Aid_Triage_Agent

**Generated:** 2/2/2026, 10:46:43 PM
**Root Path:** `d:\AI_Legal_Aid_Triage_Agent`

```
├── 📁 .github
│   └── 📁 instructions
│       └── 📝 kluster-code-verify.instructions.md
├── 📁 .ruff_cache
│   ├── 📁 0.14.10
│   │   └── 📄 8012550843402126444
│   ├── ⚙️ .gitignore
│   └── 📄 CACHEDIR.TAG
├── 📁 Images
│   ├── 🖼️ Screenshot 2026-02-02 212614.png
│   └── 🖼️ Screenshot 2026-02-02 212651.png
├── 📁 Working
│   ├── 📝 Agents_Description.md
│   ├── 📝 Data_Structures.md
│   ├── 📝 Loops_and_Logic.md
│   ├── 📝 Pipeline_Flow.md
│   └── 📝 System_Architecture.md
├── 📁 backend
│   ├── 📁 app
│   │   ├── 📁 agent
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 graph.py
│   │   │   ├── 🐍 nodes.py
│   │   │   ├── 🐍 prompts.py
│   │   │   ├── 🐍 state.py
│   │   │   └── 🐍 tools.py
│   │   ├── 📁 agents
│   │   │   ├── 🐍 clarification_agent.py
│   │   │   ├── 🐍 classifier_agent.py
│   │   │   ├── 🐍 intake_agent.py
│   │   │   ├── 🐍 memory_agent.py
│   │   │   ├── 🐍 response_agent.py
│   │   │   ├── 🐍 retriever_agent.py
│   │   │   └── 🐍 safety_agent.py
│   │   ├── 📁 api
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 auth.py
│   │   │   ├── 🐍 chat.py
│   │   │   ├── 🐍 health.py
│   │   │   └── 🐍 sessions.py
│   │   ├── 📁 db
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 supabase.py
│   │   │   └── 🐍 vector.py
│   │   ├── 📁 llm
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 embeddings.py
│   │   │   └── 🐍 router.py
│   │   ├── 📁 memory
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 long_term.py
│   │   │   ├── 🐍 short_term.py
│   │   │   └── 🐍 summarizer.py
│   │   ├── 📁 rag
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 chunker.py
│   │   │   ├── 🐍 embedder.py
│   │   │   ├── 🐍 generator.py
│   │   │   ├── 🐍 loader.py
│   │   │   ├── 🐍 pipeline.py
│   │   │   ├── 🐍 prompt.py
│   │   │   └── 🐍 retriever.py
│   │   ├── 📁 utils
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 confidence.py
│   │   │   ├── 🐍 guardrails.py
│   │   │   └── 🐍 logger.py
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 config.py
│   │   └── 🐍 main.py
│   ├── 📁 scripts
│   │   ├── 📁 Files
│   │   │   └── 📕 gees110.pdf
│   │   ├── 🐍 build_embeddings.py
│   │   ├── 🐍 ingest_documents.py
│   │   └── 🐍 setup_database.py
│   ├── 📁 tests
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 test_agent.py
│   │   ├── 🐍 test_api.py
│   │   └── 🐍 test_rag.py
│   ├── ⚙️ .env.example
│   ├── ⚙️ .gitignore
│   ├── 📝 README.md
│   ├── 🐍 check_imports.py
│   ├── 🐍 debug_vector.py
│   ├── 🐍 main.py
│   ├── ⚙️ pyproject.toml
│   ├── 📄 requirements.txt
│   ├── 📄 schema.sql
│   ├── 🐍 test_api_connection.py
│   ├── 📄 test_output.txt
│   ├── 📄 test_result.txt
│   └── 📄 uv.lock
├── 📁 frontend
│   ├── 📁 public
│   │   └── 🖼️ vite.svg
│   ├── 📁 src
│   │   ├── 📁 assets
│   │   │   └── 🖼️ react.svg
│   │   ├── 📁 components
│   │   │   ├── 📁 chat
│   │   │   │   ├── 📄 ChatBubble.tsx
│   │   │   │   ├── 📄 ChatWindow.tsx
│   │   │   │   ├── 📄 MessageInput.tsx
│   │   │   │   └── 📄 TypingIndicator.tsx
│   │   │   ├── 📁 layout
│   │   │   │   ├── 📄 Header.tsx
│   │   │   │   └── 📄 Layout.tsx
│   │   │   ├── 📁 sidebar
│   │   │   │   ├── 📄 NewChatButton.tsx
│   │   │   │   └── 📄 SessionList.tsx
│   │   │   └── 📁 ui
│   │   │       ├── 📄 avatar.tsx
│   │   │       ├── 📄 button.tsx
│   │   │       ├── 📄 card.tsx
│   │   │       ├── 📄 dropdown-menu.tsx
│   │   │       ├── 📄 input.tsx
│   │   │       ├── 📄 label.tsx
│   │   │       ├── 📄 scroll-area.tsx
│   │   │       ├── 📄 separator.tsx
│   │   │       ├── 📄 toast.tsx
│   │   │       └── 📄 toaster.tsx
│   │   ├── 📁 context
│   │   │   └── 📄 AuthContext.tsx
│   │   ├── 📁 hooks
│   │   │   ├── 📄 use-toast.ts
│   │   │   ├── 📄 useAuth.ts
│   │   │   ├── 📄 useChat.ts
│   │   │   ├── 📄 useSession.ts
│   │   │   └── 📄 useToast.ts
│   │   ├── 📁 lib
│   │   │   ├── 📄 api.ts
│   │   │   ├── 📄 supabase.ts
│   │   │   ├── 📄 types.ts
│   │   │   └── 📄 utils.ts
│   │   ├── 📁 pages
│   │   │   ├── 📄 Chat.tsx
│   │   │   ├── 📄 Login.tsx
│   │   │   └── 📄 NotFound.tsx
│   │   ├── 🎨 App.css
│   │   ├── 📄 App.tsx
│   │   ├── 🎨 index.css
│   │   ├── 📄 main.tsx
│   │   └── 📄 vite-env.d.ts
│   ├── ⚙️ .env.example
│   ├── ⚙️ .gitignore
│   ├── 📝 README.md
│   ├── ⚙️ components.json
│   ├── 📄 eslint.config.js
│   ├── 🌐 index.html
│   ├── ⚙️ package-lock.json
│   ├── ⚙️ package.json
│   ├── ⚙️ tsconfig.app.json
│   ├── 📄 tsconfig.app.tsbuildinfo
│   ├── ⚙️ tsconfig.json
│   ├── ⚙️ tsconfig.node.json
│   ├── 📄 tsconfig.node.tsbuildinfo
│   └── 📄 vite.config.ts
├── 📁 landing_page
│   ├── 📁 public
│   │   └── 🖼️ vite.svg
│   ├── 📁 src
│   │   ├── 📁 assets
│   │   │   └── 🖼️ react.svg
│   │   ├── 📁 components
│   │   │   ├── 📁 fancy
│   │   │   ├── 📁 logos
│   │   │   │   ├── 📄 FastAPI.tsx
│   │   │   │   ├── 📄 Gemini.tsx
│   │   │   │   ├── 📄 GooglePaLM.tsx
│   │   │   │   ├── 📄 HuggingFace.tsx
│   │   │   │   ├── 📄 LangChain.tsx
│   │   │   │   ├── 📄 MagicUI.tsx
│   │   │   │   ├── 📄 MediaWiki.tsx
│   │   │   │   ├── 📄 OpenAI.tsx
│   │   │   │   ├── 📄 Python.tsx
│   │   │   │   ├── 📄 Replit.tsx
│   │   │   │   ├── 📄 Supabase.tsx
│   │   │   │   ├── 📄 VSCodium.tsx
│   │   │   │   └── 📄 index.ts
│   │   │   ├── 📁 ui
│   │   │   │   ├── 📄 accordion.tsx
│   │   │   │   ├── 📄 badge.tsx
│   │   │   │   ├── 📄 button.tsx
│   │   │   │   ├── 📄 card.tsx
│   │   │   │   ├── 📄 chart.tsx
│   │   │   │   ├── 📄 infinite-slider.tsx
│   │   │   │   ├── 📄 input.tsx
│   │   │   │   ├── 📄 label.tsx
│   │   │   │   ├── 📄 select.tsx
│   │   │   │   └── 📄 textarea.tsx
│   │   │   ├── 📁 uitripled
│   │   │   │   ├── 📄 bento-grid-block-shadcnui.tsx
│   │   │   │   ├── 📄 glowy-waves-hero-shadcnui.tsx
│   │   │   │   ├── 📄 n8n-workflow-block-shadcnui.tsx
│   │   │   │   └── 📄 stats-counter-block-shadcnui.tsx
│   │   │   ├── 📄 call-to-action.tsx
│   │   │   ├── 📄 contact.tsx
│   │   │   ├── 📄 content-5.tsx
│   │   │   ├── 📄 faqs-3.tsx
│   │   │   ├── 📄 features-9.tsx
│   │   │   ├── 📄 footer.tsx
│   │   │   ├── 📄 hero.tsx
│   │   │   ├── 📄 infinite-slider.tsx
│   │   │   ├── 📄 integrations-7.tsx
│   │   │   ├── 📄 logo.tsx
│   │   │   └── 📄 stats.tsx
│   │   ├── 📁 lib
│   │   │   └── 📄 utils.ts
│   │   ├── 🎨 App.css
│   │   ├── 📄 App.tsx
│   │   ├── 🎨 index.css
│   │   └── 📄 main.tsx
│   ├── ⚙️ .gitignore
│   ├── 📝 README.md
│   ├── ⚙️ components.json
│   ├── 📄 eslint.config.js
│   ├── 🌐 index.html
│   ├── ⚙️ package-lock.json
│   ├── ⚙️ package.json
│   ├── ⚙️ tsconfig.app.json
│   ├── ⚙️ tsconfig.json
│   ├── ⚙️ tsconfig.node.json
│   └── 📄 vite.config.ts
├── ⚙️ .gitignore
├── 📝 README.md
├── 📄 guide.txt
└── 📄 requirements.txt
```

---
*Generated by FileTree Pro Extension*