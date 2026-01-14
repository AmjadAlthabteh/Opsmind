# Deployment Guide

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API Key (for AI features)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

5. Seed demo data:
```bash
python seed_data.py
```

6. Run development server:
```bash
python run.py
```

Backend will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/api/docs`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run development server:
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Production Deployment

### Docker Deployment

#### Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ENVIRONMENT=production
    volumes:
      - ./backend/faiss_index:/app/faiss_index
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

### Cloud Deployment

#### AWS (Elastic Beanstalk)

1. Install AWS CLI and EB CLI
2. Initialize Elastic Beanstalk:
```bash
eb init -p python-3.11 ai-incident-commander
```

3. Create environment:
```bash
eb create production-env
```

4. Deploy:
```bash
eb deploy
```

#### Google Cloud Platform (Cloud Run)

1. Build and push backend:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/ai-incident-commander-backend ./backend
gcloud run deploy backend --image gcr.io/PROJECT_ID/ai-incident-commander-backend --platform managed
```

2. Build and push frontend:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/ai-incident-commander-frontend ./frontend
gcloud run deploy frontend --image gcr.io/PROJECT_ID/ai-incident-commander-frontend --platform managed
```

#### Heroku

1. Create Heroku apps:
```bash
heroku create ai-incident-commander-api
heroku create ai-incident-commander-web
```

2. Deploy backend:
```bash
cd backend
git push heroku master
```

3. Deploy frontend:
```bash
cd frontend
heroku buildpacks:set heroku/nodejs
git push heroku master
```

### Kubernetes Deployment

#### Backend Deployment

Create `k8s/backend-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-incident-commander-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: your-registry/ai-incident-commander-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: openai-api-key
---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  selector:
    app: backend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```

Apply:
```bash
kubectl apply -f k8s/backend-deployment.yaml
```

## Environment Variables

### Backend

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key for LLM | - | No* |
| `APP_NAME` | Application name | "AI Incident Commander" | No |
| `DEBUG` | Enable debug mode | `True` | No |
| `ENVIRONMENT` | Environment (development/production) | `development` | No |
| `RATE_LIMIT_PER_MINUTE` | API rate limit | `100` | No |
| `VECTOR_DB_PATH` | Path to FAISS index | `./faiss_index` | No |
| `PROMETHEUS_PORT` | Prometheus metrics port | `8001` | No |

*AI features will be disabled without API key

### Frontend

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `http://localhost:8000` |

## Monitoring Setup

### Prometheus Configuration

Create `prometheus.yml`:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ai-incident-commander'
    static_configs:
      - targets: ['backend:8000']
```

### Grafana Dashboard

1. Add Prometheus as data source
2. Import dashboard JSON from `monitoring/grafana-dashboard.json`

Key metrics to monitor:
- Incident creation rate
- Mean time to resolution (MTTR)
- Active incidents by severity
- AI analysis duration
- API response times
- WebSocket connection count

## Database Migration

### Moving from In-Memory to PostgreSQL

1. Install PostgreSQL dependencies:
```bash
pip install psycopg2-binary sqlalchemy
```

2. Update `storage.py` to use SQLAlchemy
3. Add Alembic for migrations:
```bash
alembic init migrations
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

## Backup & Recovery

### Vector Database Backup

The FAISS index is stored in `faiss_index/`:
```bash
# Backup
tar -czf faiss_backup_$(date +%Y%m%d).tar.gz faiss_index/

# Restore
tar -xzf faiss_backup_YYYYMMDD.tar.gz
```

## Security Hardening

### Production Checklist

- [ ] Enable HTTPS/TLS
- [ ] Configure API authentication (JWT)
- [ ] Set up API key rotation
- [ ] Enable CORS only for trusted domains
- [ ] Implement rate limiting per user
- [ ] Add request logging and audit trails
- [ ] Configure firewall rules
- [ ] Enable database encryption at rest
- [ ] Set up secrets management (AWS Secrets Manager, Vault)
- [ ] Implement RBAC for user permissions
- [ ] Regular security audits and dependency updates

## Performance Optimization

### Backend

- Use Redis for caching incident data
- Implement database connection pooling
- Add CDN for static assets
- Enable gzip compression
- Use async database drivers

### Frontend

- Enable code splitting
- Implement lazy loading for routes
- Optimize images and assets
- Use service workers for offline support
- Enable browser caching

## Troubleshooting

### Backend Issues

**Issue:** AI Commander not working
```bash
# Check if OpenAI API key is set
echo $OPENAI_API_KEY

# Check logs
tail -f logs/app.log
```

**Issue:** High memory usage
```bash
# Clear FAISS index
rm -rf faiss_index/
# Restart application
```

### Frontend Issues

**Issue:** Cannot connect to backend
```bash
# Check VITE_API_URL in .env
# Verify backend is running
curl http://localhost:8000/health
```

**Issue:** WebSocket connection failed
- Check CORS settings on backend
- Verify WebSocket endpoint is accessible
- Check browser console for errors
