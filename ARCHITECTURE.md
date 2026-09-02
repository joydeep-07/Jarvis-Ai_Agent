# Architecture

Phase 1 uses a thin FastAPI composition root. Requests enter the API router, pass to the `JarvisOrchestrator`, which combines bounded short-term conversation memory with an `LLMProvider`. The initial `GroqClient` is the provider implementation. The orchestrator emits typed events through `EventBus`, and the WebSocket endpoint broadcasts them to connected UI clients.

Future capabilities remain isolated behind provider and tool boundaries: voice providers, tool registry, persistent memory, vision, scheduling, and platform-specific computer controllers will not be placed in `main.py`.

## Voice pipeline (Phase 2)

The optional local microphone captures short PCM chunks and applies local VAD to find the phrase boundary. Audio is retained only in memory, then sent to the selected `SpeechToTextProvider`. `VoiceManager` emits lifecycle events, optionally verifies/removes the wake word, and exposes `TextToSpeechProvider` output as WAV bytes. The initial providers use Groq-compatible speech endpoints; replacing either provider does not affect the API or orchestrator.

## Tool execution (Phase 3)

The model requests tools through the provider's structured function-call output. `JarvisOrchestrator` limits execution to six iterations and only routes calls through `ToolRegistry`. Tools declare their JSON schema, permission level, confirmation requirement, and executor. The first tools are calculation, current time, and configured application aliases. No LLM-produced shell command can be executed.

## Computer control (Phase 4)

`ComputerController` keeps keyboard and pointer operations behind a portable contract, with a Windows implementation running PyAutoGUI operations in worker threads. Window control and browser navigation are separate modules. All input controls are low-risk registered tools; browser navigation only accepts HTTP(S) URLs. The MongoDB connection factory is lazy and will underpin persistent memory in Phase 5 without preventing offline startup.

Security-sensitive system actions are intentionally not introduced in Phase 1.
