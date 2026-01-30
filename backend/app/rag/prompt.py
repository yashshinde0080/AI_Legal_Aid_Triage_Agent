from typing import List, Dict, Any

def build_prompt(context_chunks: List[Dict[str, Any]], question: str) -> str:
    """
    Build a prompt for the LLM using retrieved context.
    """
    context = "\n\n".join(
        f"[Source: {c.get('act_name', 'Unknown')} S.{c.get('section', 'Unknown')}]\n{c['content']}" 
        for c in context_chunks
    )

    return f"""
You are a legal assistant. Answer ONLY using the context below.
If the answer is not present, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
""".strip()
