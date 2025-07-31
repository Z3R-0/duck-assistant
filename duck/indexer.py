import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
from bs4 import BeautifulSoup
import markdown
import hashlib

# Use persistent client, specify your desired path for DB files
client = chromadb.PersistentClient(path="./chromadb_data")

# Explicitly create or get the collection with the same embedder as used for queries
embedder = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    "duck_notes",
    embedding_function=embedder
)

def clean_markdown(md_text):
    html = markdown.markdown(md_text)
    return BeautifulSoup(html, features="html.parser").get_text()

def chunk_text(text, size=500):
    return [text[i:i+size] for i in range(0, len(text), size)]

vault_path = Path("C:/Users/ididt/SyncThing/main-notes").expanduser()

existing_ids = set(collection.get(ids=None)["ids"])  # fetch existing IDs to avoid duplicates

for file in vault_path.rglob("*.md"):
    with open(file, encoding="utf-8") as f:
        raw = f.read()
    chunks = chunk_text(clean_markdown(raw))
    for chunk in chunks:
        uid = hashlib.md5(chunk.encode()).hexdigest()
        if uid not in existing_ids:
            collection.add(documents=[chunk], ids=[uid])
            existing_ids.add(uid)

print(f"Indexed documents: {len(existing_ids)}")
