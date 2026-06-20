#!/bin/bash

BACKUP_DIR="./backups"

echo "📥 Restoring backup..."

# Find latest backup
LATEST_BACKUP=$(ls -t $BACKUP_DIR/*.sql 2>/dev/null | head -n 1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "❌ No backup found in $BACKUP_DIR"
    exit 1
fi

echo "Using backup: $LATEST_BACKUP"

# Restore PostgreSQL
cat $LATEST_BACKUP | docker exec -i threat_intelligence_db psql -U user threat_intelligence

echo "✅ Backup restored successfully!"