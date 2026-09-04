#!/bin/bash

set -e

RETENTION_DAYS=7

echo "Removing backups older than $RETENTION_DAYS days..."

find disaster-recovery/backups/database \
  -type f \
  -mtime +$RETENTION_DAYS \
  -delete

find disaster-recovery/backups/configuration \
  -type f \
  -mtime +$RETENTION_DAYS \
  -delete

find disaster-recovery/backups/volumes \
  -type f \
  -mtime +$RETENTION_DAYS \
  -delete

echo "Backup retention cleanup completed successfully."
