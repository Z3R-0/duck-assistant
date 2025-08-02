import sys
from chat_engine import chat_with_context
from indexer import clear_session_cache
from session_manager import load_sessions, create_session

def print_usage():
    print("Usage:")
    print("  duck --list")
    print("      List all sessions.")
    print("  duck --new <name> <path_to_context>")
    print("      Create a new session (will return the slug).")
    print("  duck --session <slug> <prompt>")
    print("      Ask a question in the given session.")
    print("  duck --clear-cache <slug>")
    print("      Clear cached embeddings for a session")

def main():
    args = sys.argv[1:]

    if not args:
        print_usage()
        return

    if args[0] == "--list":
        sessions = load_sessions()
        if not sessions:
            print("No sessions found.")
            return
        for slug, s in sessions.items():
            print(f"{slug}: {s['title']} -> {s['context_path']}")
        return

    if args[0] == "--new" and len(args) == 3:
        name, context_path = args[1], args[2]
        slug = create_session(name, context_path)
        print(f"Session created: {slug}")
        return
    
    if args[0] == "--clear-cache" and len(args) == 2:
        slug = args[1]
        clear_session_cache(slug)
        return

    if args[0] == "--session" and len(args) >= 3:
        slug = args[1]
        prompt = " ".join(args[2:])
        sessions = load_sessions()
        if slug not in sessions:
            print(f"No session found with slug '{slug}'.")
            return
        reply = chat_with_context(slug, prompt)
        print(reply)
        return

    print_usage()

if __name__ == "__main__":
    main()
