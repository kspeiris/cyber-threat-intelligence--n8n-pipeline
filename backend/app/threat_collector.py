import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
import logging
import os
from dotenv import load_dotenv

from . import models, schemas, crud, alert_service

load_dotenv()
logger = logging.getLogger(__name__)

# NVD API configuration
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
NVD_API_KEY = os.getenv("NVD_API_KEY", "")

def collect_nvd_vulnerabilities(db: Session, days_back: int = 1) -> List[Dict[str, Any]]:
    """Collect vulnerabilities from NVD API"""
    try:
        # Calculate date range
        start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        end_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
        
        params = {
            "pubStartDate": start_date,
            "pubEndDate": end_date,
            "resultsPerPage": 100
        }
        
        headers = {}
        if NVD_API_KEY:
            headers["apiKey"] = NVD_API_KEY
        
        response = requests.get(NVD_API_URL, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        vulnerabilities = []
        
        for vuln in data.get("vulnerabilities", []):
            cve = vuln.get("cve", {})
            cve_id = cve.get("id")
            
            # Skip if CVE already exists
            if crud.get_threat_by_cve(db, cve_id):
                continue
            
            # Extract CVSS score and severity
            metrics = cve.get("metrics", {})
            cvss_v3 = metrics.get("cvssMetricV31", [{}])[0] if metrics.get("cvssMetricV31") else None
            cvss_v2 = metrics.get("cvssMetricV2", [{}])[0] if metrics.get("cvssMetricV2") else None
            
            cvss_score = None
            severity = "low"
            
            if cvss_v3:
                cvss_score = cvss_v3.get("cvssData", {}).get("baseScore")
                cvss_severity = cvss_v3.get("cvssData", {}).get("baseSeverity", "").lower()
                if cvss_severity:
                    severity = cvss_severity
            elif cvss_v2:
                cvss_score = cvss_v2.get("cvssData", {}).get("baseScore")
                if cvss_score >= 7.0:
                    severity = "high"
                elif cvss_score >= 4.0:
                    severity = "medium"
            
            # Map severity to enum values
            severity_map = {
                "critical": "critical",
                "high": "high",
                "medium": "medium",
                "low": "low"
            }
            severity = severity_map.get(severity, "low")
            
            # Extract description
            descriptions = cve.get("descriptions", [])
            description = ""
            for desc in descriptions:
                if desc.get("lang") == "en":
                    description = desc.get("value", "")
                    break
            
            # Create threat
            threat_data = schemas.ThreatCreate(
                cve_id=cve_id,
                title=f"CVE-{cve_id}" if cve_id else "Unknown Vulnerability",
                description=description,
                severity=severity,
                cvss_score=cvss_score,
                source="NVD",
                published_date=datetime.fromisoformat(cve.get("published", "").replace("Z", "+00:00"))
            )
            
            threat = crud.create_threat(db, threat_data)
            vulnerabilities.append(threat)
            
            # Send alert for critical vulnerabilities
            if severity == "critical":
                alert_service.send_telegram_alert(
                    f"🚨 CRITICAL VULNERABILITY DETECTED\n"
                    f"CVE: {cve_id}\n"
                    f"CVSS Score: {cvss_score}\n"
                    f"Description: {description[:200]}..."
                )
                alert_service.create_alert(db, threat.id, "critical_vulnerability", description[:500])
        
        logger.info(f"Collected {len(vulnerabilities)} new vulnerabilities from NVD")
        return vulnerabilities
        
    except Exception as e:
        logger.error(f"Error collecting NVD vulnerabilities: {str(e)}")
        return []

def collect_indicators(db: Session) -> List[Dict[str, Any]]:
    """Collect indicators of compromise from various sources"""
    # Example: Collect from CISA known exploited vulnerabilities
    indicators = []
    
    try:
        # This is a mock implementation - replace with actual threat intelligence feeds
        # In production, you would integrate with:
        # - AlienVault OTX
        # - MISP
        # - CISCO Talos
        # - VirusTotal
        # - AbuseIPDB
        
        mock_indicators = [
            {
                "type": "ip",
                "value": "192.168.1.100",
                "risk_score": 8.5,
                "source": "Mock Feed"
            },
            {
                "type": "domain",
                "value": "malicious-domain.com",
                "risk_score": 7.0,
                "source": "Mock Feed"
            },
            {
                "type": "hash",
                "value": "5d41402abc4b2a76b9719d911017c592",
                "risk_score": 9.0,
                "source": "Mock Feed"
            }
        ]
        
        for ind_data in mock_indicators:
            # Check if indicator already exists
            existing = crud.get_indicator_by_value(db, ind_data["value"])
            if existing:
                continue
            
            indicator = schemas.IndicatorCreate(
                indicator_type=ind_data["type"],
                indicator_value=ind_data["value"],
                risk_score=ind_data["risk_score"],
                source=ind_data["source"],
                metadata={"collected_at": datetime.now().isoformat()}
            )
            
            db_indicator = crud.create_indicator(db, indicator)
            indicators.append(db_indicator)
            
        logger.info(f"Collected {len(indicators)} new indicators")
        return indicators
        
    except Exception as e:
        logger.error(f"Error collecting indicators: {str(e)}")
        return []

def collect_all_threats(db: Session) -> Dict[str, Any]:
    """Collect all threats from all sources"""
    results = {
        "timestamp": datetime.now().isoformat(),
        "nvd_vulnerabilities": 0,
        "indicators": 0,
        "errors": []
    }
    
    try:
        # Collect from NVD
        nvd_threats = collect_nvd_vulnerabilities(db)
        results["nvd_vulnerabilities"] = len(nvd_threats)
        
        # Collect indicators
        indicators = collect_indicators(db)
        results["indicators"] = len(indicators)
        
        logger.info(f"Collection complete: {results}")
        return results
        
    except Exception as e:
        logger.error(f"Error in collect_all_threats: {str(e)}")
        results["errors"].append(str(e))
        return results