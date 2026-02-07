from pathlib import Path
from rag.ingest import load_text_files

def main():
    raw_dir = Path("data/raw")
    docs = load_text_files(raw_dir)
    
    print(f"Loaded {len(docs)} documents from {raw_dir}.\n")
    
    for d in docs:
        preview = d["text"][:120].replace("\n", " ")
        print(f"- {d['doc_id']} ({len(d['text'])} chars)")
        print(f"  Preview: {preview}...\n")

if __name__ == "__main__":
    main()