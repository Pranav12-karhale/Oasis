<div align="center">
  <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/React-Dark.svg" height="80" alt="React" />
  <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Python-Dark.svg" height="80" alt="Python" />
  <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Docker.svg" height="80" alt="Docker" />
  <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Kubernetes.svg" height="80" alt="Kubernetes" />
  <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Grafana-Dark.svg" height="80" alt="Grafana" />
  
  <br />
  <br />
  
  <h1>🏝️ Oasis</h1>
  
  <p>
    <b>Intelligent Health & Safety Advisory Platform for India</b>
  </p>
  
  <p>
    <i>AI-powered, real-time health and safety recommendations based on climate, disasters, weather, pollution, conflicts, and crises across India — accessible to <b>all</b> (including deaf and blind communities) in <b>13+ Indian languages</b> with full voice interaction.</i>
  </p>

  <p>
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License" />
    <img src="https://img.shields.io/badge/Python-3.12-blue.svg" alt="Python" />
    <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status" />
  </p>
</div>

---

<details>
<summary><h2>✨ Why Oasis? (Click to Expand)</h2></summary>
<br>

Oasis bridges the gap between critical public health data and the diverse population of India. By leveraging advanced Language Models, Agentic Workflows, and Multi-Modal accessibility, it transforms raw metrics into actionable, life-saving advice for everyone—regardless of language barriers or physical abilities.

- 🧠 **Agentic RAG Pipeline**: LangGraph-powered self-correcting workflow with Gemini Pro.
- 🌤️ **Real-Time Data**: Integrates Weather (IMD), Pollution (CPCB), and Disasters (NDMA).
- 🌍 **13+ Indian Languages**: Seamless translation via the Bhashini API.
- 🔊 **Voice-First Accessibility**: Full ASR and TTS interaction for blind/visually impaired users.
- 🤟 **Deaf Accessibility**: Visual alerts, iconography, vibration patterns, and ISL support.
- 📍 **Location-Aware**: Personalized advisories tailored to the user's precise geography.

</details>

<details open>
<summary><h2>🏗️ System Architecture</h2></summary>
<br>

Oasis is designed as a cloud-native, microservices-driven platform. It uses a LangGraph orchestrator to coordinate various independent MCP (Model Context Protocol) servers that fetch real-time public data.

```mermaid
graph TD
    classDef user fill:#64748b,stroke:#000,color:#fff,stroke-width:2px;
    classDef gateway fill:#0284c7,stroke:#000,color:#fff,stroke-width:2px;
    classDef brain fill:#7e22ce,stroke:#000,color:#fff,stroke-width:2px;
    classDef data fill:#059669,stroke:#000,color:#fff,stroke-width:2px;
    classDef frontend fill:#c026d3,stroke:#000,color:#fff,stroke-width:2px;

    U([👤 User]):::user <-->|Voice, Text, Gestures| F[🖥️ Next.js PWA Frontend]:::frontend
    F <-->|REST / WebSockets| G[🚪 API Gateway <br> FastAPI]:::gateway
    
    G -->|Dispatch Request| O[🧠 LangGraph Orchestrator]:::brain
    
    subgraph Data & Context Gathering
        O -->|Query Real-time Data| MCP[🔌 MCP Servers]:::data
        MCP -.-> W[🌤️ Weather MCP]
        MCP -.-> P[🌫️ Pollution MCP]
        MCP -.-> D[🚨 Disaster MCP]
        MCP -.-> M[🏥 Health & News MCPs]
        
        O -->|Semantic Search| RAG[(📚 Qdrant RAG Engine)]:::data
    end
    
    subgraph Core Processing
        O -->|Synthesize Context| LLM[🤖 Gemini Pro / Groq]:::brain
        O -->|Accessibility formatting| AE[♿ Accessibility Engine]:::brain
        LLM -->|Translate & Audio| T[🌍 Translation & Voice Services]:::brain
    end
    
    T -.-> Bhashini[Bhashini API]
    AE --> G
    T --> G
```
</details>

<details open>
<summary><h2>🔄 Dynamic Workflows</h2></summary>
<br>

The request lifecycle is managed by an intelligent graph that ensures real-time accuracy and multi-modal delivery.

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Gateway as API Gateway
    participant Orch as LangGraph Orchestrator
    participant MCP as Data MCPs (Weather, etc.)
    participant RAG as Qdrant Vector DB
    participant LLM as Gemini Pro Engine
    participant Acc as Accessibility/Voice
    
    User->>Gateway: Query "Is air quality safe in Delhi?" (Lang: Hindi)
    Gateway->>Orch: Init Context Graph
    
    par Real-Time Data Collection
        Orch->>MCP: Query Pollution & Weather
        MCP-->>Orch: Return AQI (e.g. 400 - Severe)
    and RAG Retrieval
        Orch->>RAG: Fetch asthma/health guidelines
        RAG-->>Orch: Guideline Documents
    end
    
    Orch->>LLM: Synthesize Advisory Prompt
    LLM-->>Orch: Generate Health Warning
    
    Orch->>Acc: Process for Output Language & Modality
    Acc-->>Orch: Hindi Text + TTS Audio + Visual Alert
    
    Orch->>Gateway: Final Multi-Modal Payload
    Gateway-->>User: Present Alert (Push, Audio, Screen)
```
</details>

<details>
<summary><h2>🛠️ Tech Stack & Ecosystem</h2></summary>
<br>

| Domain | Technologies |
| :--- | :--- |
| **Frontend** | React, Next.js 14+ (PWA) |
| **Backend** | Python 3.12, FastAPI, LangChain, LangGraph |
| **AI / LLMs** | Google Gemini Pro, Groq, Sentence Transformers |
| **Data Integration** | MCP (Model Context Protocol) Servers |
| **Databases** | PostgreSQL, Redis, Qdrant (Vector DB) |
| **Translation & Speech** | Bhashini API (IndicTrans2) |
| **Observability** | OpenTelemetry, Grafana, Prometheus, Loki, Tempo |

</details>

<details>
<summary><h2>📁 Project Structure</h2></summary>
<br>

```text
Oasis/
├── 🖥️ frontend/                # Next.js PWA frontend
├── ⚙️ services/                # Microservices architecture
│   ├── gateway/               # Central API Gateway
│   ├── orchestrator/          # LangGraph coordination
│   ├── ml-pipeline/           # Machine learning models
│   ├── accessibility-engine/  # ARIA & sensory adaptations
│   ├── voice/                 # ASR/TTS processors
│   ├── translation/           # Bhashini wrappers
│   ├── rag-engine/            # Qdrant querying
│   ├── data-ingestion/        # Batch data processing
│   ├── auth/                  # Authentication service
│   └── notification/          # Multi-channel alerts
├── 🔌 mcp-servers/             # Model Context Protocol servers
│   ├── weather-mcp/
│   ├── pollution-mcp/
│   ├── disaster-mcp/
│   ├── health-mcp/
│   ├── news-mcp/
│   └── geo-mcp/
├── 📊 observability/           # Grafana & Prometheus dashboards
└── 📚 knowledge-base/          # Source documents for RAG
```
</details>
