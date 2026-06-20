import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from app import crud, schemas, models

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

def test_create_threat():
    db = TestingSessionLocal()
    threat_data = schemas.ThreatCreate(
        cve_id="CVE-2024-12345",
        title="Test Vulnerability",
        description="Test description",
        severity="high",
        cvss_score=7.5,
        source="Test Source",
        published_date=datetime.now()
    )
    threat = crud.create_threat(db, threat_data)
    assert threat.cve_id == "CVE-2024-12345"
    assert threat.severity == "high"
    db.close()

def test_get_threat():
    db = TestingSessionLocal()
    threat_data = schemas.ThreatCreate(
        cve_id="CVE-2024-54321",
        title="Test Vulnerability 2",
        description="Test description 2",
        severity="medium",
        cvss_score=5.5,
        source="Test Source 2",
        published_date=datetime.now()
    )
    created = crud.create_threat(db, threat_data)
    fetched = crud.get_threat(db, created.id)
    assert fetched is not None
    assert fetched.cve_id == "CVE-2024-54321"
    db.close()

def test_get_threats():
    db = TestingSessionLocal()
    threats = crud.get_threats(db, limit=50)
    assert isinstance(threats, list)
    db.close()

def test_create_indicator():
    db = TestingSessionLocal()
    indicator_data = schemas.IndicatorCreate(
        indicator_type="ip",
        indicator_value="192.168.1.1",
        risk_score=8.0,
        source="Test Feed"
    )
    indicator = crud.create_indicator(db, indicator_data)
    assert indicator.indicator_value == "192.168.1.1"
    assert indicator.indicator_type == "ip"
    db.close()

def test_create_alert():
    db = TestingSessionLocal()
    # First create a threat
    threat_data = schemas.ThreatCreate(
        cve_id="CVE-2024-ALERT",
        title="Alert Test",
        description="Test for alert",
        severity="critical",
        cvss_score=9.0,
        source="Test",
        published_date=datetime.now()
    )
    threat = crud.create_threat(db, threat_data)
    
    alert_data = schemas.AlertCreate(
        threat_id=threat.id,
        alert_type="test_alert",
        message="Test alert message",
        severity="critical"
    )
    alert = crud.create_alert(db, alert_data)
    assert alert.alert_type == "test_alert"
    assert alert.is_resolved == False
    db.close()