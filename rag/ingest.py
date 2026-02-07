from pathlib import Path
from typing import Dict, List

def load_text_files(folder: Path) -> List[Dict]:
    """
    Reads .txt and .md files recursively from a folder.
    Returns list of dicts with doc_id, path, and text.
    """
    docs = []
    
    for p in folder.rglob("*"):
        if p.is_file() and p.suffix.lower() in [".txt", ".md"]:
            text = p.read_text(encoding="utf-8", errors="ignore")
            docs.append({
                "doc_id": p.name,
                "path": str(p),
                "text": text
            })
    return docs
 
    