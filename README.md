# Shoppy Agent

A full-stack, multimodal AI e-commerce assistant powered by an autonomous **LangGraph** agent running on local LLMs via **Ollama**, featuring voice search (**faster-whisper**), speech synthesis (**Kokoro TTS**), policy RAG (**PostgreSQL + pgvector**), and simulated checkout. 

100% self-hosted with zero paid API keys required.

---

## ✨ Features

- **Autonomous ReAct Agent**: Driven by LangGraph and Ollama (`qwen2.5:7b`) with 13 tool bindings for searching, comparing, cart updates, and orders.
- **Multimodal Voice I/O**: Real-time voice query transcription via local `faster-whisper` and natural speech output using `Kokoro TTS`.
- **Policy RAG**: Context-aware store policy search powered by `pgvector` embeddings.
- **Cart & Order Flow**: Live stock checking, cart management, and simulated order placement.
- **Modern UI**: Clean React 18 + Vite frontend with glassmorphism styling and live voice state indicators.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, Async SQLAlchemy, PostgreSQL 17 + `pgvector`
- **Agent & AI**: LangGraph, Ollama (`qwen2.5:7b`), `nomic-embed-text`
- **Voice Services**: `faster-whisper` (STT), `Kokoro TTS` (TTS)
- **Frontend**: React 18, Vite, Vanilla CSS

---

## 🚀 Quickstart

### 1. Clone & Setup Environment
```bash
git clone https://github.com/vasantha-kumar-s/shoppy-agent.git
cd shoppy-agent
cp .env.example .env
```

### 2. Run with Docker (Recommended)
```bash
# Start all services (PostgreSQL, Ollama, Whisper, Kokoro, Backend, Frontend)
docker compose up -d

# Pull the tool-calling LLM model
docker exec -it agentcart-ollama ollama pull qwen2.5:7b
```
Open `http://localhost` in your browser.

### 3. Local Development Setup

#### Backend
```bash
docker compose up -d postgres

cd backend
python -m venv venv
# Windows: .\venv\Scripts\Activate.ps1 | Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python -m seed.seed_data
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173`.

---

## 🧪 Testing

Run the backend test suite:
```bash
cd backend
pytest -v
```

---

## 📄 License
MIT
