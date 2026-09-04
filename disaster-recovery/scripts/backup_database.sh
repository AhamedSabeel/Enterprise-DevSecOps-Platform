#!/bin/bash

set -e

BACKUP_DIR="disaster-recovery/backups/database"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/enterprise_db_$TIMESTAMP.sql"

mkdir -p "$BACKUP_DIR"

echo "Starting PostgreSQL database backup..."

docker exec enterprise-postgres pg_dump \
  -U enterprise_user \
  enterprise_db > "$BACKUP_FILE"

echo "Database backup completed successfully."
echo "Backup file: $BACKUP_FILE"
