import os
import json
from pathlib import Path

SESSION_INDEX = Path("bin/session_index.json")

def load_sessions():
    if not SESSION_INDEX.exists():
        return {}
    with open(SESSION_INDEX, "r") as f:
        return json.load(f)

def save_sessions(sessions):
    with open(SESSION_INDEX, "w") as f:
        json.dump(sessions, f, indent=2)

def create_session(title, context_path):
    slug = title.lower().replace(" ", "-")
    session_dir = Path("bin/sessions") / slug
    session_dir.mkdir(parents=True, exist_ok=True)

    sessions = load_sessions()
    sessions[slug] = {
        "title": title,
        "context_path": str(Path(context_path).resolve()),
        "chat_file": f"{session_dir}/chat.json",
        "index_file": f"{session_dir}/context_index.json"
    }
    save_sessions(sessions)

    # Touch files
    Path(sessions[slug]["chat_file"]).write_text("[]")
    Path(sessions[slug]["index_file"]).write_text("[]")
    return slug
