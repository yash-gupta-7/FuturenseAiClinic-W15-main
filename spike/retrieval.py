import os
import logging
from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from spike.config import DATA_FOLDER, CHUNK_SIZE, CHUNK_OVERLAP, OPENAI_API_KEY, TOP_K



# Configure logging for the retrieval module
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def load_documents(directory_path: str = DATA_FOLDER) -> List[Document]:
    """
    Reads all PDF files from the specified folder using LangChain loaders.

    Args:
        directory_path (str): Path to the folder containing PDF documents.

    Returns:
        List[Document]: A list of loaded LangChain Document objects.
    """
    logger.info(f"Attempting to load documents from directory: {directory_path}")

    # Check if path exists
    if not os.path.exists(directory_path):
        logger.warning(f"Directory '{directory_path}' does not exist. Creating directory.")
        try:
            os.makedirs(directory_path, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to create directory '{directory_path}': {e}")
        return []

    # Check if path is a directory
    if not os.path.isdir(directory_path):
        logger.error(f"Path '{directory_path}' exists but is not a directory.")
        return []

    # Check for PDF files
    pdf_files = [f for f in os.listdir(directory_path) if f.lower().endswith('.pdf')]
    if not pdf_files:
        logger.warning(f"No PDF files found in directory: {directory_path}")
        return []

    logger.info(f"Found {len(pdf_files)} PDF file(s) to load: {pdf_files}")

    try:
        # Load all PDFs in the directory
        loader = PyPDFDirectoryLoader(directory_path)
        documents = loader.load()
        logger.info(f"Successfully loaded {len(documents)} page(s) from {len(pdf_files)} PDF file(s).")
        return documents
    except Exception as e:
        logger.error(f"An error occurred while loading PDF documents: {e}")
        return []

def chunk_documents(
    documents: List[Document],
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP
) -> List[Document]:
    """
    Splits loaded documents into smaller chunks using RecursiveCharacterTextSplitter.
    Preserves source metadata from original documents.

    Args:
        documents (List[Document]): List of original LangChain Document objects.
        chunk_size (int): Character size of each chunk.
        chunk_overlap (int): Overlap size between consecutive chunks.

    Returns:
        List[Document]: List of split Document chunks.
    """
    logger.info(f"Chunking {len(documents)} document(s) with chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")

    if not documents:
        logger.warning("No documents provided to chunk.")
        return []

    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            add_start_index=True  # Preserves and adds start_index to source metadata
        )
        chunks = text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks from {len(documents)} documents.")
        return chunks
    except Exception as e:
        logger.error(f"An error occurred while splitting documents: {e}")
        return []

def create_embeddings(
    chunks: List[Document],
    persist_directory: str = "chroma_db",
    embedding_model: str = "text-embedding-3-small"
) -> Chroma:
    """
    Generates embeddings for chunks and persists them in a local ChromaDB instance.

    Args:
        chunks (List[Document]): List of chunked Document objects.
        persist_directory (str): Local directory path where ChromaDB should persist its database.
        embedding_model (str): Name of the OpenAI embedding model to use.

    Returns:
        Chroma: The initialized and populated Chroma vector store.
    """
    logger.info(f"Creating embeddings using model '{embedding_model}' and persisting to '{persist_directory}'")

    if not chunks:
        logger.warning("No chunks provided to create embeddings.")
        return None

    try:
        # Initialize OpenAIEmbeddings client using the configured API key
        embeddings = OpenAIEmbeddings(
            model=embedding_model,
            openai_api_key=OPENAI_API_KEY
        )

        # Initialize Chroma vector store and ingest the chunk documents
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_directory
        )

        logger.info(f"Successfully stored {len(chunks)} chunks in ChromaDB at '{persist_directory}'.")
        return vector_store
    except Exception as e:
        logger.error(f"An error occurred while generating embeddings or initializing ChromaDB: {e}")
        raise e

def retrieve_documents(
    query: str,
    vector_store: Chroma = None,
    persist_directory: str = "chroma_db",
    embedding_model: str = "text-embedding-3-small",
    top_k: int = TOP_K
) -> List[Dict[str, Any]]:
    """
    Searches the Chroma vector database and returns the top_k most similar document chunks.

    Args:
        query (str): The search query.
        vector_store (Chroma): The active vector store object. If None, it will be loaded from disk.
        persist_directory (str): Local path where Chroma database is persisted.
        embedding_model (str): OpenAI embedding model to use for loading the vector store.
        top_k (int): Number of most similar document chunks to retrieve.

    Returns:
        List[Dict[str, Any]]: List of dictionaries, each containing:
                              - 'content' (str): Page content of the chunk.
                              - 'metadata' (dict): Metadata of the chunk.
                              - 'source' (str): Basename of the source file.
                              - 'score' (float): Similarity/distance score.
    """
    logger.info(f"Initializing document retrieval for query: '{query}'")

    if not query.strip():
        logger.warning("Empty search query provided.")
        return []

    # Load vector store from disk if not provided
    if vector_store is None:
        logger.info(f"No active vector store provided. Loading from '{persist_directory}'...")
        if not os.path.exists(persist_directory):
            logger.warning(f"Persistence directory '{persist_directory}' does not exist. Cannot retrieve.")
            return []
        try:
            embeddings = OpenAIEmbeddings(
                model=embedding_model,
                openai_api_key=OPENAI_API_KEY
            )
            vector_store = Chroma(
                persist_directory=persist_directory,
                embedding_function=embeddings
            )
        except Exception as e:
            logger.error(f"Failed to load vector store from '{persist_directory}': {e}")
            return []

    try:
        # Perform similarity search with score
        logger.info(f"Performing similarity search (k={top_k})")
        results_with_scores = vector_store.similarity_search_with_score(query, k=top_k)

        retrieved_results = []
        for doc, score in results_with_scores:
            source_path = doc.metadata.get("source", "unknown")
            source_filename = os.path.basename(source_path)

            retrieved_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "source": source_filename,
                "score": score
            })

        logger.info(f"Successfully retrieved {len(retrieved_results)} document chunks.")
        return retrieved_results
    except Exception as e:
        logger.error(f"An error occurred during retrieval: {e}")
        return []


