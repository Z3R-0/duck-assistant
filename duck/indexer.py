import os
import chromadb
from pathlib import Path
from chromadb.utils import embedding_functions

CHROMA_PATH = Path("./bin/chromadb_data")
CHROMA_PATH.parent.mkdir(parents=True, exist_ok=True)

client = chromadb.PersistentClient(path=str(CHROMA_PATH))
embedder = embedding_functions.DefaultEmbeddingFunction()

def index_context(session_id, context_path):
    collection = client.get_or_create_collection(f"session_{session_id}", embedding_function=embedder)
    docs = []
    ids = []

    context_path = Path(context_path)
    if not context_path.exists():
        print(f"[indexer] ERROR: context_path does not exist: {context_path}")
        return

    total_chars = 0

    for root, _, files in os.walk(context_path):
        for fname in files:
            fpath = os.path.join(root, fname)
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read().strip()
            if not content:
                print(f"[indexer] Skipping empty file: {fpath}")
                continue
            docs.append(content)
            ids.append(f"{fname}_{len(ids)}")
            total_chars += len(content)

    if not docs:
        print(f"[indexer] No readable documents found in: {context_path}")
        return

    print(f"[indexer] Indexing {len(docs)} documents from: {context_path} (total size: {total_chars} chars, ~{total_chars // 4} tokens)")
    collection.add(documents=docs, ids=ids)

def query_context(query, session_id, k=5):
    collection = client.get_or_create_collection(f"session_{session_id}", embedding_function=embedder)
    results = collection.query(query_texts=[query], n_results=k)

    docs = results.get("documents", [[]])[0]
    if not docs:
        return "No relevant documents found."

    return "\n---\n".join(docs)
