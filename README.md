# AI Incident Commander

A real-time AI system that detects, investigates, and coordinates responses to production incidents.

## Features

- **Real-time Incident Detection**: Ingests logs, metrics, and alerts
- **AI Incident Commander**: LangChain-powered agent that investigates and coordinates responses
- **RAG-based Knowledge**: Vector database stores past incidents, runbooks, and logs
- **Async Deep Analysis**: Background jobs for root cause analysis and postmortem generation
- **Live Incident Rooms**: WebSocket-powered real-time collaboration
- **Observability**: Full metrics, logging, and tracing
- **Rate Limiting**: Protection against alert floods and abuse

## Architecture

### Backend
- **FastAPI**: Async REST API and WebSocket server
- **LangChain**: AI agent orchestration
- **FAISS**: Vector database for RAG
- **AsyncIO**: Job queue for background tasks
- **Prometheus**: Metrics and observability

### Frontend
- **React**: Modern, responsive UI
- **TypeScript**: Type-safe frontend code
- **WebSocket**: Real-time updates
- **Recharts**: Metrics visualization

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Tech Stack

- Python 3.11+
- FastAPI
- LangChain
- FAISS (Vector DB)
- React + TypeScript
- WebSockets
- Prometheus

## Use Cases

- Production incident management
- Automated root cause analysis
- Knowledge base for incident resolution
- Real-time collaboration during outages
- Postmortem generation
