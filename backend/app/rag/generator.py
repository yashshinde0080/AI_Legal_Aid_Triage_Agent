from app.llm.router import get_llm
from app.rag.prompt import build_prompt
from langchain_core.messages import HumanMessage
from app.utils.logger import logger

async def generate_answer(context_chunks: list, question: str) -> str:
    """
    Generate an answer using the LLM and retrieved context.
    """
    try:
        # Build the prompt
        prompt_text = build_prompt(context_chunks, question)
        
        # Get the configured LLM (e.g., Gemini)
        llm = get_llm()
        
        logger.info(f"Generating answer for question: {question[:50]}...")
        
        # Invoke LLM
        response = await llm.ainvoke([HumanMessage(content=prompt_text)])
        
        return str(response.content)
        
    except Exception as e:
        logger.error(f"Generation error: {e}")
        return "I apologize, but I encountered an error while generating the answer."
