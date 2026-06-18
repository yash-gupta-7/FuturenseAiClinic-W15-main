import logging
import pandas as pd
from typing import List, Dict, Any
from langchain_community.vectorstores import Chroma
from spike.retrieval import retrieve_documents

# Configure logging for the evaluation module
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Evaluation dataset containing realistic admission policy questions and their target source files
EVALUATION_SET: List[Dict[str, str]] = [
    {
        "question": "What is the minimum TOEFL score required for international graduate applicants?",
        "expected_document": "international_admission_policy.pdf"
    },
    {
        "question": "Are transfer credits accepted from non-accredited community colleges?",
        "expected_document": "transfer_credit_policy.pdf"
    },
    {
        "question": "What is the deadline to submit the FAFSA for priority financial aid consideration?",
        "expected_document": "financial_aid_policy.pdf"
    },
    {
        "question": "How long can an accepted student defer their enrollment?",
        "expected_document": "enrollment_deferral_policy.pdf"
    },
    {
        "question": "What GPA is required to maintain merit-based academic scholarships?",
        "expected_document": "scholarship_policy.pdf"
    },
    {
        "question": "Can waitlisted applicants submit additional recommendation letters to improve their chances?",
        "expected_document": "waitlist_policy.pdf"
    },
    {
        "question": "What is the refund schedule if a student withdraws from all classes in the first week?",
        "expected_document": "tuition_refund_policy.pdf"
    },
    {
        "question": "Are standardized test scores (SAT/ACT) required for home-schooled applicants?",
        "expected_document": "homeschool_admission_policy.pdf"
    },
    {
        "question": "Does the university offer application fee waivers for low-income domestic applicants?",
        "expected_document": "fee_waiver_policy.pdf"
    },
    {
        "question": "What is the maximum number of credits that can be transferred toward an undergraduate degree?",
        "expected_document": "transfer_credit_policy.pdf"
    }
]

def evaluate_retrieval(vector_store: Chroma, findings_path: str = "findings.csv") -> Dict[str, Any]:
    """
    Evaluates retrieval performance against the admission policy question set.
    For each question, it retrieves the top 3 chunks, checks for the expected document,
    records the details, saves them to findings.csv, and calculates metrics.

    Args:
        vector_store (Chroma): The active vector store object containing document embeddings.
        findings_path (str): File path to save evaluation results in CSV format.

    Returns:
        Dict[str, Any]: Dictionary containing aggregate metrics:
                        - 'total_questions' (int)
                        - 'total_hits' (int)
                        - 'hit_rate' (float)
    """
    logger.info("Starting retrieval evaluation...")

    results = []
    total_hits = 0
    total_questions = len(EVALUATION_SET)

    for item in EVALUATION_SET:
        question = item["question"]
        expected_doc = item["expected_document"]

        # Retrieve top 3 chunks (using Chroma search)
        retrieved_chunks = retrieve_documents(question, vector_store=vector_store, top_k=3)

        # Check if the expected document is in the retrieved chunks
        matching_chunk = next((c for c in retrieved_chunks if c["source"] == expected_doc), None)

        hit = "N"
        retrieved_source = "N/A"
        similarity_score = None

        if matching_chunk:
            hit = "Y"
            total_hits += 1
            retrieved_source = matching_chunk["source"]
            similarity_score = matching_chunk["score"]
        else:
            # If expected document is not found, record the top retrieved document (if any)
            if retrieved_chunks:
                retrieved_source = retrieved_chunks[0]["source"]
                similarity_score = retrieved_chunks[0]["score"]

        results.append({
            "Question": question,
            "Expected Document": expected_doc,
            "Retrieved Source": retrieved_source,
            "Similarity Score": similarity_score,
            "Hit (Y/N)": hit
        })

    # Save to findings.csv using pandas
    df = pd.DataFrame(results)
    try:
        df.to_csv(findings_path, index=False)
        logger.info(f"Successfully saved evaluation findings to '{findings_path}'")
    except Exception as e:
        logger.error(f"Failed to save findings to '{findings_path}': {e}")

    hit_rate = total_hits / total_questions if total_questions > 0 else 0.0

    metrics = {
        "total_questions": total_questions,
        "total_hits": total_hits,
        "hit_rate": hit_rate
    }

    logger.info(f"Evaluation Complete. Total Questions: {total_questions}, Total Hits: {total_hits}, Hit Rate: {hit_rate:.2%}")
    return metrics
