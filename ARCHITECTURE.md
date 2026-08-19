# 🏗️ AgentCart System Architecture

This document provides an in-depth technical overview of the **AgentCart** architecture, data flow patterns, and component interactions.

---

## 1. High-Level System Architecture

AgentCart is structured into four primary layers:
1. **Presentation Layer**: Single Page Application built with React 18 and Vite.
2. **API & Service Gateway**: FastAPI async web framework with dependency injection and Pydantic validation.
3. **Agentic AI & Knowledge Layer**: LangGraph `StateGraph` state machine with native tool-calling, anti-hallucination prompt control, and RAG policy retriever.
4. **Data & Inference Layer**: PostgreSQL 17 with `pgvector`, local Ollama LLM server, `faster-whisper` STT, and `Kokoro TTS`.

```
┌─────────────────────────────────────────────────────────────┐
│                      React 18 Frontend                      │
│   (Catalog UI, Chat UI, Voice Controls, Live Health Dots)   │
└──────────────┬───────────────────────────────▲──────────────┘
               │                               │
               │ HTTP / JSON                   │ Audio Stream / JSON
               ▼                               │
┌──────────────────────────────────────────────┴──────────────┐
│                    FastAPI Backend Gateway                  │
│                                                             │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────────┐  │
│  │ Products API  │ │   Cart API    │ │    Orders API     │  │
│  └───────┬───────┘ └───────┬───────┘ └─────────┬─────────┘  │
│          │                 │                   │            │
│  ┌───────▼─────────────────▼───────────────────▼─────────┐  │
│  │              Service Layer (Business Logic)           │  │
│  └───────┬───────────────────────────────────────────────┘  │
│          │                                                  │
│  ┌───────▼───────────────────────────────────────────────┐  │
│  │                 LangGraph Agent Layer                 │  │
│  │  - StateGraph ReAct Loop                              │  │
│  │  - 13 Structured Tools (Product, Cart, Order, RAG)    │  │
│  │  - Anti-Hallucination Directives                      │  │
│  └───────┬───────────────────┬───────────────────┬───────┘  │
└──────────┼───────────────────┼───────────────────┼──────────┘
           │                   │                   │
           ▼                   ▼                   ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  PostgreSQL 17   │ │   Ollama LLM     │ │  Voice Services  │
│    + pgvector    │ │  (qwen2.5:7b)    │ │ - faster-whisper │
│                  │ │                  │ │ - Kokoro TTS     │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

---

## 2. End-to-End Multimodal Sequence Diagram

The diagram below details the execution flow when a user speaks a voice command:

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Frontend as React Frontend
    participant FastAPI as FastAPI Backend
    participant Whisper as faster-whisper (STT)
    participant LangGraph as LangGraph Agent
    participant Ollama as Ollama (Local LLM)
    participant Tools as Tool Execution Layer
    participant DB as PostgreSQL (pgvector)
    participant Kokoro as Kokoro TTS

    User->>Frontend: 🎙️ Speaks query ("Find headphones under ₹5,000")
    Frontend->>FastAPI: POST /api/voice/transcribe (audio/webm blob)
    FastAPI->>Whisper: POST /asr (audio payload)
    Whisper-->>FastAPI: Returns transcript ("Find headphones under ₹5,000")
    FastAPI-->>Frontend: Returns JSON transcript
    
    Frontend->>FastAPI: POST /api/chat { message: "Find headphones under ₹5,000" }
    FastAPI->>DB: Load recent conversation history
    FastAPI->>LangGraph: ainvoke(AgentState with history + new message)
    
    LangGraph->>Ollama: Inference with System Prompt + 13 Tool Schemas
    Ollama-->>LangGraph: Tool Call: search_products(category='headphones', max_price=5000)
    
    LangGraph->>Tools: Execute search_products()
    Tools->>DB: Async SQLAlchemy SELECT with filters
    DB-->>Tools: Returns matching products (e.g. Rockerz 450 Pro ₹1,499)
    Tools-->>LangGraph: ToolMessage(observation result)
    
    LangGraph->>Ollama: Second-order inference with Tool observation
    Ollama-->>LangGraph: Final synthesis ("I found the boAt Rockerz 450 Pro...")
    
    LangGraph->>DB: Persist user message and assistant reply
    LangGraph-->>FastAPI: ChatResponse (text + tool_activities + products)
    
    FastAPI->>Kokoro: POST /v1/audio/speech (synthesize final text)
    Kokoro-->>FastAPI: audio/mpeg byte stream
    FastAPI-->>Frontend: JSON ChatResponse + Audio playback
    Frontend->>User: 🔊 Speaks answer + Displays interactive product cards
```

---

## 3. Database Entity Relationship Model

```mermaid
erDiagram
    USERS ||--o{ ADDRESSES : has
    USERS ||--o| CARTS : owns
    USERS ||--o{ ORDERS : places
    USERS ||--o{ CONVERSATIONS : starts
    USERS ||--o{ PRODUCT_REVIEWS : writes

    CATEGORIES ||--o{ PRODUCTS : categorizes
    PRODUCTS ||--o| INVENTORY : has_stock
    PRODUCTS ||--o{ CART_ITEMS : in_cart
    PRODUCTS ||--o{ ORDER_ITEMS : in_order
    PRODUCTS ||--o{ PRODUCT_REVIEWS : has_reviews

    CARTS ||--o{ CART_ITEMS : contains
    ORDERS ||--o{ ORDER_ITEMS : contains
    ORDERS ||--o| ADDRESSES : ships_to
    CONVERSATIONS ||--o{ MESSAGES : stores
```

---

## 4. State Management in LangGraph

The agent's state is modeled with the `AgentState` TypedDict:

```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    user_id: int
    conversation_id: Optional[int]
    tool_activities: List[Dict[str, Any]]
    extracted_products: List[Dict[str, Any]]
```

- **`add_messages` reducer**: Appends messages in chronological order, allowing tool responses (`ToolMessage`) to feed seamlessly back into the reasoning loop without overwriting conversational history.
- **`tools_condition` router**: Evaluates whether the LLM's response contains tool calls. If so, it routes execution to `ToolNode`; if not, it transitions to `END`.
