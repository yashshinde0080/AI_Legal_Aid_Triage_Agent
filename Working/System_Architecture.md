# System Architecture

## Overview
The **AI Legal Aid Triage Agent** is a sophisticated legal assistance system designed to triage user queries, classify legal issues, and provide relevant legal information using a text-based interface. The system is built on a modular architecture separating the frontend (React) from the backend (FastAPI + LangGraph).

## High-Level Architecture Diagram

```text
+---------------------------------------------------------------+
|                      FRONTEND (React)                         |
|                                                               |
|   +----------------+      +---------------------------+       |
|   |  Chat Interface|      | State Management (Zustand)|       |
|   +-------+--------+      +-------------+-------------+       |
|           |                             ^                     |
|           | HTTP / JSON                 |                     |
|           v                             |                     |
+-----------+-----------------------------+---------------------+
            |                             ^
            | POST /api/chat              | Response
            v                             |
+---------------------------------------------------------------+
|                       BACKEND (FastAPI)                       |
|                                                               |
|  +-------------------+    +--------------------------------+  |
|  | API Routes        |--->|    LegalTriageAgent (Logic)    |  |
|  | (main.py)         |    |        (LangGraph)             |  |
|  +-------------------+    +--------------+-----------------+  |
|                                          |                    |
|                                          v                    |
|                           +--------------------------------+  |
|                           |      Orchestration Engine      |  |
|                           |   (Intake -> Classify -> ...)  |  |
|                           +--------------+-----------------+  |
|                                          |                    |
|            +-----------------------------+-----------------+  |
|            |                             |                 |  |
|   +--------v--------+           +--------v------+    +-----v--+
|   | Specialized     |           |   Knowledge   |    | Memory |
|   | Agents (LLM)    |           |   Base (RAG)  |    | (DB)   |
|   +-----------------+           +---------------+    +--------+
|                                                               |
+---------------------------------------------------------------+
```

## Backend Structure (`backend/`)

The backend is structured around the `app` package, which contains the core logic.

### Key Directories
- **`app/api`**: specific definitions of api's.
- **`app/agent`**: Defines the orchestration logic using LangGraph (`graph.py`, `state.py`, `nodes.py`).
- **`app/agents`**: Contains the specialized agent classes (`ClassifierAgent`, `RetrieverAgent`, etc.) that perform specific tasks.
- **`app/rag`**: Implements the Retrieval-Augmented Generation (RAG) pipeline for fetching legal documents.
- **`app/db`**: Database interactions, including vector store operations for RAG.
- **`app/llm`**: LLM configurations and routing.
- **`app/memory`**: Conversation memory management.

## Core Components Interaction Flow

```text
USER REQUEST
     |
     v
[FastAPI Endpoint]
     |
     v
[LangGraph runner]
     |
     +---> 1. INTAKE (Check input safety)
     |
     +---> 2. MEMORY (Load context)
     |
     +---> 3. CLASSIFIER (Analyze intent)
     |        |
     |        +---> IF Vague? ----> [CLARIFICATION LOOPS]
     |        |
     |        +---> IF Clear? ----> [RETRIEVAL (RAG)]
     |                                   |
     |                                   v
     +----------------------------- 4. GENERATION
     |                              (Draft Answer)
     |
     +---> 5. SAFETY CHECK (Validate Answer)
     |
     v
FINAL RESPONSE
```

## Technology Stack
- **Framework**: FastAPI (Python)
- **Orchestration**: LangGraph
- **Database**: PostgreSQL (with pgvector for embeddings)
- **LLM**: Integrated via `app/llm` (supporting multiple providers)
- **Vector Store**: Custom implementation wrapping pgvector logic (`app/db/vector.py`).
