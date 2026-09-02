# JARVIS — Modular Desktop AI Assistant

Phase 1 is a working conversational backend with Groq integration, bounded conversation context, real-time WebSocket events, and a provider abstraction. Voice, system control, persistent memory, and the Electron UI are deliberately deferred to later phases.

## Architecture

`REST/WebSocket → Orchestrator → LLMProvider → Groq` with a separate event bus and memory facade. See [ARCHITECTURE.md](ARCHITECTURE.md).

## Install and run

1. Install Python 3.12 or later.
2. Create and activate a virtual environment from `backend`:

   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. Copy `backend/.env.example` to `backend/.env`, then set `GROQ_API_KEY` and optionally select a Groq model.
4. From the repository root, run:

   ```powershell
   python scripts/start_backend.py
   ```

5. Open `http://127.0.0.1:8000/docs`. The health endpoint is `GET /api/v1/health`; send a command with `POST /api/v1/commands` and `{"message":"Hello"}`. WebSocket events are available at `ws://127.0.0.1:8000/ws/events`.

The React/Electron desktop client is scheduled for Phase 12; the existing frontend can still be installed independently with `npm install` from `frontend` when that phase begins.

## Verification

From `backend`, run `pytest` and `ruff check app tests`.

## Extensibility and security

All model calls go through `app/ai/groq_client.py` and the `LLMProvider` protocol. The orchestrator does not execute system commands. Later tool modules must register metadata, use permission checks, require confirmation for unsafe actions, and write audit events.

## Later phases

The directory layout already reserves modules for voice, tools, memory, vision, automation, security, and the React/Electron desktop client. Only Phase 1 functionality is implemented now, as requested.
