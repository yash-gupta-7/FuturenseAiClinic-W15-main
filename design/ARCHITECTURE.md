# System Architecture Design: AI Admission Copilot

This document outlines the software architecture and data pipeline design for the AI Admission Copilot system.

---

## 1. System Architecture

The system is designed around a **Modular RAG (Retrieval-Augmented Generation)** pattern. The block diagram below illustrates the ingestion and query processing pipelines:

```mermaid
flowchart TD
    %% Ingestion Flow
    subgraph Ingestion Pipeline
        PDF[Policy PDFs in /docs] --> Loader[LangChain PDF Loader]
        Loader --> Splitter[Recursive Splitter: Size 1000, Overlap 200]
        Splitter --> Embedder[OpenAI text-embedding-3-small]
        Embedder --> VectorDB[(ChromaDB local storage)]
    end

    %% Query Flow
    subgraph Query Pipeline
        UserQuery[User Query] --> QueryEmbed[Embed Query]
        QueryEmbed --> VectorDB
        VectorDB --> Search[Similarity Search K=3]
        Search --> Contexts[Retrieved Chunks + Metadata]
        Contexts --> LLM[OpenAI GPT-4o-mini]
        LLM --> Response[Citation-backed Answer]
    end
```

---

## 2. Ingestion Pipeline Detail
- **PDF Loader**: Uses `PyPDFDirectoryLoader` to read documents page-by-page.
- **Splitter**: Uses `RecursiveCharacterTextSplitter` configured with character delimiters `["\n\n", "\n", " ", ""]` to ensure boundaries between paragraphs are maintained, avoiding splitting mid-term.
- **Metadata Preservation**: Each document chunk maintains:
  - `source`: File path (converted to basename) for citation tracking.
  - `page`: Page index within the source PDF.
  - `start_index`: Character offset within the document for exact search alignment.

---

## 3. Database Selection
- **Spike Database**: ChromaDB (lightweight, SQLite-backed, local persistence).
- **Production Database**: Proposed transition to **Qdrant** or **pgvector (PostgreSQL)** to support horizontal scaling, metadata filtering at scale, and high-concurrency connections.
