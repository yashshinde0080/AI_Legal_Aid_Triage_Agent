# specialized Agents

The system delegates specific logic to specialized agent classes located in `backend/app/agents/`. These are invoked by the LangGraph nodes.

## Agent Hierarchy Diagram

```text
       +-----------------------+
       |   LangGraph Router    |
       +-----------+-----------+
                   |
     Delegates to Specialized Agents
                   |
   +---------------+------------------+-----------------+
   |               |                  |                 |
   v               v                  v                 v
+------+     +------------+     +-----------+     +-----------+
|Intake|     | Classifier |     | Retriever |     | Response  |
|Agent |     |   Agent    |     |   Agent   |     |   Agent   |
+------+     +-----+------+     +-----+-----+     +-----+-----+
   |               |                  |                 |
   |           +---+---+         +----+----+       +----+----+
   |           | LLM   |         | PgVector|       | LLM     |
   |           | Prompt|         | Store   |       | Context |
   |           +-------+         +---------+       +---------+
   v
(Safe?)
```

## Detailed Agent Descriptions

### 1. Classifier Agent (`ClassifierAgent`)
- **File**: `classifier_agent.py`
- **Role**: Analyzes the user's input to determine the legal domain and acts involved.
- **Key Methods**:
  - `classify(text, context)`: Returns a `ClassificationResult` containing domain, subdomain, confidence, and missing fields.
- **Logic**: Uses LLM prompts to extract structured data about the legal issue.

### 2. Clarification Agent (`ClarificationAgent`)
- **File**: `clarification_agent.py`
- **Role**: Generates follow-up questions when the user's query is vague.
- **Key Methods**:
  - `generate_questions(query, missing_info)`: formulated specific questions to gather missing context.
- **Logic**: specific prompting to be polite but precise in gathering legal context.

### 3. Retriever Agent (`RetrieverAgent`)
- **File**: `retriever_agent.py`
- **Role**: Interfaces with the Vector Store to find legal documents.
- **Key Methods**:
  - `retrieve(query, domain, k)`: Performs semantic search.
  - `_build_query(...)`: Enhances user query with domain-specific terms.
  - `get_act_sections(...)`: Fetches specific sections referencing exact act names.
- **Logic**: combines keyword filtering with semantic embeddings.

### 4. Response Agent (`ResponseAgent`)
- **File**: `response_agent.py`
- **Role**: Synthesizes the final answer.
- **Key Methods**:
  - `generate_response(query, retrieved_docs, context)`: Produces the final text.
- **Logic**: ensure the tone is empathetic yet professional, citing sources from the retrieved documents.

### 5. Safety Agent (`SafetyAgent`)
- **File**: `safety_agent.py`
- **Role**: Guardian of the output.
- **Key Methods**:
  - `validate(response)`: Checks for harmful content or unlicensed legal advice (e.g., claiming to be a lawyer).
- **Logic**: Content filtering and compliance checks.

### 6. Intake Agent (`IntakeAgent`)
- **File**: `intake_agent.py`
- **Role**: Pre-processing and validation.
- **Result**: Ensures input is safe and relevant before processing begins.

### 7. Memory Agent (`MemoryAgent`)
- **File**: `memory_agent.py`
- **Role**: Chat history management.
- **Logic**: Handles storage and retrieval of session history from the database/storage.
