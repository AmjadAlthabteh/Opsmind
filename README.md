# 🚨 AI Incident Commander

> **Production-grade incident management system powered by AI** — Detect, investigate, and coordinate responses to production incidents in real-time.

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)

**[Live Demo](#quick-start) • [Documentation](#documentation) • [Architecture](#architecture) • [Contributing](CONTRIBUTING.md)**

</div>

---

## 🎯 What Is This?

**AI Incident Commander** is a real-time incident management platform that combines traditional SRE workflows with AI-powered analysis. Think **PagerDuty + Datadog + ChatGPT** combined into one system.

### Why This Project?

Built to demonstrate **production-grade full-stack development** skills:
- ✅ **Backend Engineering** - FastAPI with async patterns
- ✅ **AI/ML Integration** - LangChain + RAG with vector databases
- ✅ **Real-time Systems** - WebSocket-powered live collaboration
- ✅ **Observability** - Prometheus metrics and monitoring
- ✅ **DevOps** - Docker, Docker Compose, deployment-ready

Perfect for showcasing skills to employers in **SRE**, **backend development**, and **AI systems engineering**.

---

## ✨ Features

### 🔍 **Intelligent Incident Detection**
- Ingest logs, metrics, and alerts from any source
- Automatic severity classification
- Real-time event correlation

### 🤖 **AI-Powered Analysis**
- **LangChain-based AI Commander** that investigates incidents
- **RAG (Retrieval-Augmented Generation)** using FAISS vector database
- Root cause analysis and remediation suggestions
- Similar incident detection from historical data

### 📊 **Real-Time Collaboration**
- **WebSocket-powered incident rooms** for live updates
- Timeline tracking with full audit trail
- Action tracking and assignment
- Live metrics and dashboards

### 🔧 **Production-Ready Features**
- Async job queue for background processing
- Rate limiting and security guardrails
- Prometheus metrics integration
- Full API documentation
- Docker and Kubernetes ready

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Frontend (React + Vite)                 │
│         Dashboard • Incident Rooms • Analytics          │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP + WebSocket
                        ▼
┌─────────────────────────────────────────────────────────┐
│              Backend (FastAPI + Python)                 │
│  ┌──────────────┬───────────────┬────────────────────┐ │
│  │   REST API   │   WebSocket   │   AI Commander     │ │
│  │              │   Live Rooms  │   (LangChain)      │ │
│  └──────────────┴───────────────┴────────────────────┘ │
└───────────────────────┬─────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌──────────────┐ ┌─────────────┐ ┌────────────────┐
│  Vector DB   │ │  Job Queue  │ │  Prometheus    │
│   (FAISS)    │ │   (Async)   │ │   (Metrics)    │
└──────────────┘ └─────────────┘ └────────────────┘
```

### Tech Stack

**Backend:**
- FastAPI (async Python web framework)
- LangChain (AI orchestration)
- FAISS (vector similarity search)
- Prometheus (observability)
- Pydantic (data validation)

**Frontend:**
- React 18
- Vite (build tool)
- WebSocket API
- Lucide Icons
- Custom CSS

**Infrastructure:**
- Docker & Docker Compose
- Nginx (production server)
- Prometheus + Grafana (monitoring)

---

## 🚀 Quick Start

### 🎯 Super Easy Start (Recommended for First-Time Users)

**Just want to try it? Run ONE command!**

```bash
# Linux/Mac
./quickstart.sh

# Windows
quickstart.bat
```

This will:
1. ✅ Auto-install all dependencies
2. ✅ Load demo incidents
3. ✅ Start backend & frontend
4. ✅ Open your browser automatically

**No OpenAI API key needed!** Works in demo mode with intelligent pattern-based analysis.

---

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API Key (optional - works without it in demo mode!)

### Option 1: Automated Setup (Easiest)

Run the setup script once:

```bash
# Linux/Mac
./setup.sh

# Windows
setup.bat
```

This installs everything! Then run:

```bash
# Linux/Mac
./quickstart.sh

# Windows
quickstart.bat
```

Done! 🎉

- Backend: **http://localhost:8000**
- Frontend: **http://localhost:3000**
- API Docs: **http://localhost:8000/api/docs**

### Option 2: Manual Setup

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python seed_data.py
python run.py
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Option 3: Docker Compose

```bash
# Set environment variables
export OPENAI_API_KEY=your_api_key_here

# Start all services
docker-compose up -d
```

Services:
- Frontend: **http://localhost:80**
- Backend: **http://localhost:8000**
- Prometheus: **http://localhost:9090**
- Grafana: **http://localhost:3001**

### Option 4: Makefile

```bash
make install  # Install dependencies
make seed     # Load demo data
make dev      # Instructions for running dev servers
make docker-up  # Start with Docker
```

---

## 📖 Documentation

- **[API Documentation](docs/API.md)** - Complete REST API reference
- **[Architecture Guide](docs/ARCHITECTURE.md)** - System design and data flow
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Docker, K8s, AWS, GCP deployment
- **[Troubleshooting Guide](TROUBLESHOOTING.md)** - Common issues and solutions
- **[Contributing](CONTRIBUTING.md)** - How to contribute

---

## 🎯 Use Cases

- **Production Incident Management** - Track and resolve outages
- **Automated Root Cause Analysis** - AI-powered investigation
- **Knowledge Base** - Learn from past incidents
- **Real-Time Collaboration** - Coordinate team responses
- **Postmortem Generation** - Automated incident reports

---

## 📊 Features Showcase

### Dashboard
- Real-time incident stats (total, active, resolved, MTTR)
- Recent incidents list with severity badges
- Auto-refresh every 30 seconds

### Incident Detail View
- Full incident timeline
- AI-suggested remediation actions
- Live event stream (logs, metrics, alerts)
- Real-time WebSocket updates
- Status management workflow

### AI Commander
- Analyzes incidents using GPT-4
- Searches past incidents via vector similarity
- Suggests prioritized actions
- Generates postmortem reports

---

## 🔒 Security

Current security features:
- ✅ Rate limiting (SlowAPI)
- ✅ CORS configuration
- ✅ Input validation (Pydantic)
- ✅ WebSocket connection management

**For production**, add:
- Authentication (JWT/OAuth)
- Authorization (RBAC)
- Secrets management (Vault)
- TLS/SSL encryption

---

## 📈 Observability

### Prometheus Metrics

- `incidents_created_total` - Total incidents by severity/source
- `incidents_resolved_total` - Resolved incidents count
- `incident_duration_seconds` - Time to resolution
- `active_incidents` - Current open incidents
- `ai_analysis_duration_seconds` - AI processing time
- `http_requests_total` - API request counts
- `websocket_connections` - Active connections

Access metrics: **http://localhost:8000/metrics**

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test
```

---

## 📝 Development Workflow

This project demonstrates professional development practices:

✅ **30+ incremental commits** showing development progression
✅ **Clean architecture** with separation of concerns
✅ **Comprehensive documentation** (API, architecture, deployment)
✅ **Docker-ready** with multi-stage builds
✅ **Production patterns** (async jobs, rate limiting, observability)
✅ **Type safety** (Pydantic models, clear interfaces)

---

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📜 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

## 🎓 Learning Resources

This project demonstrates:
- RESTful API design
- WebSocket real-time communication
- AI/ML integration with LLMs
- Vector databases and semantic search
- Async Python programming
- React hooks and state management
- Docker containerization
- Prometheus monitoring

---

## 💼 Resume Bullet Point

> Built a production-grade AI Incident Commander platform using FastAPI, LangChain, React, and FAISS vector database with WebSocket real-time updates, async job processing, Prometheus observability, and comprehensive API documentation — demonstrating full-stack development from architecture to deployment.

---

## 📫 Contact

**Amjad Althabteh**
GitHub: [@AmjadAlthabteh](https://github.com/AmjadAlthabteh)

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Built with ❤️ for learning and demonstration purposes

</div>
