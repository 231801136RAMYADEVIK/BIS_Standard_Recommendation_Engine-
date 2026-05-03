import pdfplumber

def extract_text(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            except Exception as e:
                print(f"Skipping page {i}: {e}")
    return text

if __name__ == "__main__":
    text = extract_text("data/bis_data.pdf")
    with open("data/raw_text.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Extracted {len(text)} chars")