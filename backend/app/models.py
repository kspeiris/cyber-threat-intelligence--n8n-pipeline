from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base
import enum

class SeverityLevel(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class IndicatorType(str, enum.Enum):
    IP = "ip"
    DOMAIN = "domain"
    URL = "url"
    HASH = "hash"

class Threat(Base):
    __tablename__ = "threats"

    id = Column(Integer, primary_key=True, index=True)
    cve_id = Column(String(50), unique=True, index=True, nullable=True)
    title = Column(String(500))
    description = Column(Text)
    severity = Column(Enum(SeverityLevel))
    cvss_score = Column(Float, nullable=True)
    source = Column(String(100))
    published_date = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    alerts = relationship("Alert", back_populates="threat", cascade="all, delete-orphan")

class Indicator(Base):
    __tablename__ = "indicators"

    id = Column(Integer, primary_key=True, index=True)
    indicator_type = Column(Enum(IndicatorType))
    indicator_value = Column(String(500), unique=True, index=True)
    risk_score = Column(Float, default=0.0)
    source = Column(String(100))
    first_seen = Column(DateTime, server_default=func.now())
    last_seen = Column(DateTime, onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Additional metadata
    metadata = Column(JSON, nullable=True)

class Alert(Base):
    __tablename__ = "alert_logs"

    id = Column(Integer, primary_key=True, index=True)
    threat_id = Column(Integer, ForeignKey("threats.id"))
    alert_type = Column(String(50))
    message = Column(Text)
    severity = Column(Enum(SeverityLevel))
    created_at = Column(DateTime, server_default=func.now())
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)
    
    # Relationships
    threat = relationship("Threat", back_populates="alerts")

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String(20))  # daily, weekly
    generated_at = Column(DateTime, server_default=func.now())
    summary = Column(Text)
    metrics = Column(JSON)
    recommendations = Column(Text, nullable=True)