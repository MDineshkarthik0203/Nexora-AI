# Nexora-AI (AgentForge)

> **Autonomous Multi-Agent AI Engineering Copilot** built with **LangGraph**, **Django REST Framework**, and **React + Vite**.

---

## 🌟 Overview

**Nexora-AI (AgentForge)** is an intelligent multi-agent engineering copilot designed to autonomously plan, research, retrieve private organizational knowledge, generate self-healing executable Python code, review technical correctness, and collaborate with humans through Human-in-the-Loop (HITL) workflows.

---

## 🏗️ System Architecture

```text
React Frontend (Vite)
        │
        │ HTTP (JSON)
        ▼
Django REST API (/api/chat/, /api/human-review/)
        │
        ▼
   LangGraph Orchestrator
        │
        ├── 1. Supervisor Agent (Routes query: Chat, Research, RAG, Coding, Multi-Agent)
        ├── 2. Planning Agent   (Decomposes tasks & plans execution sequence)
        ├── 3. Research Agent   (Live web search via Tavily API)
        ├── 4. RAG Agent        (Semantic retrieval with Chroma + Mistral Embeddings + CrossEncoder)
        ├── 5. Coding Agent     (Code generation & self-healing execution loop)
        ├── 6. Code Execution   (Subprocess sandbox with automated error feedback)
        ├── 7. Reviewer Agent   (Validates logic, correctness, and execution outputs)
        ├── 8. Human Review     (HITL interrupt: pause for approval or feedback)
        └── 9. Writer Agent     (Synthesizes comprehensive markdown technical report)
```

### Specialized Agents

| Agent | Responsibility | Tools / Providers |
| :--- | :--- | :--- |
| **Supervisor** | Classifies requests into optimal execution route | ChatGroq |
| **Planner** | Generates multi-step plans and determines agent order | ChatGroq |
| **Research** | Performs external web intelligence gathering | Tavily Search API |
| **RAG** | Retrieves private documents with dense reranking | Mistral Embeddings, ChromaDB, Cross-Encoder |
| **Coding** | Generates Python code and fixes errors iteratively | Python runner, ChatGroq |
| **Code Executor** | Runs Python scripts with timeout and stdout/stderr capture | `sys.executable` Subprocess sandbox |
| **Reviewer** | Assesses code and solution validity, flags revisions | ChatGroq |
| **Human Review** | Pauses workflow for human sign-off (Approve/Revise) | LangGraph `interrupt()` |
| **Writer** | Compiles structured final documentation report | ChatGroq |

---

## 📁 Project Structure

```text
Nexora-AI/
├── backend/                  # Django REST API backend
│   ├── api/                  # API endpoints, serializers, services
│   ├── config/               # Django configuration & settings
│   └── manage.py             # Django management CLI
├── data/                     # Knowledge base documents for RAG
│   ├── architecture.txt      # System architecture info
│   ├── agent_design.txt      # Detailed agent responsibilities
│   └── project_requirements.txt
├── frontend/                 # React 18 + Vite modern UI
│   ├── src/
│   │   ├── components/       # UI Components
│   │   ├── services/         # Django API client (agentforge.js)
│   │   ├── App.jsx           # Main copilot workspace & chat UI
│   │   └── App.css           # Styling
│   └── package.json
├── src/
│   └── agentforge/           # Core LangGraph multi-agent package
│       ├── graph.py          # StateGraph definition and compilation
│       ├── nodes.py          # Agent node logic and LLM prompts
│       ├── router.py         # Conditional edge routing logic
│       ├── state.py          # TypedDict AgentState definition
│       └── tools/            # Web search, RAG, and Code execution tools
├── tests/                    # Testing scripts
│   ├── ingest_data.py        # Ingests data/ into Chroma vector store
│   ├── test_agent.py         # End-to-end multi-agent test
│   └── test_hitl.py          # Human-in-the-loop interactive test
├── main.py                   # Project entrypoint CLI
├── pyproject.toml            # Python packaging and dependencies
├── requirements.txt          # Python dependencies list
└── uv.lock                   # Lockfile for reproducible builds
```

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python**: Version 3.11 to 3.13
- **Node.js**: Version 18+ and `npm`
- **API Keys**:
  - [Groq API Key](https://console.groq.com/keys) (LLM inference)
  - [Tavily API Key](https://app.tavily.com/) (Web search)
  - [Mistral AI API Key](https://console.mistral.ai/) (Embeddings for RAG)

---

### 2. Configure Environment Variables
Copy `.env.example` to `.env` in the project root:

```bash
cp .env.example .env
```

Edit `.env` and fill in your API keys:
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
TAVILY_API_KEY=your_tavily_api_key_here
MISTRAL_API_KEY=your_mistral_api_key_here
```

---

### 3. Backend Setup

You can use either `uv` or standard `pip`:

#### Using `uv`:
```bash
uv sync
```

#### Or using `pip` and virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

#### Run Database Migrations:
```bash
python backend/manage.py migrate
```

#### Start the Django Backend:
```bash
python backend/manage.py runserver
```
The backend API is now running at `http://127.0.0.1:8000`.

---

### 4. Frontend Setup

From the `frontend` folder:
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser to interact with Nexora-AI.

---

### 5. Ingest Knowledge Base (Optional for RAG)
To index the documents in `data/` into Chroma vector store:
```bash
python tests/ingest_data.py
```

---

## 🧪 Testing

### Test Standalone Multi-Agent Pipeline:
```bash
python tests/test_agent.py
```

### Test Interactive Human-in-the-Loop (HITL):
```bash
python tests/test_hitl.py
```

---

## 📡 API Reference

### `GET /api/health/`
Checks API health status.
```json
{
  "status": "ok",
  "service": "AgentForge Django API"
}
```

### `POST /api/chat/`
Sends a query to the multi-agent system.
```json
{
  "question": "Write a python function to compute fibonacci numbers",
  "session_id": "session-123"
}
```

### `POST /api/human-review/`
Submits human approval or revision instructions to resume the paused workflow.
```json
{
  "session_id": "session-123",
  "action": "approve",
  "feedback": ""
}
```
Or to request a revision:
```json
{
  "session_id": "session-123",
  "action": "revise",
  "feedback": "Optimize space complexity to O(1)"
}
```

---

## 📄 License
MIT License.
