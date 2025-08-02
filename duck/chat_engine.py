import json
from pathlib import Path
from indexer import query_context, index_context
from model_interface import call_model
from session_manager import load_sessions

def load_chat_history(chat_file):
    if not Path(chat_file).exists():
        return []
    with open(chat_file, "r") as f:
        return json.load(f)

def save_chat_history(chat_file, history):
    with open(chat_file, "w") as f:
        json.dump(history, f, indent=2)

def chat_with_context(session_id, prompt):
    sessions = load_sessions()
    session = sessions[str(session_id)]

    # Reindex context if needed
    index_context(session_id, session["context_path"])

    # Retrieve relevant context
    context = query_context(prompt, session_id)

    # Format prompt
    full_prompt = f"""
    You are the user's assistant. Use the context below to answer their question. Ignore irrelevant notes.

    Context:
    {context}

    User:
    {prompt}
    """
    # Get model reply
    try:
        reply = call_model(full_prompt)
        if not reply:
            print("[chat_engine] Warning: No reply from model")
            reply = "[No response generated.]"
    except Exception as e:
        print(f"[chat_engine] Model call failed: {e}")
        reply = "[Error occurred calling the model.]"

    # Save conversation
    history = load_chat_history(session["chat_file"])
    history.append({"role": "user", "content": prompt})
    history.append({"role": "assistant", "content": reply})
    save_chat_history(session["chat_file"], history)

    return reply
