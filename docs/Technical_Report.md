# Technical Report

## 1. System Overview

The Cyber Threat Intelligence Pipeline is designed to automate the collection, analysis, and reporting of cybersecurity threats through integrated workflows and intelligence feeds.

## 2. Architecture Design

### 2.1 Microservices Architecture
The system follows a microservices pattern with:
- **Backend Service**: FastAPI REST API for data operations
- **Frontend Service**: Streamlit dashboard for visualization
- **Workflow Engine**: n8n for automation and scheduling
- **Database Service**: PostgreSQL for persistent storage

### 2.2 Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| API | FastAPI | Async support, automatic docs, high performance |
| Database | PostgreSQL | Reliability, JSONB support, full-text search |
| Frontend | Streamlit | Rapid development, built-in widgets, Plotly integration |
| Automation | n8n | Visual workflows, extensive integrations |

## 3. Database Design

### 3.1 Entity Relationship Diagram
```
Threats 1───∞ Alerts
   │
Indicators (independent)
   │
Reports (independent)
```

### 3.2 Indexing Strategy
- Threats: Indexed by severity, published_date
- Indicators: Indexed by type, risk_score
- Alerts: Indexed by is_resolved, created_at

## 4. API Design

### 4.1 REST Principles
- Resource-based endpoints
- HTTP status codes
- JSON request/response format
- Pagination support

### 4.2 Security Considerations
- CORS configuration
- Environment variable secrets
- SQL injection prevention via ORM

## 5. Deployment Architecture

### 5.1 Docker Compose Setup
Services are isolated in containers with:
- Shared network (threat_network)
- Persistent volumes for data
- Environment variable configuration

### 5.2 Scalability
- Horizontal scaling via Docker Swarm
- Database connection pooling
- Stateless API containers

## 6. Testing Strategy

### 6.1 Unit Tests
Located in `backend/tests/` covering:
- API endpoint testing
- CRUD operations
- Threat collection logic

### 6.2 Integration Tests
- Database operations
- External API calls (mocked)

## 7. Security Features

- Input validation via Pydantic
- SQL injection prevention via SQLAlchemy ORM
- Secrets management via .env files
- Automated security alerts

## 8. Performance Optimization

- Database connection pooling
- Async endpoints
- Caching for statistics
- Pagination for large datasets