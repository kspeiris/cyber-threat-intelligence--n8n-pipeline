import requests
import os
from sqlalchemy.orm import Session
import logging
from datetime import datetime
from dotenv import load_dotenv

from . import models, schemas, crud

load_dotenv()
logger = logging.getLogger(__name__)

# Telegram configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message: str) -> bool:
    """Send alert via Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("Telegram credentials not configured")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        logger.info("Telegram alert sent successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error sending Telegram alert: {str(e)}")
        return False

def create_alert(db: Session, threat_id: int, alert_type: str, message: str) -> models.Alert:
    """Create an alert in the database"""
    # Get threat for severity
    threat = crud.get_threat(db, threat_id=threat_id)
    severity = threat.severity if threat else "low"
    
    alert_data = schemas.AlertCreate(
        threat_id=threat_id,
        alert_type=alert_type,
        message=message,
        severity=severity
    )
    
    db_alert = crud.create_alert(db, alert_data)
    
    # Send Telegram alert
    telegram_message = f"🔔 <b>Security Alert</b>\n"
    telegram_message += f"Type: {alert_type}\n"
    telegram_message += f"Severity: {severity.upper()}\n"
    telegram_message += f"Message: {message}\n"
    telegram_message += f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    send_telegram_alert(telegram_message)
    
    return db_alert