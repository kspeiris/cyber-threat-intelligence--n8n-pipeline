from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import logging
import uvicorn

from . import models, schemas, crud, database, alert_service, threat_collector, ai_analyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Cyber Threat Intelligence Pipeline",
    description="Automated Vulnerability Monitoring and Threat Analysis System",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    models.Base.metadata.create_all(bind=database.engine)
    logger.info("Database initialized successfully")

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Cyber Threat Intelligence Pipeline API",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

# Threat endpoints
@app.post("/api/threats/collect", response_model=schemas.CollectionResult)
async def collect_threats(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Collect threats from external sources"""
    background_tasks.add_task(threat_collector.collect_all_threats, db)
    return schemas.CollectionResult(
        status="started",
        message="Threat collection initiated in background",
        timestamp=datetime.now().isoformat()
    )

@app.get("/api/threats", response_model=List[schemas.ThreatResponse])
async def get_threats(
    skip: int = 0,
    limit: int = 100,
    severity: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all threats with optional filters"""
    threats = crud.get_threats(db, skip=skip, limit=limit, severity=severity)
    return threats

@app.get("/api/threats/statistics")
async def get_threat_statistics(db: Session = Depends(get_db)):
    """Get threat statistics"""
    stats = crud.get_threat_statistics(db)
    return stats

@app.get("/api/threats/trends")
async def get_threat_trends(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get threat trends for the last N days"""
    trends = crud.get_threat_trends(db, days=days)
    return trends

@app.get("/api/threats/{threat_id}", response_model=schemas.ThreatResponse)
async def get_threat(threat_id: int, db: Session = Depends(get_db)):
    """Get a specific threat by ID"""
    threat = crud.get_threat(db, threat_id=threat_id)
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    return threat

# Indicator endpoints
@app.post("/api/indicators/collect")
async def collect_indicators(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Collect indicators of compromise"""
    background_tasks.add_task(threat_collector.collect_indicators, db)
    return {
        "status": "started",
        "message": "Indicator collection initiated",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/indicators", response_model=List[schemas.IndicatorResponse])
async def get_indicators(
    skip: int = 0,
    limit: int = 100,
    indicator_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all indicators with optional filters"""
    indicators = crud.get_indicators(db, skip=skip, limit=limit, indicator_type=indicator_type)
    return indicators

@app.get("/api/indicators/statistics")
async def get_indicator_statistics(db: Session = Depends(get_db)):
    """Get indicator statistics"""
    stats = crud.get_indicator_statistics(db)
    return stats

# Alert endpoints
@app.get("/api/alerts", response_model=List[schemas.AlertResponse])
async def get_alerts(
    skip: int = 0,
    limit: int = 100,
    resolved: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all alerts"""
    alerts = crud.get_alerts(db, skip=skip, limit=limit, resolved=resolved)
    return alerts

@app.post("/api/alerts/{alert_id}/resolve")
async def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """Resolve an alert"""
    alert = crud.resolve_alert(db, alert_id=alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"status": "success", "message": "Alert resolved"}

# AI Analysis endpoint
@app.post("/api/threats/{threat_id}/analyze")
async def analyze_threat(
    threat_id: int,
    db: Session = Depends(get_db)
):
    """Get AI analysis for a specific threat"""
    threat = crud.get_threat(db, threat_id=threat_id)
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    
    analysis = ai_analyzer.analyze_threat(threat)
    return analysis

# Report generation endpoint
@app.get("/api/reports", response_model=List[schemas.ReportResponse])
async def get_reports(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all generated reports"""
    reports = crud.get_reports(db, skip=skip, limit=limit)
    return reports

@app.post("/api/reports/generate", response_model=schemas.ReportResponse)
async def generate_report(
    report_type: str = "daily",
    db: Session = Depends(get_db)
):
    """Generate a new threat report (daily or weekly)"""
    if report_type == "weekly":
        report = crud.generate_weekly_report(db)
    else:
        report = crud.generate_daily_report(db)
    return report

@app.get("/api/reports/daily")
async def generate_daily_report(
    db: Session = Depends(get_db)
):
    """Generate a daily threat report"""
    report = crud.generate_daily_report(db)
    return report

@app.get("/api/reports/weekly")
async def generate_weekly_report(
    db: Session = Depends(get_db)
):
    """Generate a weekly threat report"""
    report = crud.generate_weekly_report(db)
    return report

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)