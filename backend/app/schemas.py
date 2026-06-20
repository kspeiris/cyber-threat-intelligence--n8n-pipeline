from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

class SeverityLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class IndicatorType(str, Enum):
    IP = "ip"
    DOMAIN = "domain"
    URL = "url"
    HASH = "hash"

# Threat schemas
class ThreatBase(BaseModel):
    cve_id: Optional[str] = None
    title: str
    description: str
    severity: SeverityLevel
    cvss_score: Optional[float] = None
    source: str
    published_date: datetime

class ThreatCreate(ThreatBase):
    pass

class ThreatResponse(ThreatBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Indicator schemas
class IndicatorBase(BaseModel):
    indicator_type: IndicatorType
    indicator_value: str
    risk_score: float = 0.0
    source: str
    metadata: Optional[Dict[str, Any]] = None

class IndicatorCreate(IndicatorBase):
    pass

class IndicatorResponse(IndicatorBase):
    id: int
    first_seen: datetime
    last_seen: Optional[datetime] = None
    is_active: bool

    class Config:
        from_attributes = True

# Alert schemas
class AlertBase(BaseModel):
    threat_id: int
    alert_type: str
    message: str
    severity: SeverityLevel

class AlertCreate(AlertBase):
    pass

class AlertResponse(AlertBase):
    id: int
    created_at: datetime
    is_resolved: bool
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Report schemas
class ReportResponse(BaseModel):
    id: int
    report_type: str
    generated_at: datetime
    summary: str
    metrics: Dict[str, Any]
    recommendations: Optional[str] = None

    class Config:
        from_attributes = True

# Statistics schemas
class ThreatStatistics(BaseModel):
    total_threats: int
    critical: int
    high: int
    medium: int
    low: int
    new_today: int
    new_week: int

class IndicatorStatistics(BaseModel):
    total_indicators: int
    by_type: Dict[str, int]
    high_risk: int
    medium_risk: int
    low_risk: int

class TrendPoint(BaseModel):
    date: str
    count: int

class ThreatTrends(BaseModel):
    labels: List[str]
    values: List[int]

# Collection result
class CollectionResult(BaseModel):
    status: str
    message: str
    timestamp: str