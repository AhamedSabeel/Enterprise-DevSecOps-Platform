#!/bin/bash

set -e

echo "========================================"
echo "Enterprise DevSecOps Backup प्रक्रिया"
echo "========================================"

echo "Running database backup..."
./disaster-recovery/scripts/backup_database.sh

echo "Running configuration backup..."
./disaster-recovery/scripts/backup_configuration.sh

echo "Running persistent volume backup..."
./disaster-recovery/scripts/backup_volumes.sh

echo "Running infrastructure and application backup..."
./disaster-recovery/scripts/backup_infrastructure_application.sh

echo "Applying backup retention policy..."
./disaster-recovery/scripts/cleanup_old_backups.sh

echo "========================================"
echo "All backup operations completed successfully."
echo "========================================"
