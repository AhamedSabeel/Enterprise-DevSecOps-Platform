#!/bin/bash

set -e

BACKUP_DIR="disaster-recovery/backups/configuration"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

mkdir -p "$BACKUP_DIR"

echo "Starting infrastructure configuration backup..."

tar -czf "$BACKUP_DIR/infrastructure_backup_$TIMESTAMP.tar.gz" \
  docker-compose.yml \
  monitoring \
  incident-response \
  disaster-recovery/scripts

echo "Infrastructure configuration backup completed."

echo "Starting application configuration backup..."

tar -czf "$BACKUP_DIR/application_backup_$TIMESTAMP.tar.gz" \
  application

echo "Application configuration backup completed."

echo "All backups completed successfully."
