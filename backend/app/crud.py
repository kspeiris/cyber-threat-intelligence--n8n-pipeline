from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import json

from . import models, schemas

# Threat CRUD operations
def create_threat(db: Session, threat: schemas.ThreatCreate) -> models.Threat:
    """Create a new threat"""
    db_threat = models.Threat(**threat.dict())
    db.add(db_threat)
    db.commit()
    db.refresh(db_threat)
    return db_threat

def get_threat(db: Session, threat_id: int) -> Optional[models.Threat]:
    """Get a threat by ID"""
    return db.query(models.Threat).filter(models.Threat.id == threat_id).first()

def get_threat_by_cve(db: Session, cve_id: str) -> Optional[models.Threat]:
    """Get a threat by CVE ID"""
    return db.query(models.Threat).filter(models.Threat.cve_id == cve_id).first()

def get_threats(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    severity: Optional[str] = None
) -> List[models.Threat]:
    """Get all threats with optional filters"""
    query = db.query(models.Threat)
    if severity:
        query = query.filter(models.Threat.severity == severity)
    return query.order_by(desc(models.Threat.published_date)).offset(skip).limit(limit).all()

def get_threat_statistics(db: Session) -> schemas.ThreatStatistics:
    """Get threat statistics"""
    now = datetime.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = now - timedelta(days=7)
    
    total = db.query(models.Threat).count()
    critical = db.query(models.Threat).filter(models.Threat.severity == "critical").count()
    high = db.query(models.Threat).filter(models.Threat.severity == "high").count()
    medium = db.query(models.Threat).filter(models.Threat.severity == "medium").count()
    low = db.query(models.Threat).filter(models.Threat.severity == "low").count()
    new_today = db.query(models.Threat).filter(models.Threat.published_date >= today).count()
    new_week = db.query(models.Threat).filter(models.Threat.published_date >= week_ago).count()
    
    return schemas.ThreatStatistics(
        total_threats=total,
        critical=critical,
        high=high,
        medium=medium,
        low=low,
        new_today=new_today,
        new_week=new_week
    )

def get_threat_trends(db: Session, days: int = 30) -> schemas.ThreatTrends:
    """Get threat trends for the last N days"""
    start_date = datetime.now() - timedelta(days=days)
    
    results = db.query(
        func.date(models.Threat.published_date).label('date'),
        func.count(models.Threat.id).label('count')
    ).filter(
        models.Threat.published_date >= start_date
    ).group_by(
        func.date(models.Threat.published_date)
    ).order_by(
        func.date(models.Threat.published_date)
    ).all()
    
    labels = [str(result[0]) for result in results]
    values = [result[1] for result in results]
    
    return schemas.ThreatTrends(labels=labels, values=values)

# Indicator CRUD operations
def create_indicator(db: Session, indicator: schemas.IndicatorCreate) -> models.Indicator:
    """Create a new indicator"""
    db_indicator = models.Indicator(**indicator.dict())
    db.add(db_indicator)
    db.commit()
    db.refresh(db_indicator)
    return db_indicator

def get_indicator_by_value(db: Session, value: str) -> Optional[models.Indicator]:
    """Get an indicator by value"""
    return db.query(models.Indicator).filter(models.Indicator.indicator_value == value).first()

def get_indicators(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    indicator_type: Optional[str] = None
) -> List[models.Indicator]:
    """Get all indicators with optional filters"""
    query = db.query(models.Indicator)
    if indicator_type:
        query = query.filter(models.Indicator.indicator_type == indicator_type)
    return query.order_by(desc(models.Indicator.risk_score)).offset(skip).limit(limit).all()

def get_indicator_statistics(db: Session) -> schemas.IndicatorStatistics:
    """Get indicator statistics"""
    total = db.query(models.Indicator).count()
    
    by_type = {}
    for indicator_type in models.IndicatorType:
        count = db.query(models.Indicator).filter(
            models.Indicator.indicator_type == indicator_type
        ).count()
        by_type[indicator_type.value] = count
    
    high_risk = db.query(models.Indicator).filter(models.Indicator.risk_score >= 7.0).count()
    medium_risk = db.query(models.Indicator).filter(
        models.Indicator.risk_score >= 4.0,
        models.Indicator.risk_score < 7.0
    ).count()
    low_risk = db.query(models.Indicator).filter(models.Indicator.risk_score < 4.0).count()
    
    return schemas.IndicatorStatistics(
        total_indicators=total,
        by_type=by_type,
        high_risk=high_risk,
        medium_risk=medium_risk,
        low_risk=low_risk
    )

# Alert CRUD operations
def create_alert(db: Session, alert: schemas.AlertCreate) -> models.Alert:
    """Create a new alert"""
    db_alert = models.Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

def get_alerts(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    resolved: Optional[bool] = None
) -> List[models.Alert]:
    """Get all alerts with optional filters"""
    query = db.query(models.Alert)
    if resolved is not None:
        query = query.filter(models.Alert.is_resolved == resolved)
    return query.order_by(desc(models.Alert.created_at)).offset(skip).limit(limit).all()

def resolve_alert(db: Session, alert_id: int) -> Optional[models.Alert]:
    """Resolve an alert"""
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if alert:
        alert.is_resolved = True
        alert.resolved_at = datetime.now()
        db.commit()
        db.refresh(alert)
    return alert

# Report generation
def generate_daily_report(db: Session) -> schemas.ReportResponse:
    """Generate daily report"""
    now = datetime.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    threats_today = db.query(models.Threat).filter(
        models.Threat.published_date >= today
    ).count()
    
    critical_today = db.query(models.Threat).filter(
        models.Threat.published_date >= today,
        models.Threat.severity == "critical"
    ).count()
    
    stats = get_threat_statistics(db)
    
    summary = f"Daily Threat Report - {now.strftime('%Y-%m-%d')}\n"
    summary += f"New threats today: {threats_today}\n"
    summary += f"Critical threats today: {critical_today}\n"
    summary += f"Total active threats: {stats.total_threats}\n"
    
    metrics = {
        "new_threats": threats_today,
        "critical_today": critical_today,
        "total_threats": stats.total_threats,
        "by_severity": {
            "critical": stats.critical,
            "high": stats.high,
            "medium": stats.medium,
            "low": stats.low
        }
    }
    
    # Create report
    db_report = models.Report(
        report_type="daily",
        summary=summary,
        metrics=metrics,
        recommendations="Review critical vulnerabilities immediately. Update patch management priorities."
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    return schemas.ReportResponse(
        id=db_report.id,
        report_type=db_report.report_type,
        generated_at=db_report.generated_at,
        summary=db_report.summary,
        metrics=db_report.metrics,
        recommendations=db_report.recommendations
    )

def generate_weekly_report(db: Session) -> schemas.ReportResponse:
    """Generate weekly report"""
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    
    threats_week = db.query(models.Threat).filter(
        models.Threat.published_date >= week_ago
    ).count()
    
    stats = get_threat_statistics(db)
    trends = get_threat_trends(db, days=7)
    
    summary = f"Weekly Threat Report - Week of {now.strftime('%Y-%m-%d')}\n"
    summary += f"New threats this week: {threats_week}\n"
    summary += f"Total threats: {stats.total_threats}\n"
    summary += f"Critical: {stats.critical}, High: {stats.high}\n"
    
    metrics = {
        "new_threats": threats_week,
        "total_threats": stats.total_threats,
        "by_severity": {
            "critical": stats.critical,
            "high": stats.high,
            "medium": stats.medium,
            "low": stats.low
        },
        "trends": {
            "labels": trends.labels,
            "values": trends.values
        }
    }
    
    # Create report
    db_report = models.Report(
        report_type="weekly",
        summary=summary,
        metrics=metrics,
        recommendations="Based on weekly trends, prioritize vulnerability remediation. Consider implementing additional security controls for high-risk threats."
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    return schemas.ReportResponse(
        id=db_report.id,
        report_type=db_report.report_type,
        generated_at=db_report.generated_at,
        summary=db_report.summary,
        metrics=db_report.metrics,
        recommendations=db_report.recommendations
    )

def get_reports(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[models.Report]:
    """Get all generated reports"""
    return db.query(models.Report).order_by(desc(models.Report.generated_at)).offset(skip).limit(limit).all()