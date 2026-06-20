.PHONY: help install build up down logs clean test lint format

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make build      - Build Docker containers"
	@echo "  make up         - Start all services"
	@echo "  make down       - Stop all services"
	@echo "  make logs       - View logs"
	@echo "  make clean      - Clean Docker containers and volumes"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linters"
	@echo "  make format     - Format code"

install:
	pip install -r backend/requirements.txt
	pip install -r dashboard/requirements.txt

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services started:"
	@echo "  - Backend: http://localhost:8000"
	@echo "  - Dashboard: http://localhost:8501"
	@echo "  - n8n: http://localhost:5678"

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	docker system prune -f

test:
	cd backend && python -m pytest
	cd dashboard && python -m pytest

lint:
	cd backend && black --check app/
	cd backend && flake8 app/
	cd dashboard && black --check app.py

format:
	cd backend && black app/
	cd dashboard && black app.py

dev-up:
	docker-compose -f docker-compose.dev.yml up -d

dev-down:
	docker-compose -f docker-compose.dev.yml down

dev-logs:
	docker-compose -f docker-compose.dev.yml logs -f

db-shell:
	docker-compose exec postgres psql -U user -d threat_intelligence

api-shell:
	docker-compose exec backend python

dashboard-shell:
	docker-compose exec dashboard bash