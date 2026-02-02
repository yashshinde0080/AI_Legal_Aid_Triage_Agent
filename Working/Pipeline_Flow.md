# Pipeline Flow (LangGraph)

The core orchestration logic is defined in `backend/app/agent/graph.py` using **LangGraph**. The system represents the triage process as a stare machine (`StateGraph`).

## Control Flow Visual

```text
                  START
                    |
                    v
            +-------+-------+
            |  Intake Node  |
            +-------+-------+
                    |
                    v
          +---------+---------+
          | Check Memory Node |
          +---------+---------+
                    |
                    v
            +-------+-------+
            | Classify Node |
            +-------+-------+
                    |
        +-----------+-----------+
        |  Routing Decision     |
        +-----------+-----------+
        |                       |
   [Needs Info?]           [Ready?]
        |                       |
        v                       v
+-------+-------+       +-------+-------+
| Clarification |       | Retrieve Node |
|     Node      |       +-------+-------+
+-------+-------+               |
        |                       v
        |               +-------+-------+
        |               | Respond Node  |
      STOP              +-------+-------+
 (Await User)                   |
                                v
                        +-------+-------+
                        | Validate Node |
                        +-------+-------+
                                |
                                v
                        +-------+-------+
                        |  Memory Node  |
                        +-------+-------+
                                |
                                v
                               END
```

## Node Details

### 1. `intake` (`intake_node`)
- **Purpose**: Initial processing of user input.
- **Function**: Validates input and prepares the state.

### 2. `check_memory` (`check_memory_node`)
- **Purpose**: Contextual awareness.
- **Function**: Checks past conversation history to understand context.

### 3. `classify` (`classify_node`)
- **Purpose**: Intent understanding.
- **Function**: Analyzes the user's query to determine the legal domain (e.g., Criminal, Civil, Family) and identifying if clarification is needed.

### 4. `clarify` (`clarification_node`)
- **Purpose**: Interactive refinement.
- **Function**: Asks the user clarifying questions if the query is ambiguous or lacks details.

### 5. `retrieve` (`retrieve_node`)
- **Purpose**: Knowledge acquisition.
- **Function**: Searches the vector database for relevant legal acts, sections, and procedures based on the classification.

### 6. `respond` (`response_node`)
- **Purpose**: Answer generation.
- **Function**: Synthesizes the retrieved information into a coherent, user-friendly response.

### 7. `validate` (`safety_node`)
- **Purpose**: Safety guardrails.
- **Function**: Checks the generated response for safety, legal compliance, and avoidance of unauthorized legal advice.

### 8. `memory` (`memory_node`)
- **Purpose**: State persistence.
- **Function**: Saves the interaction to the conversation history.

### 9. `error_handler` (`error_node`)
- **Purpose**: Resilience.
- **Function**: Handles exceptions and generates fallback messages.

## Routing Logic Detailed

```text
       [Classify Node Output]
                 |
                 v
   +-------------+--------------+
   |  _route_after_classify()   |
   +-------------+--------------+
                 |
      +----------+----------+
      |          |          |
      v          v          v
 (Errors?)   (Missing    (Clear?)
     |        Info?)        |
     |           |          |
     v           |          v
 [Error]         |      [Retrieve]
 [Node ]         |
                 v
        (Check Loop Count)
                 |
        +--------+--------+
        |                 |
    (Count < Max)    (Count >= Max)
        |                 |
        v                 v
    [Clarify]         [Retrieve]
```
