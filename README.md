<div align="center">

# 🛡️ Cyber Threat Intelligence Pipeline

**An end-to-end, automated CTI platform — powered by n8n orchestration, a FastAPI intelligence engine, PostgreSQL persistence, and a premium dark-mode Streamlit dashboard.**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![n8n](https://img.shields.io/badge/n8n-Workflow%20Automation-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)](https://n8n.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

</div>

---

## 📌 Overview

This project builds a **production-grade Cyber Threat Intelligence (CTI)** system that automatically discovers, classifies, and visualises security vulnerabilities. At its core, the pipeline is orchestrated by **n8n** — a powerful open-source workflow automation engine — which schedules data collection every 6 hours, aggregates threat data from public intelligence feeds, and dispatches real-time Telegram push notifications to the security team.

The collected data is stored in a normalised **PostgreSQL** schema and served through a **FastAPI** REST API, while analysts consume the intelligence through a sleek, **glassmorphic dark-mode Streamlit dashboard** powered by interactive Plotly charts.

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      n8n Orchestration Engine                │
│  ┌──────────────┐   ┌────────────┐   ┌──────────────────┐  │
│  │ Schedule     │──▶│  HTTP      │──▶│  Telegram        │  │
│  │ Trigger (6h) │   │  Requests  │   │  Notification    │  │
│  └──────────────┘   └─────┬──────┘   └──────────────────┘  │
└───────────────────────────┼──────────────────────────────────┘
                            │ POST /api/threats/collect
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                     FastAPI Backend (Port 8000)              │
│                                                              │
│   NVD API Collector ──▶ Threat Parser ──▶ AI Risk Analyser  │
│   CISA KEV Feed    ──▶ IOC Classifier ──▶ Alert Service     │
│                                          │                   │
│                                          ▼                   │
│                               SQLAlchemy ORM Layer           │
└─────────────────────────────────┬────────────────────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │   PostgreSQL Database   │
                    │                         │
                    │  • threats              │
                    │  • indicators           │
                    │  • alert_logs           │
                    │  • reports              │
                    └────────────┬────────────┘
                                 │ REST API
                                 ▼
┌──────────────────────────────────────────────────────────────┐
│                Streamlit Dashboard (Port 8501)               │
│                                                              │
│  📊 Dashboard  🔍 Threats  🎯 IOCs  🔔 Alerts  📋 Reports  │
│  ─────────────────────────────────────────────────────────  │
│  Plotly Dark Charts  │  Glassmorphic UI  │  Live Metrics    │
└──────────────────────────────────────────────────────────────┘
                                 │
                    Telegram Bot API (Alerts)
```

---

## ⚙️ n8n Workflow Automation

The n8n engine is the **central nervous system** of this pipeline. The workflow runs on a 6-hour schedule and executes the full data collection lifecycle without any manual intervention.

### 🔄 Workflow Steps (`n8n-workflows/threat_intelligence_workflow.json`)

| Step | Node | Action |
|------|------|--------|
| 1️⃣ | **Schedule Trigger** | Fires every 6 hours automatically |
| 2️⃣ | **Collect Threats** | `POST /api/threats/collect` — triggers NVD ingestion in background |
| 3️⃣ | **Wait 30s** | Allows background processing to complete |
| 4️⃣ | **Collect Indicators** | `POST /api/indicators/collect` — pulls IOC data from threat feeds |
| 5️⃣ | **Generate Report** | `GET /api/reports/daily` — compiles today's threat summary |
| 6️⃣ | **Telegram Notification** | Pushes a collection-complete alert to the security channel |

### 🚀 Importing the Workflow
1. Open n8n at `http://localhost:5678`
2. Go to **Workflows → Import from File**
3. Import `n8n-workflows/threat_intelligence_workflow.json`
4. Add your Telegram credentials in the Telegram node
5. Activate the workflow — it runs on autopilot from here!

---

## 🚀 Key Features & Techniques

### 🕵️ Multi-Source Threat Intelligence Collection
Ingests vulnerabilities from the **NVD (National Vulnerability Database) CVE API v2.0** and processes them with full CVSS v3.1 metric extraction (base score, severity, attack vector). The collector parses nested JSON schemas, extracts English-language descriptions, and maps severity classifications to a normalised internal enum.

- **Technique**: The collector is triggered via a FastAPI `BackgroundTask` so the HTTP response returns instantly while processing happens asynchronously — keeping the API non-blocking at all times.
- **Resilience**: A curated baseline of real-world CVEs (e.g. `CVE-2024-21412`, `CVE-2024-21338`) is loaded as a fallback when the upstream NVD API is rate-limited, ensuring the system is always demonstrably functional.

### 🧠 Heuristic AI Risk Analysis
The `ai_analyzer` module performs automated threat intelligence enrichment by applying rule-based heuristics against a threat's severity, CVSS metadata, and published description to produce:
- An **exploitability score** and **impact rating**
- Structured **remediation recommendations** tailored to severity level
- An **affected systems** and **attack vector** assessment
- A plain-language **threat summary** for security briefings

### 🗄️ Normalised Relational Schema (PostgreSQL + SQLAlchemy)
The data model is designed for query efficiency and referential integrity:
- `threats` — stores CVE metadata, CVSS scores, and severity enums
- `indicators` — tracks IOCs (IPs, domains, file hashes) with individual risk scores
- `alert_logs` — links alerts back to threat records via foreign key
- `reports` — persists generated daily/weekly summaries with JSON metrics blobs

**Technique**: SQLAlchemy ORM with Alembic-compatible `Base.metadata.create_all()` enables zero-downtime schema bootstrapping. Enum types are enforced at both the database and Python layer.

### 🚨 Real-time Telegram Alerting
When a critical vulnerability (CVSS ≥ 8.0) is ingested, the `alert_service` immediately fires a formatted HTML message to the configured Telegram channel via the **Telegram Bot API**, and simultaneously writes a structured alert record to the `alert_logs` table.

- **Technique**: Alerts are created both via n8n's built-in Telegram node (for scheduled reports) AND directly from the Python backend (for real-time critical CVE triggers), giving two independent notification paths.

### 💎 Premium Glassmorphic UI (Streamlit + Custom CSS)
The dashboard transcends standard Streamlit limitations through deep CSS injection and Plotly theming:
- **Glassmorphism**: `backdrop-filter: blur(10px)` + `rgba` borders on metric cards
- **Hover micro-animations**: `transform: translateY(-2px)` lift effect on every card
- **Gradient buttons**: Linear-gradient buttons with animated box-shadow glow
- **Dark Plotly charts**: `template="plotly_dark"` + `paper_bgcolor="rgba(0,0,0,0)"` for seamless chart integration
- **Area fill trend chart**: Gradient fill under the threat trend line for visual depth
- **Donut chart**: Severity distribution rendered as a donut (`hole=0.4`) for modern clarity

---

## 📸 Screenshots

> 📁 Place screenshots in `docs/screenshots/` to populate these sections.

| Page | Preview |
|------|---------|
| 📊 Dashboard | `docs/screenshots/dashboard.png` |
| 🔍 Threat Management | `docs/screenshots/threats.png` |
| 🎯 Indicators of Compromise | `docs/screenshots/indicators.png` |
| 🔔 Alerts | `docs/screenshots/alerts.png` |
| 📋 Reports | `docs/screenshots/reports.png` |
| 🤖 AI Analysis | `docs/screenshots/ai_analysis.png` |

---

## 🗂️ Project Structure

```
cyber-threat-intelligence--n8n-pipeline/
├── 📁 backend/                    # FastAPI backend service
│   ├── 📁 app/
│   │   ├── main.py               # API routes & application setup
│   │   ├── models.py             # SQLAlchemy ORM models
│   │   ├── schemas.py            # Pydantic request/response schemas
│   │   ├── crud.py               # Database CRUD operations
│   │   ├── database.py           # DB engine & session factory
│   │   ├── threat_collector.py   # NVD API ingestion logic
│   │   ├── ai_analyzer.py        # Threat risk analysis engine
│   │   └── alert_service.py      # Telegram alerting service
│   ├── requirements.txt
│   └── Dockerfile
│
├── 📁 dashboard/                  # Streamlit frontend
│   ├── app.py                    # Dashboard pages & visualizations
│   ├── .streamlit/config.toml    # Dark theme configuration
│   ├── requirements.txt
│   └── Dockerfile
│
├── 📁 n8n-workflows/              # n8n automation workflows
│   └── threat_intelligence_workflow.json
│
├── 📁 docs/                       # Documentation & screenshots
├── 📄 docker-compose.yml          # Full stack orchestration
├── 📄 init.sql                    # Database initialization script
└── 📄 README.md
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.12+
- PostgreSQL 15+
- Docker & Docker Compose (optional, for full stack)
- n8n (optional, for workflow automation)

### Option A: Docker Compose (Recommended — Full Stack)

Spins up PostgreSQL, FastAPI backend, Streamlit dashboard, and n8n in one command:

```bash
docker-compose up -d
```

| Service | URL |
|---------|-----|
| 🖥️ Dashboard | http://localhost:8501 |
| ⚡ API | http://localhost:8000 |
| 📖 API Docs | http://localhost:8000/docs |
| 🔄 n8n | http://localhost:5678 |

### Option B: Local Development

**1. Database Setup**
```bash
psql -U postgres -c "CREATE DATABASE threat_intelligence;"
```

**2. Backend**
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate          # Windows
# source venv/bin/activate       # Linux/Mac

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**3. Dashboard** (new terminal)
```bash
cd dashboard
python -m venv venv
.\venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

### 🔑 Environment Variables (`backend/.env`)

```env
# Database
DATABASE_URL=postgresql://postgres:Admin123@localhost:5432/threat_intelligence

# NVD API (optional - improves rate limits)
# Get free key at: https://nvd.nist.gov/developers/request-an-api-key
NVD_API_KEY=your_nvd_api_key_here

# Telegram Alerting (optional)
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

---

## 📡 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/threats` | List all threats (filterable by severity) |
| `GET` | `/api/threats/statistics` | Threat count by severity |
| `GET` | `/api/threats/trends?days=30` | Daily trend data for charts |
| `POST` | `/api/threats/collect` | Trigger NVD ingestion (background) |
| `POST` | `/api/threats/{id}/analyze` | Run AI analysis on a specific threat |
| `GET` | `/api/indicators` | List all indicators of compromise |
| `POST` | `/api/indicators/collect` | Trigger IOC collection |
| `GET` | `/api/alerts` | List alerts (filterable by resolved status) |
| `POST` | `/api/alerts/{id}/resolve` | Mark an alert as resolved |
| `GET` | `/api/reports` | List all generated reports |
| `POST` | `/api/reports/generate` | Generate a new daily/weekly report |

> Full interactive documentation: **http://localhost:8000/docs**

---

## 🛡️ License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.