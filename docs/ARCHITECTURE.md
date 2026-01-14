# System Architecture

## Overview

AI Incident Commander is a real-time incident management platform that combines traditional SRE workflows with AI-powered analysis and recommendations.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                        │
│  - Dashboard                                                │
│  - Incident Details                                         │
│  - Real-time Updates (WebSocket)                           │
└───────────┬─────────────────────────────────────────────────┘
            │ HTTP/WS
            ▼
┌─────────────────────────────────────────────────────────────┐
│                  API Layer (FastAPI)                        │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │ REST API     │ WebSocket    │ Metrics Endpoint        │ │
│  │ - Incidents  │ - Live Room  │ - Prometheus            │ │
│  │ - Events     │              │                         │ │
│  │ - Actions    │              │                         │ │
│  └──────────────┴──────────────┴──────────────────────────┘ │
└───────────┬─────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Business Logic Layer                      │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │ AI Commander │ Job Queue    │ Storage Manager         │ │
│  │ - Analysis   │ - Async Jobs │ - In-Memory DB          │ │
│  │ - RAG        │ - Postmortem │ - Vector Store          │ │
│  └──────────────┴──────────────┴──────────────────────────┘ │
└───────────┬─────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                             │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │ Vector DB    │ In-Memory    │ Observability           │ │
│  │ (FAISS)      │ Storage      │ (Prometheus)            │ │
│  └──────────────┴──────────────┴──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Components

### Frontend (React + TypeScript)

**Location:** `frontend/src/`

- **Single Page Application** with React Router
- **Real-time updates** via WebSocket connections
- **Responsive UI** with custom CSS and Lucide icons
- **State Management** using React hooks

**Key Pages:**
- Dashboard: Overview of all incidents with stats
- Incident Detail: Full incident view with timeline, actions, events
- Create Incident: Form for manual incident creation

### Backend (FastAPI + Python)

**Location:** `backend/app/`

#### API Layer (`api/`)
- **REST endpoints** for CRUD operations
- **WebSocket server** for real-time incident rooms
- **Rate limiting** using SlowAPI
- **CORS** middleware for cross-origin requests

#### AI Layer (`ai/`)
- **AI Commander**: LangChain-powered incident analyst
- **RAG System**: Vector search for past incidents and runbooks
- **Analysis Pipeline**: Automated root cause analysis

#### Job Queue (`jobs/`)
- **Async processing** for long-running tasks
- **Postmortem generation**
- **Deep incident analysis**

#### Storage (`db/`)
- **In-Memory Storage**: Fast, ephemeral data storage
- **Vector Store**: FAISS-based semantic search
- **Metadata Management**: Incident timeline, events, actions

#### Observability (`observability/`)
- **Prometheus Metrics**: Incident counts, MTTR, AI performance
- **Custom Instrumentation**: Request tracing, error tracking

## Data Flow

### Creating an Incident

1. User submits incident via frontend form
2. API receives POST request to `/api/incidents/`
3. Incident model validated with Pydantic
4. Stored in in-memory database
5. Timeline entry created
6. Metrics updated (incidents_created counter)
7. Background job triggered for AI analysis
8. WebSocket notifies connected clients
9. Frontend updates in real-time

### AI Analysis Pipeline

1. Incident created/updated
2. AI Commander invoked asynchronously
3. Context gathered:
   - Incident details
   - Recent events
   - Similar past incidents (via vector search)
4. LLM generates analysis (GPT-4)
5. Actions suggested and stored
6. Timeline updated with AI insights
7. WebSocket broadcasts updates

### Real-time Incident Room

1. User navigates to incident detail page
2. WebSocket connection established to `/ws/incidents/{id}`
3. User joins incident room
4. All updates broadcast to room participants:
   - Status changes
   - New events
   - AI analysis results
   - User comments
5. Connection maintained for live collaboration

## Tech Stack Details

### Backend
- **FastAPI**: Modern, async Python web framework
- **Pydantic**: Data validation and serialization
- **LangChain**: LLM orchestration and RAG
- **FAISS**: Vector similarity search
- **Prometheus Client**: Metrics instrumentation
- **SlowAPI**: Rate limiting middleware

### Frontend
- **React 18**: Component-based UI
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **WebSocket API**: Real-time communication
- **Recharts**: Data visualization
- **Lucide Icons**: Icon library
- **Vite**: Build tool and dev server

## Scalability Considerations

### Current Architecture
- In-memory storage (single instance)
- Synchronous AI analysis
- WebSocket connections per instance

### Production Enhancements
1. **Replace in-memory storage** with PostgreSQL/MongoDB
2. **Add Redis** for WebSocket pub/sub across instances
3. **Queue system** (Celery/RQ) for async jobs
4. **API Gateway** with load balancing
5. **Distributed vector store** (Pinecone, Weaviate)
6. **Horizontal scaling** of API instances

## Security

### Current Measures
- Rate limiting per IP
- CORS configuration
- Input validation (Pydantic)
- WebSocket connection management

### Production Requirements
- Authentication (JWT, OAuth)
- Authorization (RBAC)
- API key management
- Secrets management (Vault)
- TLS/SSL encryption
- Audit logging

## Monitoring & Observability

### Metrics Exposed
- `incidents_created_total`: Total incidents by severity/source
- `incidents_resolved_total`: Resolved incidents by severity
- `incident_duration_seconds`: Time to resolution
- `active_incidents`: Current open incidents
- `ai_analysis_duration_seconds`: AI processing time
- `http_requests_total`: API request counts
- `websocket_connections`: Active WebSocket connections

### Future Enhancements
- Distributed tracing (Jaeger, Zipkin)
- Log aggregation (ELK stack)
- Error tracking (Sentry)
- APM (Datadog, New Relic)
