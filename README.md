#  BIS Recommendation Engine

An AI-powered system that extracts BIS standards from technical documents and recommends relevant standards using **semantic search, FAISS vector indexing, and NLP embeddings**.

---

#  Problem Statement

MSMEs often struggle to identify correct BIS (Indian Standards) applicable to their products. Manual lookup is time-consuming, error-prone, and requires domain expertise.

---

#  Solution Overview

This project builds an intelligent **BIS Recommendation Engine** that:

* Takes product descriptions as input
* Extracts and processes BIS documents
* Uses semantic similarity to recommend relevant IS standards
* Provides fast and accurate results using hybrid AI retrieval

---

#  System Architecture

* PDF Data Extraction (pdfplumber)
* Text Chunking & Preprocessing
* Embedding Generation (SentenceTransformer)
* FAISS Vector Indexing for similarity search
* Hybrid Ranking (keyword + semantic + rules)
* FastAPI backend for inference
* Web UI for interaction

---

#  Features

* AI-based BIS standard recommendation
* Hybrid retrieval (keyword + semantic search)
* Category-aware filtering (cement, steel, concrete, etc.)
* Fast inference (<0.1 sec)
* REST API support
* Scalable modular architecture

---

#  Evaluation Results

* High retrieval accuracy on test dataset
* Strong ranking performance across queries
* Consistent low latency responses
* Works well for cement, steel, aggregates, and construction materials

---

#  Project Structure

* `src/extract_text.py` → PDF text extraction
* `src/chunking.py` → Text processing & categorization
* `src/vector_store.py` → Embedding + FAISS index
* `src/pipeline.py` → Core recommendation engine
* `inference.py` → Batch inference script
* `eval_script.py` → Evaluation metrics

---

#  Setup Instructions

### 1. Clone Project

```bash
cd C:\Users\YOGA\Documents
cd bis-recommendation-engine(2)
```

---

### 2. Install Dependencies

```bash
pip install sentence-transformers faiss-cpu pdfplumber streamlit fastapi uvicorn python-multipart
```

---

#  Running the Backend Server

```bash
uvicorn src.app:app --reload --port 8000
```

---

#  Running the Web Application

* Open frontend (`index.html` or Streamlit UI if used)
* Enter product description
* Get real-time BIS recommendations

---

#  Inference / Evaluation Steps

```bash
python inference.py --input data/public_test_set.json --output data/result.json
```

---

#  Final Submission Command

```bash
python inference.py --input data/public_test_set.json --output data/result.json
python eval_script.py --results data/result.json
```

---

#  Evaluation Metrics

* Hit Rate @3
* Mean Reciprocal Rank (MRR @5)
* Precision @K
* Recall @K
* Average Latency

---

#  Methodology

* Rule-based keyword mapping for domain knowledge
* Semantic embeddings for contextual similarity
* FAISS for fast vector search
* Hybrid reranking for improved accuracy

---

#  Important Note (Embeddings Dependency)

* Uses `SentenceTransformer (all-MiniLM-L6-v2)`
* Model is downloaded on first run (~80MB)
* Embeddings are cached for performance optimization

---

#  Key Highlights

* Hybrid AI + rule-based architecture
* Real-time inference (<0.1 sec)
* Domain-specific BIS intelligence system
* Modular and scalable design

---

#  Demo

* Input: “High strength cement for construction”
* Output: IS 269, IS 8112, IS 12269
* Web UI provides instant recommendations

---

#  Team Details

* Team Name: Alpha One
* Domain: AI / NLP / Industrial Compliance
* Members: Ramya Devi K 
---

#  Notes

* Designed for MSME compliance automation
* Extendable to ISO / ASTM standards
* Future scope: multilingual support, mobile app, voice input

---
