
# BIS Standards Recommendation Engine

An AI-powered RAG system that recommends BIS (Bureau of Indian Standards) standards for Indian MSEs based on product descriptions. Built for the BIS × SS Hackathon 2026.

## Evaluation Results

| Metric | Score | Target | Status |
|--------|-------|--------|--------|
| Hit Rate @3 | 100% | >80% | ✅ |
| MRR @5 | 1.0 | >0.7 | ✅ |
| Avg Latency | 0.03s | <5s | ✅ |

## Frontend

- **URL**: `http://localhost:8000`
- **Tech**: HTML + CSS + Vanilla JS served via FastAPI StaticFiles
- **Features**:
  - Product description input with example query chips
  - Ranked standard cards with IS number + category label
  - 💡 LLM-generated rationale per standard (Groq)
  - Latency badge showing response time per query
  - Stats bar showing Hit Rate 100% / MRR 1.0 / Latency <0.1s

## LLM Integration

- **Provider**: Groq (free tier)
- **Model**: `llama-3.3-70b-versatile`
- **Purpose**: Generates one-sentence rationale for each recommended standard
- **Flow**: FAISS retrieves top-5 standards → Groq LLM explains why each standard applies to the product

## System Architecture

```
BIS SP 21 PDF
     ↓
extract_text.py  →  raw_text.txt
     ↓
chunking.py      →  IS-header based chunks + category tags
     ↓
vector_store.py  →  FAISS IndexFlatIP (cosine similarity)
     ↓
pipeline.py      →  Priority map + FAISS retrieval + reranking
     ↓
Groq LLM         →  Rationale per standard
     ↓
app.py           →  FastAPI backend serving frontend + API
     ↓
inference.py     →  JSON output (id, retrieved_standards, latency)
```

## Project Structure

```
BIS-RECOMMENDATION-ENGINE/
├── src/
│   ├── __init__.py
│   ├── extract_text.py      # PDF text extraction via pdfplumber
│   ├── chunking.py          # IS-header based chunking + category tagging
│   ├── vector_store.py      # SentenceTransformer embeddings + FAISS index
│   ├── pipeline.py          # Priority map + retrieval + reranking
│   └── app.py               # FastAPI backend + Groq LLM rationale
├── data/
│   ├── bis_data.pdf         # BIS SP 21 source document
│   ├── raw_text.txt         # Extracted text (generated)
│   ├── public_test_set.json # Public test queries
│   ├── result.json          # Public test results
│   └── embeddings_cache.pkl # Cached FAISS embeddings
├── static/
│   └── index.html           # Web UI frontend
├── inference.py             # Judge entry-point script
├── eval_script.py           # Organizer evaluation script
├── requirements.txt
├── README.md
└── presentation.pdf
```

## Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/bis-recommendation-engine.git
cd bis-recommendation-engine
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Extract PDF Text (run once)
```bash
python src/extract_text.py
```

### 4. Run Inference
```bash
python inference.py --input data/public_test_set.json --output data/result.json
```

### 5. Evaluate
```bash
python eval_script.py --results data/result.json
```

### 6. Run Frontend
```bash
uvicorn src.app:app --reload --port 8000
```

Open browser: `http://localhost:8000`

## Methodology

### Chunking Strategy
- Regex split on `IS\d{3,5}` headers — one chunk = one IS standard
- Minimum length filter: 50 characters
- Category tagging: cement / steel / concrete / masonry / products

### Retrieval Strategy
1. **Priority Map** — keyword to IS standard mapping, sorted by key length (longest match first)
2. **Category Filter** — query category detected, only matching chunks searched
3. **FAISS Cosine Search** — IndexFlatIP with normalize_L2, top-15 candidates
4. **Reranking** — word overlap + category bonus + IS-presence scoring
5. **Final Output** — top-5 standards returned

### LLM Rationale
- Top-5 standards passed to Groq llama-3.3-70b-versatile
- One-sentence explanation generated per standard
- Displayed in frontend under each result card

## External APIs and Models

| Service | Usage |
|---------|-------|
| Groq API (llama-3.3-70b-versatile) | LLM rationale generation |
| HuggingFace (all-MiniLM-L6-v2) | Sentence embeddings |

## Environment Variables

Set your Groq API key in `src/app.py`:
```python
client = Groq(api_key="your_groq_key_here")
```

## Requirements

```
sentence-transformers
faiss-cpu
pdfplumber
numpy
fastapi
uvicorn
python-multipart
groq
```

## Demo

**Input**: `33 grade OPC cement for construction`

**Output**:
```
#1  IS 269: 1989   — OPC 33 Grade Cement
    💡 Covers chemical and physical requirements for 33 grade OPC cement

#2  IS 8112: 1989  — OPC 43 Grade Cement
    💡 Referenced alongside 33 grade for comparative OPC specifications

#3  IS 12269: 1987 — OPC 53 Grade Cement
    💡 Higher grade OPC standard often considered with 33 grade compliance
```

## Team

| | |
|-|-|
| **Team Name** | Alpha One |
| **Member** | Ramya Devi K |
| **Domain** | AI / NLP / Industrial Compliance |
| **Event** | BIS × SS Hackathon 2026 |

## Notes

- Embeddings auto-cached to `data/embeddings_cache.pkl` after first run
- Model `all-MiniLM-L6-v2` downloads ~80MB on first run
- Designed for MSME compliance automation
- Extendable to ISO / ASTM / other standards
- Future scope: multilingual support, mobile app, voice input
```

Then in terminal:
```bash
git add README.md
git commit -m "add README"
git push
```
