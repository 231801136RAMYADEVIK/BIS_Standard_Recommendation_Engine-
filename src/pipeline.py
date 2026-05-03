import re
import time
import numpy as np
import faiss
from src.chunking import create_chunks, detect_category
from src.vector_store import build_index, model

# Load once at import
chunks = create_chunks("data/raw_text.txt")
index, texts, embeddings, standard_ids = build_index(chunks)

PRIORITY_MAP = {
    # SPECIFIC PHRASES FIRST (longest match priority)
    "hollow lightweight":          ["IS 2185 (Part 2): 1983"],
    "solid lightweight":           ["IS 2185 (Part 2): 1983"],
    "lightweight concrete":        ["IS 2185 (Part 2): 1983"],
    "not intended for structural": ["IS 3466: 1988"],
    "masonry mortar":              ["IS 3466: 1988"],
    "mortar masonry":              ["IS 3466: 1988"],
    "general purpose":             ["IS 3466: 1988"],
    "natural source":              ["IS 383: 1970"],
    "structural concrete":         ["IS 383: 1970", "IS 456: 2000"],
    "masonry block":               ["IS 2185 (Part 2): 1983", "IS 2185 (Part 1): 1979"],

    # OPC grades
    "33 grade":              ["IS 269: 1989"],
    "43 grade":              ["IS 8112: 1989"],
    "53 grade":              ["IS 12269: 1987"],
    "ordinary portland":     ["IS 269: 1989", "IS 8112: 1989", "IS 12269: 1987"],
    "opc":                   ["IS 269: 1989", "IS 8112: 1989", "IS 12269: 1987"],

    # Cement variants
    "portland slag":         ["IS 455: 1989"],
    "slag cement":           ["IS 455: 1989"],
    "calcined clay":         ["IS 1489 (Part 2): 1991"],
    "fly ash":               ["IS 1489 (Part 1): 1991", "IS 3812: 1981"],
    "pozzolana":             ["IS 1489 (Part 2): 1991", "IS 1489 (Part 1): 1991"],
    "masonry cement":        ["IS 3466: 1988"],
    "mortar":                ["IS 3466: 1988", "IS 2250: 1981"],
    "supersulphated":        ["IS 6909: 1990"],
    "marine":                ["IS 6909: 1990"],
    "aggressive water":      ["IS 6909: 1990"],
    "white portland":        ["IS 8042: 1989"],
    "white cement":          ["IS 8042: 1989"],
    "rapid hardening":       ["IS 8041: 1990"],
    "high alumina":          ["IS 6452: 1989"],
    "sulphate resisting":    ["IS 12330: 1988"],
    "low heat":              ["IS 12600: 1989"],
    "cement":                ["IS 269: 1989", "IS 8112: 1989", "IS 12269: 1987"],

    # Aggregates
    "coarse aggregate":      ["IS 383: 1970"],
    "fine aggregate":        ["IS 383: 1970"],
    "natural aggregate":     ["IS 383: 1970"],
    "aggregate":             ["IS 383: 1970"],
    "sand":                  ["IS 383: 1970", "IS 2116: 1980"],

    # Concrete pipes
    "precast concrete pipe": ["IS 458: 2003"],
    "concrete pipe":         ["IS 458: 2003"],
    "water main":            ["IS 458: 2003"],
    "pipe":                  ["IS 458: 2003", "IS 1592: 2003"],

    # Blocks / masonry
    "autoclaved":            ["IS 2185 (Part 3): 1984"],
    "lightweight":           ["IS 2185 (Part 2): 1983"],
    "hollow":                ["IS 2185 (Part 2): 1983", "IS 2185 (Part 1): 1979"],
    "block":                 ["IS 2185 (Part 2): 1983", "IS 2185 (Part 1): 1979"],
    "clay brick":            ["IS 1077: 1992"],
    "brick":                 ["IS 1077: 1992"],

    # Sheets / roofing
    "asbestos cement sheet": ["IS 459: 1992"],
    "corrugated":            ["IS 459: 1992"],
    "asbestos":              ["IS 459: 1992", "IS 1592: 2003"],
    "roofing":               ["IS 459: 1992", "IS 2096: 1992"],
    "cladding":              ["IS 459: 1992"],

    # Steel
    "tmt":                   ["IS 1786: 2008"],
    "rebar":                 ["IS 1786: 2008"],
    "reinforcement":         ["IS 1786: 2008"],
    "steel bar":             ["IS 1786: 2008"],
    "steel":                 ["IS 1786: 2008"],

    # Concrete
    "rcc":                   ["IS 456: 2000"],
    "concrete":              ["IS 456: 2000"],
}


def get_priority_standards(query: str) -> list[str]:
    q = query.lower()
    results = []
    for key in sorted(PRIORITY_MAP.keys(), key=len, reverse=True):
        if key in q:
            for s in PRIORITY_MAP[key]:
                if s not in results:
                    results.append(s)
    return results[:3]


def normalize_standard(std: str) -> str:
    std = std.strip()
    std = re.sub(r'\s+', ' ', std)
    std = re.sub(r'\s*:\s*', ': ', std)
    std = re.sub(r'\s*\(\s*', ' (', std)
    std = re.sub(r'\s*\)\s*', ')', std)
    return std.upper()


def extract_all_standards(text: str) -> list[str]:
    matches = re.findall(
        r'IS\s*\d+(?:\s*\(Part\s*\d+\))?(?:\s*:\s*\d{4})?',
        text, re.IGNORECASE
    )
    seen = []
    for m in matches:
        std = normalize_standard(m)
        if std not in seen:
            seen.append(std)
    return seen


def retrieve(query: str, k: int = 15) -> list[str]:
    q_category = detect_category(query)

    filtered = [
        (texts[i], embeddings[i])
        for i, chunk in enumerate(chunks)
        if chunk["category"] == q_category
    ]

    if not filtered:
        filtered = list(zip(texts, embeddings))

    f_texts, f_embeddings = zip(*filtered)
    fe = np.array(f_embeddings).astype('float32')
    faiss.normalize_L2(fe)

    temp_index = faiss.IndexFlatIP(fe.shape[1])
    temp_index.add(fe)

    qv = np.array(model.encode([query])).astype('float32')
    faiss.normalize_L2(qv)

    D, I = temp_index.search(qv, min(k, len(f_texts)))
    return [f_texts[i] for i in I[0]]


def rerank(query: str, retrieved: list[str]) -> list[str]:
    q = query.lower()
    query_words = set(q.split())
    category_keys = ["cement", "steel", "concrete", "block",
                     "aggregate", "pipe", "brick", "asbestos", "roofing"]

    def score(chunk):
        cl = chunk.lower()
        overlap = sum(w in cl for w in query_words)
        cat_bonus = sum(5 for k in category_keys if k in q and k in cl)
        is_bonus = 2 if re.search(r'\bis\s+\d+', cl) else 0
        return overlap + cat_bonus + is_bonus

    return sorted(retrieved, key=score, reverse=True)


def get_recommendations(query: str) -> tuple[list[str], float]:
    start = time.time()

    priority = get_priority_standards(query)
    retrieved = retrieve(query, k=15)
    reranked = rerank(query, retrieved)

    standards = list(priority)

    for chunk in reranked[:8]:
        for std in extract_all_standards(chunk):
            if std not in standards:
                standards.append(std)

    return standards[:5], round(time.time() - start, 3)