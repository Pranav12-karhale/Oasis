# 🏝️ Oasis — Intelligent Health & Safety Advisory Platform for India

> AI-powered, real-time health and safety recommendations based on climate, disasters, weather, pollution, conflicts, and crises across India — accessible to **all** (including deaf and blind communities) in **13+ Indian languages** with full voice interaction.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-compose-blue.svg)](https://docs.docker.com/compose/)

---

## ✨ Features

- **🧠 Agentic RAG Pipeline** — LangGraph-powered self-correcting workflow with Gemini Pro
- **🌤️ Real-Time Data** — Weather (IMD), pollution (CPCB), disasters (NDMA), health alerts via custom MCP servers
- **🌍 13+ Indian Languages** — Hindi, Tamil, Bengali, Marathi, Telugu, and more via Bhashini API
- **🔊 Voice-First Accessibility** — Full voice interaction for blind/visually impaired users (ASR + TTS)
- **🤟 Deaf Accessibility** — Visual alerts, icons, vibration patterns, ISL support
- **📍 Location-Aware** — Personalized advisories based on your city, district, and state
- **🚨 Push Alerts** — Multi-channel disaster notifications (Push, WhatsApp, SMS, Email)
- **📱 Offline PWA** — Works without internet during disasters with cached advisories
- **📊 Full Observability** — OpenTelemetry + Grafana + Prometheus + Loki + Tempo
- **☸️ Cloud-Native** — Docker Compose + Kubernetes (Minikube) + Helm charts

## 🏗️ Architecture

```
User → Gateway (FastAPI) → LangGraph Orchestrator → MCP Servers (Weather/Pollution/Disaster)
                                    ↓                         ↓
                              RAG Engine (Qdrant)    Bhashini (Translation/TTS/ASR)
                                    ↓
                          Gemini Pro (Advisory Generation)
                                    ↓
                    Response (Text + Audio + Visual Alerts)
```

## 🚀 Quick Start

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed
- [Google Gemini API key](https://makersuite.google.com/app/apikey) (free with your subscription)

### 1. Clone & Setup
```bash
git clone https://github.com/your-username/Oasis.git
cd Oasis
cp .env.example .env
# Edit .env with your GEMINI_API_KEY
```

### 2. Start Everything
```bash
make up
# Or without make:
docker compose up -d
```

### 3. Access
| Service | URL |
|---------|-----|
| **Gateway API** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |
| **Frontend** | http://localhost:3001 |
| **Grafana** | http://localhost:3000 (admin/admin) |
| **Qdrant** | http://localhost:6333/dashboard |
| **MinIO** | http://localhost:9001 |

### 4. Try a Query
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Is air quality safe in Delhi today?",
    "location": {"city": "Delhi", "state": "Delhi"},
    "language": "hi"
  }'
```

## 💰 Cost: $0

Everything runs on free/open-source tools:
- **LLM**: Gemini Pro (your subscription) + Groq free tier (fallback)
- **Translation**: Bhashini API (free, Government of India)
- **Infrastructure**: Docker + Minikube (local)
- **Databases**: PostgreSQL, Redis, Qdrant, MinIO (all Docker)
- **Observability**: Grafana + Prometheus + Loki + Tempo (all open-source)

## 📁 Project Structure

```
Oasis/
├── services/          # Backend microservices (9 services)
├── mcp-servers/       # Custom MCP data integration (6 servers)
├── frontend/          # Next.js PWA frontend
├── knowledge-base/    # RAG documents
├── infrastructure/    # Docker, Helm, K8s configs
├── observability/     # Grafana, Prometheus, Loki, Tempo
└── docs/              # Documentation
```

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Google Gemini Pro + Groq (fallback) |
| Orchestration | LangGraph + LangChain |
| RAG | Qdrant + sentence-transformers |
| Backend | FastAPI (Python 3.12) |
| Translation | Bhashini API (IndicTrans2) |
| Frontend | Next.js 14+ (PWA) |
| Database | PostgreSQL + Redis |
| Observability | OpenTelemetry + Grafana + Prometheus + Loki + Tempo |
| Infrastructure | Docker + Kubernetes (Minikube) + Helm |

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.