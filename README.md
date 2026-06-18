# 🎓 AI Admission Copilot - Retrieval Spike

[![Status](https://img.shields.io/badge/Status-Prototype-orange.svg)]()
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![AI](https://img.shields.io/badge/Embeddings-OpenAI-green.svg)]()

This repository contains the **de-risk prototype spike** for the **AI Admission Copilot**. Before moving to full-scale development, this sandboxed suite evaluates our strategy for document ingestion, chunking algorithms, vector embeddings, and retrieval accuracy against real-world academic and admission policies.

---

## 📖 Project Overview

The primary goal of this repository is to validate our RAG (Retrieval-Augmented Generation) foundation. The pipeline performs the following end-to-end:
1. Loads complex policy documents in PDF format.
2. Splits them into semantically meaningful chunks.
3. Indexes them into a local vector database (ChromaDB).
4. Runs a standardized evaluation dataset of realistic admission queries to compute the **Hit Rate @ K=3**.

---

## 📂 Repository Structure

The project is structured to separate the core spike logic from documentation and design assets.

```text
.
├── .gitignore
├── README.md                # Main project documentation (this file)
├── EXEC_MEMO.md             # Executive summary of findings
├── FINDINGS.md              # Detailed spike evaluation findings
├── findings.csv             # Raw evaluation metrics output
├── prd/
│   └── PRD.md               # Product Requirements Document
├── design/
│   └── ARCHITECTURE.md      # Proposed System Architecture
├── diagrams/
│   └── README.md            # Visual architecture assets
└── spike/                   # Core implementation folder
    ├── README.md            # Spike-specific documentation
    ├── config.py            # Environment configuration & hyperparameters
    ├── retrieval.py         # Ingestion, chunking, and ChromaDB search logic
    ├── evaluation.py        # Question dataset & performance metrics calculation
    ├── main.py              # Orchestration entry point
    └── requirements.txt     # Pinpointed library dependencies
```

---

## 🛠️ Setup Instructions

### 1. Clone & Navigate
Navigate to the root directory of the workspace:
```bash
git clone https://github.com/yash-gupta-7/FuturenseAiClinic-W15-main.git
cd FuturenseAiClinic-W15-main
```

### 2. Virtual Environment
Create and activate a Python virtual environment to isolate dependencies:
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

### 4. Environment Variables
The project utilizes `python-dotenv` to manage secret keys. Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

---

## 🚀 How to Run the Spike

1. **Prepare Documents**: Create a directory named `docs` in the root of the project (if it doesn't already exist):
   ```bash
   mkdir docs
   ```
2. **Add Policies**: Place all your admission policy PDFs (e.g., `international_admission_policy.pdf`, `transfer_credit_policy.pdf`) inside the `docs/` folder.
3. **Execute Pipeline**: Run the end-to-end pipeline from the root directory:
   ```bash
   python -m spike.main
   ```

*(For a deeper dive into the retrieval architecture, check out the [Spike README](spike/README.md))*

---

## 🧪 Evaluation Methodology

The pipeline uses a deterministic testing dataset of standard admission policy questions. The evaluation sequence is as follows:

1. **Embedding**: The question is embedded using OpenAI's `text-embedding-3-small` model.
2. **Search**: ChromaDB performs a similarity search and returns the **Top 3** most relevant document chunks.
3. **Validation**: The pipeline checks if the **expected source document** containing the answer exists within those top 3 results.
4. **Logging**: It records the question, the top retrieved document, its similarity score, and a **Hit (Y/N)** flag.
5. **Output**: All results are written to `findings.csv`, and aggregate metrics are printed to the console.

---

## 📊 Sample Evaluation Output

When the pipeline finishes running, it outputs detailed metrics to `findings.csv`. A representative snapshot looks as follows:

| Question | Expected Document | Retrieved Source | Score | Hit |
| :--- | :--- | :--- | :---: | :---: |
| What is the minimum TOEFL score required for international applicants? | `international_admission_policy.pdf` | `international_admission_policy.pdf` | 0.231 | ✅ **Y** |
| Are transfer credits accepted from non-accredited community colleges? | `transfer_credit_policy.pdf` | `transfer_credit_policy.pdf` | 0.312 | ✅ **Y** |
| What is the deadline to submit the FAFSA for priority consideration? | `financial_aid_policy.pdf` | `financial_aid_policy.pdf` | 0.198 | ✅ **Y** |
| How long can an accepted student defer their enrollment? | `enrollment_deferral_policy.pdf` | `scholarship_policy.pdf` | 0.540 | ❌ **N** |
| What GPA is required to maintain merit-based academic scholarships? | `scholarship_policy.pdf` | `scholarship_policy.pdf` | 0.204 | ✅ **Y** |

---
*Developed as part of the Futurense AI Clinic (W15)*
