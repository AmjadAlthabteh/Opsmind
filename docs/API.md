# API Documentation

## Base URL

```
http://localhost:8000
```

## Endpoints

### Incidents

#### Create Incident
```http
POST /api/incidents/
Content-Type: application/json

{
  "title": "Database connection timeout",
  "description": "Users experiencing 502 errors",
  "severity": "high",
  "source": "datadog",
  "tags": ["database", "postgres"],
  "metadata": {}
}
```

**Response:** `201 Created`

#### List Incidents
```http
GET /api/incidents/?status=open&limit=50
```

**Response:** `200 OK`

#### Get Incident
```http
GET /api/incidents/{incident_id}
```

**Response:** `200 OK`

#### Update Incident Status
```http
PATCH /api/incidents/{incident_id}/status?status=investigating
```

**Response:** `200 OK`

#### Get Incident Timeline
```http
GET /api/incidents/{incident_id}/timeline
```

**Response:** `200 OK`

#### Get Incident Actions
```http
GET /api/incidents/{incident_id}/actions
```

**Response:** `200 OK`

### Events

#### Ingest Single Event
```http
POST /api/ingest/events
Content-Type: application/json

{
  "incident_id": "123e4567-e89b-12d3-a456-426614174000",
  "event_type": "log",
  "message": "PostgreSQL connection pool exhausted",
  "level": "error",
  "source": "api-server-01",
  "metadata": {}
}
```

**Response:** `201 Created`

#### Ingest Batch Events
```http
POST /api/ingest/events/batch
Content-Type: application/json

[
  {
    "incident_id": "...",
    "event_type": "log",
    "message": "...",
    ...
  }
]
```

**Response:** `201 Created`

#### Get Incident Events
```http
GET /api/ingest/events/{incident_id}?limit=100
```

**Response:** `200 OK`

### WebSocket

#### Connect to Incident Room
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/incidents/{incident_id}');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

// Send message
ws.send(JSON.stringify({
  user: 'John Doe',
  message: 'Investigating the issue...'
}));
```

### Health & Metrics

#### Health Check
```http
GET /health
```

**Response:** `200 OK`
```json
{
  "status": "healthy"
}
```

#### Prometheus Metrics
```http
GET /metrics
```

**Response:** `200 OK` (Prometheus format)

## Data Models

### Incident
```typescript
{
  id: string
  title: string
  description: string
  status: "open" | "investigating" | "identified" | "monitoring" | "resolved" | "closed"
  severity: "critical" | "high" | "medium" | "low" | "info"
  source: string
  tags: string[]
  metadata: object
  created_at: datetime
  updated_at: datetime
  resolved_at: datetime | null
  ai_summary: string | null
  root_cause: string | null
  suggested_actions: string[]
  mttr_minutes: number | null
}
```

### Event
```typescript
{
  id: string
  incident_id: string
  event_type: "log" | "metric" | "alert" | "trace" | "user_action"
  message: string
  level: "debug" | "info" | "warning" | "error" | "critical"
  source: string
  metadata: object
  timestamp: datetime
}
```

### Action
```typescript
{
  id: string
  incident_id: string
  title: string
  description: string
  status: "pending" | "in_progress" | "completed" | "failed" | "skipped"
  suggested_by: string
  priority: number
  created_at: datetime
}
```

### Timeline Entry
```typescript
{
  id: string
  incident_id: string
  entry_type: "status_change" | "ai_analysis" | "user_action" | "system_event" | "comment"
  title: string
  description: string
  actor: string
  timestamp: datetime
}
```
