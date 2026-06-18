# Executive Memo: AI Admission Copilot Retrieval Spike

**To**: Executive Leadership / Course Review Panel  
**From**: Lead AI Architect  
**Subject**: Retrieval De-Risk Spike Evaluation & Phase 2 Roadmap Recommendation  
**Date**: June 18, 2026  

---

### Executive Summary
The engineering team completed the de-risk retrieval spike for the **AI Admission Copilot**. The spike tested a baseline vanilla dense vector retriever (OpenAI `text-embedding-3-small` in a local ChromaDB index) against a validation dataset of 10 standard admission policy questions. 

- **Target KPI**: Retrieval Hit Rate @ K=3 of $\ge 95.0\%$  
- **Observed KPI**: Retrieval Hit Rate @ K=3 of **$80.0\%$** (8 out of 10 questions resolved successfully)  
- **Verdict**: **No-Go for Production Deploy** on the baseline architecture. Architectural upgrades are required to reach the target accuracy thresholds.

---

### Key Failure Modes & System Risks
The 20% failure rate was driven by two distinct system vulnerabilities:
1. **Concept Collision (Vocabulary Overlap)**: Dense embeddings failed to separate the semantic space of *application fee waivers* from *general financial aid eligibility*, routing queries to the wrong document.
2. **Contextual Misalignment**: Queries referencing student *enrollment deferral* were falsely matched with *financial fee deferral* rules inside the tuition refund document due to similar financial terminology.

---

### Strategic Recommendations (Phase 2 Roadmap)
To bridge the 15% accuracy gap and safely deploy the system, we recommend implementing the following upgrades:

```text
Phase 1 (Baseline Spike)       Phase 2 (Proposed Upgrades)
[Vanilla Dense Search]  --->  [Hybrid Search (BM25 + Dense) + Cross-Encoder Re-ranking]
     (Hit Rate: 80%)                      (Projected Hit Rate: 96-98%)
```

1. **Implement Hybrid Ingestion (Dense + BM25)**: Combine dense semantic vectors with sparse lexical indices (BM25) to enforce keyword matches for critical terms (e.g., "TOEFL," "fee waiver," "SAT").
2. **Add a Cross-Encoder Re-ranking Layer**: Integrate a lightweight re-ranker (e.g., Cohere or local cross-encoder) to re-evaluate the top 10 candidates retrieved. This corrects semantic mapping errors at a marginal latency cost ($+100\text{ms}$).
3. **Structured Metadata Partitioning**: Add pre-retrieval filters based on category flags (`academic`, `financial`, `admissions`) to prevent queries from searching unrelated documents.

---

### Cost & Resource Projection
- **Spike Infrastructure**: Low cost. Embedded vectors consume minimal memory, averaging $\$0.0001$ per 1,000 document chunks.
- **Production Query Costs**: Estimated at **$\$0.0035$ per user query** (combining embedding, re-ranking, and GPT-4o-mini generation APIs), remaining well within the target budget metric ($<\$0.005$).
