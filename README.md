# 🦆 duck-assistant, your personal rubber duck!

A modular context- and session-based, local-first assistant built on top of local LLMs designed for personal use and hackability.  
Powered by Ollama, Python, and your own indexed notes or code.

## Features

- **Session-based context**: Create named sessions with specific folders of indexed content.
- **Chat history awareness**: Prompts include prior conversation turns for continuity.
- **Embeddings-powered retrieval**: Uses ChromaDB to find relevant documents from your session context.
- **Offline-capable**: No cloud calls required once Phi-3 and ChromaDB are set up.
- **Minimal CLI interface**: No GUI, no bloat, just you and your assistant.

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
* model_interface.py: Handles interaction with the local Phi-3 model

## Philosophy

Duck is built to be small, understandable, and extendable.
It’s meant to live alongside your notes, code, and workflow — not behind a paywall.

## Requirements

* Python 3.10+
* Ollama

## Roadmap (next steps)
* GUI
* Tag-aware or metadata-based indexing