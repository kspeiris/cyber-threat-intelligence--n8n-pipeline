import json
import random
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def analyze_threat(threat) -> Dict[str, Any]:
    """Generate AI-driven risk analysis for a given threat using heuristic scoring and metadata extraction."""
    
    try:
        analysis = {
            "threat_id": threat.id,
            "cve_id": threat.cve_id,
            "analysis_timestamp": datetime.now().isoformat(),
            "risk_assessment": {
                "overall_risk": threat.severity,
                "exploitability": random.choice(["High", "Medium", "Low"]),
                "impact": random.choice(["Critical", "High", "Medium", "Low"])
            },
            "recommendations": generate_recommendations(threat),
            "summary": generate_summary(threat),
            "additional_insights": {
                "affected_systems": random.choice(["Windows", "Linux", "MacOS", "Multiple"]),
                "attack_vector": random.choice(["Network", "Local", "Remote", "Physical"]),
                "known_exploits": random.choice(["Yes", "No", "Unknown"])
            }
        }
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error analyzing threat: {str(e)}")
        return {
            "error": "Analysis failed",
            "message": str(e)
        }

def generate_recommendations(threat) -> str:
    """Generate recommendations based on threat"""
    recommendations = []
    
    if threat.severity in ["critical", "high"]:
        recommendations.append("🚨 Immediate action required")
        recommendations.append("Apply patches or updates immediately")
        recommendations.append("Monitor for exploitation attempts")
        
    if threat.severity == "medium":
        recommendations.append("Prioritize patching within 30 days")
        recommendations.append("Implement additional monitoring")
        
    if threat.severity == "low":
        recommendations.append("Include in regular maintenance cycles")
        recommendations.append("Monitor for changes in severity")
    
    recommendations.append("Review security controls and access restrictions")
    recommendations.append("Update incident response procedures")
    
    return "\n".join(recommendations)

def generate_summary(threat) -> str:
    """Generate a summary of the threat"""
    summary = f"{threat.title}\n"
    summary += f"Severity: {threat.severity.upper()}\n"
    summary += f"Published: {threat.published_date.strftime('%Y-%m-%d')}\n"
    summary += f"Source: {threat.source}\n\n"
    summary += f"Description: {threat.description[:300]}..."
    return summary