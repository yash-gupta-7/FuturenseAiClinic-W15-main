import logging
import sys
from spike.retrieval import load_documents, chunk_documents, create_embeddings
from spike.evaluation import evaluate_retrieval

# Configure logging for the pipeline orchestrator
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting AI Admission Copilot Retrieval Spike Pipeline...")

    try:
        # Step 1: Load PDF documents from the configured data directory
        logger.info("--- Step 1: Loading PDF documents ---")
        documents = load_documents()
        if not documents:
            logger.error("No documents loaded. Please place PDF files in the configured docs folder.")
            sys.exit(1)

        # Step 2: Chunk documents into overlapping segments
        logger.info("--- Step 2: Chunking documents ---")
        chunks = chunk_documents(documents)
        if not chunks:
            logger.error("Document chunking yielded zero chunks. Exiting pipeline.")
            sys.exit(1)

        # Step 3: Generate embeddings and build ChromaDB index
        logger.info("--- Step 3: Generating embeddings and indexing chunks in ChromaDB ---")
        vector_store = create_embeddings(chunks)
        if vector_store is None:
            logger.error("Chroma vector store initialization failed. Exiting pipeline.")
            sys.exit(1)

        # Step 4: Run evaluation against the set of questions
        logger.info("--- Step 4: Running retrieval evaluation ---")
        metrics = evaluate_retrieval(vector_store)

        # Step 5: Print summary metrics
        print("\n" + "="*50)
        print("RETRIEVAL SPIKE EVALUATION SUMMARY")
        print("="*50)
        print(f"Total Questions Evaluated : {metrics['total_questions']}")
        print(f"Total Successful Hits     : {metrics['total_hits']}")
        print(f"Hit Rate @ K=3            : {metrics['hit_rate']:.2%}")
        print("="*50)
        print("Detailed logs and scores have been saved to 'findings.csv'\n")

    except Exception as e:
        logger.exception(f"An unexpected error occurred during pipeline execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
