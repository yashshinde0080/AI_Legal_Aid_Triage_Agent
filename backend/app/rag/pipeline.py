from app.rag.retriever import LegalDocumentRetriever
from app.rag.generator import generate_answer
from app.utils.logger import logger

async def answer_question(question: str) -> str:
    """
    End-to-end RAG pipeline: Retrieve -> Generate.
    """
    try:
        # Retrieve context
        retriever = LegalDocumentRetriever()
        chunks = await retriever.retrieve(question, k=5)
        
        if not chunks:
            logger.info("No relevant documents found.")
            return "I don't know. No relevant legal documents were found."
            
        # Generate answer
        answer = await generate_answer(chunks, question)
        
        return answer
        
    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        return "An error occurred while processing your request."
