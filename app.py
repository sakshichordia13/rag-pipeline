from pathlib import Path
from rag.ingest import load_text_files
from rag.clean import clean_doc

def main():
    raw_dir = Path("data/raw")
    docs = load_text_files(raw_dir)

    print(f"Loaded {len(docs)} raw documents.\n")

    cleaned_docs = []
    seen = set()

    for d in docs:
        cd = clean_doc(d)

        # Deduplicate (skip identical cleaned content)
        if cd["hash"] in seen:
            continue
        seen.add(cd["hash"])
        cleaned_docs.append(cd)

    print(f"After cleaning + dedupe: {len(cleaned_docs)} documents.\n")

    for d in cleaned_docs:
        preview = d["clean_text"][:160].replace("\n", " ")
        print(f"- {d['doc_id']}")
        print(f"  Cleaned chars: {len(d['clean_text'])}")
        print(f"  Preview: {preview}...\n")

if __name__ == "__main__":
    main()
