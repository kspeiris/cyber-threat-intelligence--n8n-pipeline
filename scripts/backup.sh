#!/bin/bash

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "💾 Creating backup..."

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup PostgreSQL
docker exec threat_intelligence_db pg_dump -U user threat_intelligence > $BACKUP_DIR/threat_intelligence_$TIMESTAMP.sql

# Backup environment files
cp -r backend/.env $BACKUP_DIR/.env_$TIMESTAMP 2>/dev/null || echo "No .env file to backup"

echo "✅ Backup created at $BACKUP_DIR/threat_intelligence_$TIMESTAMP.sql"

# Remove backups older than 7 days
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name ".env_*" -mtime +7 -delete