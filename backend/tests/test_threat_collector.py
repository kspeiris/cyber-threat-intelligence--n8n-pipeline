import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from app import threat_collector, schemas

def test_collect_nvd_vulnerabilities():
    """Test NVD vulnerability collection"""
    db = MagicMock()
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "vulnerabilities": [
            {
                "cve": {
                    "id": "CVE-2024-TEST",
                    "descriptions": [{"lang": "en", "value": "Test vulnerability"}],
                    "published": "2024-01-01T00:00:00.000Z",
                    "metrics": {
                        "cvssMetricV31": [
                            {
                                "cvssData": {
                                    "baseScore": 7.5,
                                    "baseSeverity": "HIGH"
                                }
                            }
                        ]
                    }
                }
            }
        ]
    }
    mock_response.raise_for_status = MagicMock()
    
    with patch("app.threat_collector.requests.get", return_value=mock_response):
        with patch("app.threat_collector.crud.get_threat_by_cve", return_value=None):
            with patch("app.threat_collector.crud.create_threat") as mock_create:
                mock_create.return_value = MagicMock(id=1, cve_id="CVE-2024-TEST", severity="high")
                with patch("app.threat_collector.alert_service") as mock_alert:
                    result = threat_collector.collect_nvd_vulnerabilities(db)
                    assert isinstance(result, list)

def test_collect_indicators():
    """Test indicator collection"""
    db = MagicMock()
    
    with patch("app.threat_collector.crud.get_indicator_by_value", return_value=None):
        with patch("app.threat_collector.crud.create_indicator") as mock_create:
            mock_create.return_value = MagicMock(id=1, indicator_value="192.168.1.1")
            result = threat_collector.collect_indicators(db)
            assert isinstance(result, list)