import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app import models, database

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[database.get_db] = override_get_db

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Cyber Threat Intelligence Pipeline API"
    assert response.json()["status"] == "operational"

def test_threat_statistics():
    response = client.get("/api/threats/statistics")
    assert response.status_code == 200
    data = response.json()
    assert "total_threats" in data
    assert "critical" in data
    assert "high" in data
    assert "medium" in data
    assert "low" in data