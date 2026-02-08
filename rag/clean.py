import re
import hashlib
from typing import Dict
import spacy

# Load spaCy model (we only need sentence splitting)
_nlp = spacy.load("en_core_web_sm", disable=["ner", "parser", "lemmatizer", "tagger"])
_nlp.add_pipe("sentencizer")

# Simple boilerplate patterns (you can add more later)
BOILERPLATE_PATTERNS = [
    r"(?i)copyright\s+\d{4}.*",
    r"(?i)all rights reserved.*",
    r"(?i)page\s+\d+\s+of\s+\d+",
]

def normalize_whitespace(text: str) -> str:
    """Fix weird whitespace, collapse excessive spaces/newlines."""
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def remove_boilerplate(text: str) -> str:
    """Remove common header/footer boilerplate using regex patterns."""
    for pat in BOILERPLATE_PATTERNS:
        text = re.sub(pat, "", text)
    return text

def sentence_filter(text: str) -> str:
    """
    NLP-ish cleanup:
    - split into sentences
    - remove very short/noisy sentences
    - re-join as newline separated sentences
    """
    doc = _nlp(text)
    keep = []
    for sent in doc.sents:
        s = sent.text.strip()

        # Drop very short lines (often noise)
        if len(s) < 25:
            continue

        # Drop lines with only punctuation
        if re.fullmatch(r"[\W_]+", s):
            continue

        keep.append(s)

    return "\n".join(keep)

def content_hash(text: str) -> str:
    """Hash used for deduplication (same cleaned text => same hash)."""
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()

def clean_doc(doc: Dict) -> Dict:
    """
    Takes a raw doc:
      {doc_id, path, text}
    Returns an enriched doc:
      {doc_id, path, text, clean_text, hash}
    """
    text = doc["text"]
    text = normalize_whitespace(text)
    text = remove_boilerplate(text)
    text = sentence_filter(text)

    out = dict(doc)
    out["clean_text"] = text
    out["hash"] = content_hash(text)
    return out
