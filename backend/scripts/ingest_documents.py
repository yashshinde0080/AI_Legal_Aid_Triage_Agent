"""
Document Ingestion Script
Ingests legal documents into the vector store.
"""

import sys
import os
import asyncio
from pathlib import Path
from typing import Optional

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.loader import DocumentLoader
from app.rag.chunker import TextChunker
from app.rag.embedder import DocumentEmbedder
from app.db.vector import VectorStore
from app.utils.logger import setup_logger, logger


async def ingest_directory(directory: str, domain: Optional[str] = None):
    """
    Ingest all documents from a directory.
    
    Args:
        directory: Path to directory with documents
        domain: Optional domain to assign to all documents
    """
    logger.info(f"Starting ingestion from: {directory}")
    
    # Load documents
    loader = DocumentLoader()
    documents = loader.load_directory(directory)
    
    if not documents:
        logger.warning("No documents found to ingest")
        return
    
    logger.info(f"Loaded {len(documents)} documents")
    
    # Add domain if specified
    if domain:
        for doc in documents:
            doc["metadata"]["domain"] = domain
            doc["domain"] = domain
    
    # Chunk documents
    chunker = TextChunker(chunk_size=800, chunk_overlap=100)
    chunks = chunker.chunk_documents(documents)
    
    logger.info(f"Created {len(chunks)} chunks")
    
    # Create embeddings
    embedder = DocumentEmbedder(batch_size=10)
    embedded_chunks = await embedder.embed_documents(chunks)
    
    # Filter out failed embeddings
    failed = [c for c in embedded_chunks if not c.get("embedding")]
    if failed:
        raise RuntimeError(f"Embedding failed for {len(failed)} chunks")

    logger.info(f"Successfully embedded {len(embedded_chunks)} chunks")
    
    # Store in vector database
    vector_store = VectorStore()
    added = await vector_store.add_documents(embedded_chunks)
    
    logger.info(f"Added {added} chunks to vector store")


async def ingest_sample_data():
    """Ingest sample legal data for testing."""
    
    sample_documents = [
        {
            "content": """
Consumer Protection Act, 2019
Section 2 - Definitions

In this Act, unless the context otherwise requires:
(1) "advertisement" means any audio or visual publicity, representation, 
endorsement or pronouncement made by means of light, sound, smoke, gas, 
print, electronic media, internet or website.

(7) "consumer" means any person who—
(i) buys any goods for a consideration which has been paid or promised 
or partly paid and partly promised, or under any system of deferred payment;
(ii) hires or avails of any service for a consideration which has been 
paid or promised or partly paid and partly promised, or under any system 
of deferred payment.

(11) "defect" means any fault, imperfection or shortcoming in the quality, 
quantity, potency, purity or standard which is required to be maintained 
by or under any law for the time being in force.
            """,
            "act_name": "Consumer Protection Act, 2019",
            "section": "2",
            "domain": "Consumer Law",
            "source_url": "https://consumeraffairs.nic.in"
        },
        {
            "content": """
Consumer Protection Act, 2019
Section 35 - Jurisdiction of District Commission

(1) Subject to the other provisions of this Act, the District Commission 
shall have jurisdiction to entertain complaints where the value of the 
goods or services paid as consideration does not exceed one crore rupees.

(2) A complaint shall be instituted in a District Commission within the 
local limits of whose jurisdiction:
(a) the opposite party or each of the opposite parties, at the time of 
the institution of the complaint, actually and voluntarily resides or 
carries on business or has a branch office or personally works for gain; or
(b) any of the opposite parties, at the time of the institution of the 
complaint, actually and voluntarily resides, or carries on business or 
has a branch office, or personally works for gain.
            """,
            "act_name": "Consumer Protection Act, 2019",
            "section": "35",
            "domain": "Consumer Law",
            "source_url": "https://consumeraffairs.nic.in"
        },
        {
            "content": """
Consumer Complaint Filing Procedure

Step 1: Identify the appropriate forum
- District Commission: Claims up to Rs. 1 crore
- State Commission: Claims Rs. 1 crore to Rs. 10 crore
- National Commission: Claims above Rs. 10 crore

Step 2: Prepare the complaint
- Written complaint with details of the dispute
- Name and address of complainant
- Name and address of opposite party
- Facts of the case
- Documents supporting the claim
- Relief sought

Step 3: Pay the required fee
- Fee varies based on claim amount
- Can be paid via demand draft or online

Step 4: File the complaint
- Submit at the appropriate Consumer Forum
- Keep acknowledgment receipt

Step 5: Attend hearings
- Both parties present arguments
- Submit evidence
- Commission gives decision

Time Limit: Complaint should be filed within 2 years from the date 
of cause of action.
            """,
            "act_name": "Consumer Complaint Procedure",
            "section": "Filing Guide",
            "domain": "Consumer Law",
            "source_url": "https://consumerhelpline.gov.in"
        },
        {
            "content": """
Indian Penal Code, 1860
Section 420 - Cheating and dishonestly inducing delivery of property

Whoever cheats and thereby dishonestly induces the person deceived to 
deliver any property to any person, or to make, alter or destroy the 
whole or any part of a valuable security, or anything which is signed 
or sealed, and which is capable of being converted into a valuable 
security, shall be punished with imprisonment of either description 
for a term which may extend to seven years, and shall also be liable to fine.

Elements of the offence:
1. Deception of a person
2. Fraudulent or dishonest inducement
3. Delivery of property or valuable security
4. Intention to cheat

Filing a complaint:
- FIR at local police station
- Private complaint before Magistrate under Section 200 CrPC
            """,
            "act_name": "Indian Penal Code, 1860",
            "section": "420",
            "domain": "Criminal Law",
            "source_url": "https://legislative.gov.in"
        },
        {
            "content": """
Filing an FIR (First Information Report)

What is an FIR?
An FIR is a written document prepared by the police when they receive 
information about the commission of a cognizable offence.

Steps to file an FIR:
1. Visit the police station with jurisdiction over the area where 
   the offence occurred
2. Provide verbal or written information about the incident
3. The officer will record your statement
4. Read the FIR carefully before signing
5. Get a free copy of the FIR

Your rights:
- Police cannot refuse to register FIR for cognizable offences
- If refused, approach the Superintendent of Police
- Can also file complaint to Judicial Magistrate under Section 156(3) CrPC
- Zero FIR can be filed at any police station

Important:
- File FIR as soon as possible after the incident
- Keep all evidence and documents safe
- Note down names of witnesses
            """,
            "act_name": "Criminal Procedure Code",
            "section": "FIR Filing Guide",
            "domain": "Criminal Law",
            "source_url": "https://police.gov.in"
        },
        {
            "content": """
Payment of Wages Act, 1936
Section 3 - Responsibility for payment of wages

Every employer shall be responsible for the payment to persons employed 
by him of all wages required to be paid under this Act.

Section 4 - Fixation of wage-periods
Every person responsible for the payment of wages shall fix periods 
(wage-periods) in respect of which such wages shall be payable.

No wage-period shall exceed one month.

Section 5 - Time of payment of wages
The wages of every person employed upon or in any railway, factory or 
industrial establishment shall be paid before the expiry of the seventh 
day after the last day of the wage-period.

Complaint procedure:
1. File complaint before Labour Commissioner
2. Can also approach Labour Court
3. Time limit: Within 12 months of wage due date
            """,
            "act_name": "Payment of Wages Act, 1936",
            "section": "3-5",
            "domain": "Labour Law",
            "source_url": "https://labour.gov.in"
        }
    ]
    
    logger.info(f"Ingesting {len(sample_documents)} sample documents...")
    
    # Process documents
    chunker = TextChunker(chunk_size=800, chunk_overlap=100)
    embedder = DocumentEmbedder(batch_size=5)
    vector_store = VectorStore()
    
    all_chunks = []
    for doc in sample_documents:
        chunk_doc = {
            "content": doc["content"],
            "metadata": {
                "act_name": doc["act_name"],
                "section": doc["section"],
                "domain": doc["domain"],
                "source_url": doc["source_url"]
            },
            "source": doc["source_url"],
            "act_name": doc["act_name"],
            "section": doc["section"],
            "domain": doc["domain"],
            "source_url": doc["source_url"]
        }
        all_chunks.append(chunk_doc)
    
    # Embed documents
    embedded = await embedder.embed_documents(all_chunks)
    valid = [c for c in embedded if c.get("embedding")]
    
    # Store
    added = await vector_store.add_documents(valid)
    
    logger.info(f"Successfully ingested {added} sample documents")





if __name__ == "__main__":
    setup_logger()
    
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        domain = sys.argv[2] if len(sys.argv) > 2 else None
        asyncio.run(ingest_directory(directory, domain))
    else:
        # Default to Files directory in the same folder as this script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        files_dir = os.path.join(current_dir, "Files")
        
        if os.path.exists(files_dir):
            logger.info(f"Ingesting from default directory: {files_dir}")
            # Ensure the directory exists and pass it to the ingestion function
            asyncio.run(ingest_directory(files_dir))
        else:
            logger.info("Files directory not found. Ingesting sample data...")
            asyncio.run(ingest_sample_data())