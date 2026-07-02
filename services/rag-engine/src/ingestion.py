"""
Oasis RAG Engine — Document Ingestion Pipeline
Parses Markdown and PDF files, chunks text, and pushes to Qdrant.
"""

import os
import glob
import uuid
import logging
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from vector_store import store

logger = logging.getLogger("oasis.rag.ingestion")

# Standard text splitter for chunking documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)

def process_file(file_path: str, category: str) -> List[Document]:
    """Parse a single file and return chunked Langchain Documents."""
    try:
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.md'):
            loader = UnstructuredMarkdownLoader(file_path)
        else:
            logger.warning(f"Unsupported file type: {file_path}")
            return []

        docs = loader.load()
        
        # Add metadata
        for doc in docs:
            doc.metadata["category"] = category
            doc.metadata["source"] = os.path.basename(file_path)
            
        chunks = text_splitter.split_documents(docs)
        logger.info(f"Processed {file_path} into {len(chunks)} chunks.")
        return chunks
        
    except Exception as e:
        logger.error(f"Failed to process {file_path}: {e}")
        return []

def process_directory(directory_path: str, category: str):
    """
    Find all PDFs and Markdown files in a directory, parse them, 
    embed them, and insert them into the vector store.
    """
    logger.info(f"Starting ingestion for directory {directory_path} (Category: {category})")
    
    all_chunks = []
    
    # Process PDFs
    for pdf_path in glob.glob(os.path.join(directory_path, "**/*.pdf"), recursive=True):
        all_chunks.extend(process_file(pdf_path, category))
        
    # Process Markdown
    for md_path in glob.glob(os.path.join(directory_path, "**/*.md"), recursive=True):
        all_chunks.extend(process_file(md_path, category))

    if not all_chunks:
        logger.warning(f"No valid documents found in {directory_path}")
        return

    # Convert Langchain Documents to expected format for VectorStore
    formatted_docs = [
        {
            "id": str(uuid.uuid4()),
            "text": chunk.page_content,
            "metadata": chunk.metadata
        }
        for chunk in all_chunks
    ]

    try:
        # Batch insert to vector store
        # Store handles the embedding internally
        store.add_documents(formatted_docs)
        logger.info(f"Successfully ingested {len(formatted_docs)} chunks from {directory_path}.")
    except Exception as e:
        logger.error(f"Failed to ingest documents to vector store: {e}")

