# Architecture

Phase 1 uses a thin FastAPI composition root. Requests enter the API router, pass to the `JarvisOrchestrator`, which combines bounded short-term conversation memory with an `LLMProvider`. The initial `GroqClient` is the provider implementation. The orchestrator emits typed events through `EventBus`, and the WebSocket endpoint broadcasts them to connected UI clients.

Future capabilities remain isolated behind provider and tool boundaries: voice providers, tool registry, persistent memory, vision, scheduling, and platform-specific computer controllers will not be placed in `main.py`.

Security-sensitive system actions are intentionally not introduced in Phase 1.
