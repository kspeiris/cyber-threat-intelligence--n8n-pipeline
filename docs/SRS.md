# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose
This document specifies the software requirements for the Cyber Threat Intelligence Pipeline, an automated system for vulnerability monitoring and threat analysis.

### 1.2 Scope
The system collects vulnerability data from external sources, analyzes threats, and provides actionable security insights through dashboards and alerts.

### 1.3 Definitions
- **CVE**: Common Vulnerabilities and Exposures
- **CVSS**: Common Vulnerability Scoring System
- **IOC**: Indicator of Compromise

## 2. Overall Description

### 2.1 Product Perspective
The system is a standalone application designed to integrate with existing security infrastructure.

### 2.2 Product Functions
- Automated threat collection from NVD
- IOC tracking and monitoring
- Real-time alerting system
- Interactive analytics dashboard
- AI-powered threat analysis
- Report generation

### 2.3 User Characteristics
- Security analysts
- System administrators
- IT security managers

## 3. Specific Requirements

### 3.1 External Interface Requirements

#### 3.1.1 User Interfaces
- Streamlit web dashboard
- n8n workflow interface
- REST API endpoints

#### 3.1.2 Hardware Interfaces
- Docker-compatible environment
- PostgreSQL database

#### 3.1.3 Software Interfaces
- NVD API integration
- Telegram Bot API
- Optional: OpenAI API

### 3.2 Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | Collect CVEs from NVD API | High |
| FR-02 | Store threats in database | High |
| FR-03 | Generate alerts for critical threats | High |
| FR-04 | Display threat analytics dashboard | High |
| FR-05 | Generate daily/weekly reports | Medium |
| FR-06 | Provide AI threat analysis | Medium |

### 3.3 Non-Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-01 | API response time < 3s | High |
| NFR-02 | Support 1000 concurrent threats | Medium |
| NFR-03 | Secure API with authentication | High |
| NFR-04 | Docker containerized deployment | High |

## 4. System Architecture

### 4.1 High-Level Architecture
```
┌─────────────────┐     ┌──────────┐     ┌────────────┐
│   NVD API       │────▶│  FastAPI  │────▶│ PostgreSQL  │
│ (Threat Source)  │     │  Backend  │     │ Database    │
└─────────────────┘     └──────────┘     └────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │  Streamlit          │
                    │  Dashboard          │
                    └─────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │  n8n Workflows      │
                    │  (Automation)       │
                    └─────────────────────┘
```

## 5. Data Model

### 5.1 Threat Entity
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| cve_id | String | CVE identifier |
| title | String | Threat title |
| severity | Enum | critical/high/medium/low |
| cvss_score | Float | CVSS base score |

### 5.2 Indicator Entity
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| type | Enum | ip/domain/url/hash |
| value | String | Indicator value |
| risk_score | Float | Risk assessment score |

## 6. API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/threats | Get all threats |
| POST | /api/threats/collect | Collect threats |
| GET | /api/threats/statistics | Get statistics |
| GET | /api/alerts | Get all alerts |
| POST | /api/alerts/{id}/resolve | Resolve an alert |

## 7. Constraints

- Must run on Docker-compatible platforms
- Requires PostgreSQL 15+
- Python 3.10+ required