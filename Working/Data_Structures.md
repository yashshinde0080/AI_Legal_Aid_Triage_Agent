# Data Structures & State Management

The system relies on strict typing and state management to ensure reliability.

## Agent State (`LegalAgentState`)
Defined in `backend/app/agent/state.py`, this `TypedDict` acts as the shared memory for the entire graph execution.

### Schema
| Field | Type | Description |
|-------|------|-------------|
| `user_input` | `str` | The original message from the user. |
| `session_id` | `str` | Unique identifier for the conversation session. |
| `chat_history` | `List[ChatMessage]` | Contextual history of the conversation. |
| `classification` | `ClassificationResult` | Outcome of the intent classification step. |
| `retrieved_docs` | `List[RetrievedDocument]` | List of legal documents found by the retriever. |
| `needs_clarification` | `bool` | Flag triggering the clarification loop. |
| `clarification_count` | `int` | Counter to prevent infinite clarification loops. |
| `response` | `str` | The final generated response. |
| `error` | `Optional[str]` | Error message if a failure occurs. |

## Key Types

### `ClassificationResult`
```python
class ClassificationResult(TypedDict):
    domain: str          # e.g., "Criminal Law"
    sub_domain: str      # e.g., "Theft"
    confidence: float    # 0.0 to 1.0
    missing_fields: List[str] # Information needed
```

### `RetrievedDocument`
```python
class RetrievedDocument(TypedDict):
    id: str
    content: str
    title: str            # e.g., "Indian Penal Code"
    section: str          # e.g., "Section 378"
    source_url: str
    score: float          # Relevance score
```

### `ChatMessage`
Standardizes the history format across the system.
```python
class ChatMessage(TypedDict):
    role: str    # "user" or "assistant"
    content: str
    timestamp: str
```
