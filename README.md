# 🦆 duck-assistant, your personal rubber duck!

A modular context- and session-based, local-first assistant built on top of local LLMs designed for personal use and hackability.  
Powered by Ollama, Python, and your own indexed notes or code.

Ever wished you didn't need to copy paste (and anonymize) your data into ChatGPT and be told your prompt was too long?
Well, then duck-assistant is for you: 
* It's local, so no worries about your data being shared with whoever.
* You control the context, so it'll ingest your notes for relevant answers.
* The limit of context size goes as far as your hardware and Ollama can handle.
* In the future, context will be optimized/summarized for improved performance and size limits.

## Features

- **Session-based context**: Create named sessions with specific folders of indexed content.
- **Chat history awareness**: Prompts include prior conversation turns for continuity.
- **Embeddings-powered retrieval**: Uses ChromaDB to find relevant documents from your session context.
- **Offline-capable**: No cloud calls required once your Ollama model(s) set up.
- **Optional CLI interface**: Just you and your assistant.

## Quick Start

Install the application: 
* With `pip`: `pip install git+https://github.com/Z3R-0/duck-assistant`.
* Through the [Releases](https://github.com/Z3R-0/duck-assistant/releases) page.

Set your preferred model *(default: phi3)* and Ollama port in `config.json` and then:

```bash
# List sessions
duck --list

# Create a new session (indexing a folder as context)
duck --new "Project X" ./my-notes/project-x

# Chat with a session
duck --session project-x "What's the architecture of this project?"

# Clear cached embeddings for a session
duck --clear-cache project-x
```

## Project Structure

* cli.py: CLI entry point
* session_manager.py: Handles creating and loading sessions
* indexer.py: Handles context indexing (with ChromaDB) and querying
* chat_engine.py: Runs inference with context + history
* model_interface.py: Handles interaction with the local Ollama model

## Philosophy

Duck is built to be small, understandable, and extendable.
It’s meant to live alongside your notes, code, and workflow — not behind a paywall.

## Requirements

* Ollama, for the actual AI responses
* Python 3.10+ (if running through `pip`)

## Roadmap (next steps)
* GUI
* Automated context size optimization
* Tag-aware or metadata-based indexing