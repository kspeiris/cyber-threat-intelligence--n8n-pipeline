# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication
Currently no authentication required. Add API keys or JWT tokens for production.

## Endpoints

### Health Check

#### GET /
Returns API status.

**Response:**
```json
{
  "message": "Cyber Threat Intelligence Pipeline API",
  "status": "operational",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Threats

#### POST /threats/collect
Initiate background threat collection from configured sources.

**Response:**
```json
{
  "status": "started",
  "message": "Threat collection initiated in background",
  "timestamp": "2024-01-15T10:30:00"
}
```

#### GET /threats
Get all threats with optional filtering and pagination.

**Parameters:**
| Name | Type | Default | Description |
|------|------|---------|-------------|
| skip | int | 0 | Number of records to skip |
| limit | int | 100 | Maximum records to return |
| severity | string | - | Filter by severity (critical/high/medium/low) |

**Response:**
```json
[
  {
    "id": 1,
    "cve_id": "CVE-2024-12345",
    "title": "Test Vulnerability",
    "description": "Vulnerability description",
    "severity": "high",
    "cvss_score": 7.5,
    "source": "NVD",
    "published_date": "2024-01-15T00:00:00",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

#### GET /threats/{threat_id}
Get a specific threat by ID.

**Response:**
```json
{
  "id": 1,
  "cve_id": "CVE-2024-12345",
  "title": "Test Vulnerability",
  "description": "Vulnerability description",
  "severity": "high",
  "cvss_score": 7.5,
  "source": "NVD",
  "published_date": "2024-01-15T00:00:00",
  "created_at": "2024-01-15T10:30:00"
}
```

#### GET /threats/statistics
Get threat statistics summary.

**Response:**
```json
{
  "total_threats": 150,
  "critical": 15,
  "high": 45,
  "medium": 60,
  "low": 30,
  "new_today": 5,
  "new_week": 25
}
```

#### GET /threats/trends
Get threat trends for specified days.

**Parameters:**
| Name | Type | Default | Description |
|------|------|---------|-------------|
| days | int | 30 | Number of days to analyze |

**Response:**
```json
{
  "labels": ["2024-01-01", "2024-01-02"],
  "values": [5, 10]
}
```

### Indicators

#### POST /indicators/collect
Initiate background IOC collection.

#### GET /indicators
Get all indicators with optional filtering.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| indicator_type | string | Filter by type (ip/domain/url/hash) |
| skip | int | Number of records to skip |
| limit | int | Maximum records to return |

#### GET /indicators/statistics
Get indicator statistics.

### Alerts

#### GET /alerts
Get all alerts.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| resolved | boolean | Filter by resolution status |

#### POST /alerts/{alert_id}/resolve
Resolve a specific alert.

### Analysis

#### POST /threats/{threat_id}/analyze
Get AI analysis for a specific threat.

**Response:**
```json
{
  "threat_id": 1,
  "cve_id": "CVE-2024-12345",
  "analysis_timestamp": "2024-01-15T10:30:00",
  "risk_assessment": {
    "overall_risk": "high",
    "exploitability": "High",
    "impact": "Critical"
  },
  "recommendations": "Immediate action required...",
  "additional_insights": {
    "affected_systems": "Windows",
    "attack_vector": "Network",
    "known_exploits": "Yes"
  }
}
```

### Reports

#### GET /reports/daily
Generate daily threat report.

#### GET /reports/weekly
Generate weekly threat report.

## Error Responses

### 404 Not Found
```json
{
  "detail": "Threat not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error message"
}