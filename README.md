# AI Admission Copilot - Retrieval De-Risk Spike

This repository contains the de-risk prototype spike for the **AI Admission Copilot**. The primary goal is to evaluate document ingestion, chunking strategies, vector embeddings, and retrieval accuracy against academic and admission policies before moving to full implementation.

---

## Project Overview

The retrieval spike acts as a sandboxed testing suite. It loads policy documents in PDF format, splits them into semantic chunks, indexes them into a local vector database, and runs a standardized evaluation dataset of 10 realistic admission questions to compute the **Hit Rate @ K=3**.

---

## Repository Structure

```text
.
├── .gitignore
├── README.md                # Project documentation (this file)
└── spike/
    ├── README.md            # Spike folder documentation
    ├── config.py            # Environment configuration & hyperparameter constants
    ├── retrieval.py         # Ingestion, chunking, and ChromaDB search logic
    ├── evaluation.py        # Question dataset & performance metrics calculation
    ├── main.py              # Orchestration entry point
    └── requirements.txt     # Pinpointed library dependencies
```

---

## Setup Instructions

### 1. Clone & Navigate
Navigate to the root directory of the workspace:
```bash
cd FuturenseAiClinic-W15
```

### 2. Create and Activate Virtual Environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install the required packages using pip:
```bash
pip install -r spike/requirements.txt
```

---

## Environment Variables

The project utilizes `python-dotenv` to manage secret keys. Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your-actual-openai-api-key-here
```

---

## How to Run

1. Create a directory named `docs` in the root of the project (if it doesn't already exist):
   ```bash
   mkdir docs
   ```
2. Place all admission policy PDFs (e.g., `international_admission_policy.pdf`, `transfer_credit_policy.pdf`, etc.) inside the `docs/` folder.
3. Run the end-to-end pipeline:
   ```bash
   python -m spike.main
   ```

---

## Evaluation Methodology

The pipeline uses a testing dataset of **10 standard admission policy questions**. For each question:
1. The question is embedded using OpenAI's `text-embedding-3-small` model.
2. ChromaDB returns the **Top 3** most similar document chunks.
3. The pipeline checks if the **expected source document** containing the answer exists within those top 3 results.
4. It records the question, the matching/top retrieved document name, its similarity score, and flags whether it was a **Hit (Y/N)**.
5. All results are written to `findings.csv`.
6. Aggregate metrics (**Total Questions, Total Hits, and overall Hit Rate**) are calculated and output to the terminal.

---

## Sample Output Table

When the pipeline finishes running, it outputs detailed metrics to `findings.csv`. A representative snapshot of the evaluation looks as follows:

| Question | Expected Document | Retrieved Source | Similarity Score | Hit (Y/N) |
| :--- | :--- | :--- | :---: | :---: |
| What is the minimum TOEFL score required for international graduate applicants? | `international_admission_policy.pdf` | `international_admission_policy.pdf` | 0.231 | Y |
| Are transfer credits accepted from non-accredited community colleges? | `transfer_credit_policy.pdf` | `transfer_credit_policy.pdf` | 0.312 | Y |
| What is the deadline to submit the FAFSA for priority financial aid consideration? | `financial_aid_policy.pdf` | `financial_aid_policy.pdf` | 0.198 | Y |
| How long can an accepted student defer their enrollment? | `enrollment_deferral_policy.pdf` | `scholarship_policy.pdf` | 0.540 | N |
| What GPA is required to maintain merit-based academic scholarships? | `scholarship_policy.pdf` | `scholarship_policy.pdf` | 0.204 | Y |
