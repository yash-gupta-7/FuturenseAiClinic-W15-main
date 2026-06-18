# Product Requirements Document (PRD): AI Admission Copilot

## 1. Product Overview
The **AI Admission Copilot** is an intelligent assistant designed to help admissions officers and prospective students navigate complex university admission policies, deadlines, and credit requirements. By indexing institutional PDF policies, the system provides accurate, citation-backed answers to reduce administrative overhead.

---

## 2. Target Users
- **Admissions Officers**: Query internal databases for edge-case guidelines (e.g., transfer credit limits, GPA exceptions).
- **Prospective Students**: Ask conversational questions regarding entry criteria, English proficiency waivers, and financial aid timelines.

---

## 3. Key Performance Indicators (KPIs)
To meet the standards of a production-grade AI system, the application must satisfy the following metrics:

| Metric | Target | Description |
| :--- | :--- | :--- |
| **Retrieval Accuracy (Hit Rate @ K=3)** | $\ge 95.0\%$ | The percentage of queries where the correct policy document is included in the top-3 retrieved chunks. |
| **End-to-End Latency** | $< 1.5\text{ seconds}$ | Time elapsed from user query submission to response generation. |
| **Query Cost** | $< \$0.005 / \text{query}$ | Combined API costs of embeddings (OpenAI) and LLM inference. |
| **Hallucination Rate** | $0.0\%$ | Zero fabrication of policies; responses must explicitly reference indexed chunks. |

---

## 4. Functional Requirements
1. **Document Ingestion**: Automatically watch a folder (e.g., `docs/`) for new or updated policy PDFs.
2. **Contextual Semantic Search**: Search indexed materials and return top-3 relevant context chunks with similarity scores and page metadata.
3. **Response Compiling (LLM)**: Generate precise, professional answers utilizing retrieved contexts.
4. **Audit Trail**: Output exact filename and matching score for transparency.

---

## 5. Security & Compliance
- **FERPA Compliance**: Do not log personally identifiable student data.
- **Data Isolation**: Store vectors locally or in an enterprise-secured tenant.
