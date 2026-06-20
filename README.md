# Cyber Threat Intelligence Pipeline

An automated vulnerability monitoring and threat analysis system using n8n, FastAPI, PostgreSQL, and Streamlit.

## 🎯 Features

- **Automated Threat Collection**: Collects CVEs from NVD and other sources
- **Indicator of Compromise (IOC) Tracking**: Monitors malicious IPs, domains, and hashes
- **Real-time Alerts**: Telegram notifications for critical threats
- **Interactive Dashboard**: Visual analytics with Streamlit
- **AI-Assisted Analysis**: Threat summaries and recommendations
- **Comprehensive Reporting**: Daily and weekly threat reports
- **Workflow Automation**: n8n for scheduled threat collection

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.10+
- Git

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/cyber-threat-intelligence-pipeline.git
cd cyber-threat-intelligence-pipeline
```

2. **Run setup script**
```bash
chmod +x setup.sh
./setup.sh
```

3. **Configure environment variables**
   - Edit `backend/.env` with your API keys:
     - NVD_API_KEY (optional)
     - TELEGRAM_BOT_TOKEN
     - TELEGRAM_CHAT_ID

4. **Import n8n workflow**
   - Access n8n at http://localhost:5678
   - Import workflow from `n8n-workflows/threat_intelligence_workflow.json`
   - Configure Telegram credentials in n8n

5. **Access services**
   - Dashboard: http://localhost:8501
   - API Docs: http://localhost:8000/docs
   - n8n: http://localhost:5678

## 📊 Architecture

```
┌─────────────┐     ┌──────────┐     ┌────────────┐
│ Threat      │     │ n8n      │     │ FastAPI    │
│ Sources     │────▶│ Workflow │────▶│ Backend    │
│             │     │          │     │            │
└─────────────┘     └──────────┘     └────────────┘
                           │                  │
                           ▼                  ▼
                     ┌──────────┐     ┌────────────┐
                     │ Telegram │     │ PostgreSQL │
                     │ Alerts   │     │ Database   │
                     └──────────┘     └────────────┘
                           │                  │
                           ▼                  ▼
                     ┌────────────────────────────┐
                     │ Streamlit Dashboard        │
                     │ - Threat Analytics         │
                     │ - IOC Monitoring           │
                     │ - AI Analysis              │
                     └────────────────────────────┘
```

## 🔧 Services

### Backend API (FastAPI)
- RESTful API for threat management
- Database operations via SQLAlchemy
- Threat collection and processing
- AI analysis integration

### Database (PostgreSQL)
- Threat storage with severity classification
- IOC tracking
- Alert logging
- Report generation

### Dashboard (Streamlit)
- Real-time threat visualization
- Interactive analytics
- AI threat analysis
- Report generation

### Workflow Automation (n8n)
- Scheduled threat collection
- Automated reporting
- Alert distribution

## 📁 Project Structure

```
.
├── backend/               # FastAPI Backend
│   ├── app/
│   │   ├── main.py       # API endpoints
│   │   ├── models.py     # Database models
│   │   ├── schemas.py    # Pydantic schemas
│   │   ├── crud.py       # CRUD operations
│   │   ├── threat_collector.py
│   │   ├── alert_service.py
│   │   └── ai_analyzer.py
│   ├── requirements.txt
│   └── .env
├── dashboard/            # Streamlit Dashboard
│   ├── app.py
│   └── requirements.txt
├── n8n-workflows/        # n8n Workflow definitions
│   └── threat_intelligence_workflow.json
├── docker-compose.yml
└── setup.sh
```

## 🛠️ Development

### Running Locally
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### API Documentation
Access auto-generated Swagger documentation at: http://localhost:8000/docs

### Testing
```bash
# Run unit tests (pending implementation)
python -m pytest

# Test API endpoints
curl http://localhost:8000/
```

## 🔒 Security Considerations

1. **API Keys**: Store securely in `.env` file
2. **Database**: Default credentials should be changed
3. **n8n**: Enable authentication in production
4. **HTTPS**: Use SSL/TLS in production

## 📊 Database Schema

### Threats Table
- id (Primary Key)
- cve_id (Unique)
- title
- description
- severity (critical/high/medium/low)
- cvss_score
- source
- published_date

### Indicators Table
- id (Primary Key)
- indicator_type (ip/domain/url/hash)
- indicator_value (Unique)
- risk_score
- source

### Alerts Table
- id (Primary Key)
- threat_id (Foreign Key)
- alert_type
- message
- severity
- is_resolved

## 🤖 AI Integration

The system includes a mock AI analysis module. To integrate with real AI services:

1. **OpenAI**: Configure `OPENAI_API_KEY` and use GPT models
2. **Claude**: Use Anthropic's API for advanced analysis
3. **Local LLM**: Deploy models with Ollama or similar

## 📈 Performance

- API Response Time: < 3 seconds
- Dashboard Load Time: < 5 seconds
- Database: Optimized with indexes
- Caching: Planned for future updates

## 🚧 Future Enhancements

1. **Machine Learning**: Predictive threat analysis
2. **SIEM Integration**: Connect to security information systems
3. **Multi-user Authentication**: Role-based access control
4. **Advanced Analytics**: Threat correlation and pattern detection
5. **Mobile App**: Android/iOS monitoring application

## 📝 License

MIT License - See LICENSE file for details

## 👥 Contributors

Your Name - Initial work

## 🙏 Acknowledgments

- NVD API
- Open Source Community
- FastAPI, Streamlit, n8n teams

---
**Note**: This is a proof-of-concept system. Production deployments require additional security hardening and monitoring.