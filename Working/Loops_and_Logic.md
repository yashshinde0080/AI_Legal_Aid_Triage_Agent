# Loops and Control Logic

The system implements specific control flows to handle complex user interactions, most notably the **Clarification Loop**.

## The Clarification Loop Visualized

One of the key features of the triage agent is its ability to "ask back" rather than hallucinating an answer when information is missing.

```text
       START LOOP
           |
           v
+------------------------+
|   User Input Message   |
+-----------+------------+
            |
            v
   [CLASSIFIER AGENT] <---- Analyzes for missing entities
            |               (Jurisdiction, Date, Contract Type)
            |
            v
    Is Info Missing?
    +-------+-------+
    | No    | Yes   |
    |       |       v
    |       |  Check Safety Counter:
    |       |  [Is Count < MAX_LOOPS?]
    |       |       |       |
    |       |       | Yes   | No (Give up & Try)
    |       |       |       |
    |       |       v       +------------+
    |       |  [CLARIFICATION AGENT]     |
    |       |       |                    |
    |       |       v                    |
    |       |  Generate Question         |
    |       |       |                    |
    |       |       v                    v
    |       |   [WAIT FOR USER]      [RETRIEVER AGENT]
    |       |       |                    |
    |       |       v                    |
    |       +-------+                    |
    v                                    v
[RETRIEVER AGENT] <----------------------+
    |
    v
 [RESPONSE GENERATION]
```

## Logic Flow Steps
1. **Classification Analysis**: The `ClassifierAgent` analyzes the Input.
2. **Missing Information Check**: If critical legal details are missing (e.g., jurisdiction, specific dates, nature of contract), the agent sets `needs_clarification = True`.
3. **Graph Routing**: The `_route_after_classify` function checks this flag.
4. **Execution**:
   - The graph transitions to `clarification_node`.
   - The agent generates a question.
   - The graph ends (`END`), returning the question to the user.
5. **Re-entry**:
   - The user answers.
   - The state is re-initialized with the new input + history.
   - The process repeats.

## Loop Guard (Infinite Loop Prevention)

To prevent the agent from asking questions forever:
- The state tracks `clarification_count`.
- **Threshold**: Defined in settings (typically `max_clarification_loops = 3`).
- **Break Condition**: If `clarification_count >= max`, the router forces the path to `retrieve` regardless of missing info, doing the best it can with available data.

```python
# Simplified Logic Representation
if needs_clarification and (loop_count < MAX_LOOPS):
    return "Ask Question"
else:
    return "Proceed to Search"
```

## Error Handling Loop

```text
    [Any Node]
        |
    (Exception!)
        |
        v
 [Try/Except Block]
        |
        v
  [Error Handler]
        |
        v
  [Graceful Msg]
        |
        v
       stop
```
