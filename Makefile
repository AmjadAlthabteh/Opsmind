.PHONY: help install dev clean test docker-build docker-up docker-down seed

help:
	@echo "AI Incident Commander - Make Commands"
	@echo ""
	@echo "  make install       - Install all dependencies"
	@echo "  make dev          - Run development servers"
	@echo "  make seed         - Load demo data"
	@echo "  make test         - Run tests"
	@echo "  make docker-build - Build Docker images"
	@echo "  make docker-up    - Start Docker containers"
	@echo "  make docker-down  - Stop Docker containers"
	@echo "  make clean        - Clean build artifacts"

install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

dev:
	@echo "Starting development servers..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo ""
	@echo "Run these in separate terminals:"
	@echo "  Terminal 1: cd backend && python run.py"
	@echo "  Terminal 2: cd frontend && npm run dev"

seed:
	@echo "Loading demo data..."
	cd backend && python seed_data.py

test:
	@echo "Running backend tests..."
	cd backend && pytest tests/
	@echo "Running frontend tests..."
	cd frontend && npm test

docker-build:
	@echo "Building Docker images..."
	docker-compose build

docker-up:
	@echo "Starting Docker containers..."
	docker-compose up -d
	@echo ""
	@echo "Services running:"
	@echo "  Frontend:   http://localhost:80"
	@echo "  Backend:    http://localhost:8000"
	@echo "  Prometheus: http://localhost:9090"
	@echo "  Grafana:    http://localhost:3001"

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down

clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "node_modules" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name ".venv" -exec rm -rf {} +
	find . -type d -name "venv" -exec rm -rf {} +
