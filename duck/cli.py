import chromadb
import requests
import sys
from chromadb.utils import embedding_functions

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3"

client = chromadb.PersistentClient(path="./chromadb_data")
embedder = embedding_functions.DefaultEmbeddingFunction()

def query_model(prompt, system_prompt="You are a helpful assistant."):
    payload = {
        "model": MODEL,
        "prompt": f"{system_prompt}\n\n{prompt}",
        "stream": False
    }
    r = requests.post(OLLAMA_URL, json=payload)
    data = r.json()
    if "response" not in data:
        print("Unexpected response:", data)
        sys.exit(1)
    return data["response"]

def rag_context(user_input, k=5):
    collection = client.get_or_create_collection(
        "duck_notes",
        embedding_function=embedder
    )
    results = collection.query(query_texts=[user_input], n_results=k)

    if not results["documents"] or not results["documents"][0]:
        return "No relevant documents found."

    return "\n---\n".join(results["documents"][0])

def main():
    user_query = " ".join(sys.argv[1:])
    context = rag_context(user_query)
    prompt = f"""Use the following notes to answer the user's query.
    These are personal notes written by the user. 
    Use them as a reference to answer the following query as if you were the user's assistant.

    Notes:
    {context}

    Answer using the information from the context as a basis. 
    If the context doesn't include enough relevant info, mention that.

    Query:
    {user_query}
    """

    print(query_model(prompt))
