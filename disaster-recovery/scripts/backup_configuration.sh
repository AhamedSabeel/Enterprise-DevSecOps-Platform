#!/bin/bash

set -e

BACKUP_DIR="disaster-recovery/backups/configuration"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/configuration_backup_$TIMESTAMP.tar.gz"

mkdir -p "$BACKUP_DIR"

echo "Starting configuration backup..."

tar -czf "$BACKUP_FILE" \
  docker-compose.yml \
  monitoring \
  incident-response \
  disaster-recovery/scripts

echo "Configuration backup completed successfully."
echo "Backup file: $BACKUP_FILE"
