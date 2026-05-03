import re

def detect_category(text: str) -> str:
    text = text.lower()
    if any(k in text for k in ["cement", "opc", "ppc", "clinker", "slag",
                                "pozzolana", "supersulphated", "masonry cement",
                                "white portland"]):
        return "cement"
    elif any(k in text for k in ["steel", "rebar", "tmt", "bar", "reinforcement"]):
        return "steel"
    elif any(k in text for k in ["concrete", "aggregate", "rcc", "mix", "mortar"]):
        return "concrete"
    elif any(k in text for k in ["block", "brick", "masonry", "hollow"]):
        return "masonry"
    elif any(k in text for k in ["pipe", "asbestos", "roofing", "sheet", "corrugated"]):
        return "products"
    return "other"

def create_chunks(file_path: str) -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    parts = re.split(r'(?=IS\s?\d{3,5})', text)

    chunks = []
    for chunk in parts:
        chunk = chunk.strip()
        if len(chunk) < 50:
            continue
        match = re.match(r'(IS\s?\d+[^\n]*)', chunk)
        standard_id = match.group(1).strip() if match else "UNKNOWN"
        chunks.append({
            "standard_id": standard_id,
            "text": chunk,
            "category": detect_category(chunk)
        })

    return chunks

if __name__ == "__main__":
    chunks = create_chunks("data/raw_text.txt")
    print(f"Total chunks: {len(chunks)}")
    for c in chunks[:5]:
        print(c["standard_id"], "|", c["category"])