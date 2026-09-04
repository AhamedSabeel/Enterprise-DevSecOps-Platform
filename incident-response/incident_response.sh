#!/bin/bash

PROJECT_DIR="$HOME/Enterprise-DevSecOps-Platform"
REPORT_DIR="$PROJECT_DIR/incident-response/reports"

mkdir -p "$REPORT_DIR"

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

generate_report() {
    SERVICE=$1
    INCIDENT=$2
    STATUS=$3

    REPORT_FILE="$REPORT_DIR/incident_${SERVICE}_${TIMESTAMP}.txt"

    {
        echo "========================================="
        echo "AUTOMATED INCIDENT RESPONSE REPORT"
        echo "========================================="
        echo "Timestamp: $(date)"
        echo "Affected Service: $SERVICE"
        echo "Incident Type: $INCIDENT"
        echo "Recovery Status: $STATUS"
        echo ""
        echo "Diagnostics:"
        docker compose ps
        echo ""
        echo "Recent Logs:"
        docker logs "enterprise-$SERVICE" --tail 30 2>&1
    } > "$REPORT_FILE"

    echo "Incident report generated: $REPORT_FILE"
}

check_backend() {

    echo "Checking Backend Service..."

    HEALTH=$(curl -s --max-time 5 http://localhost:8003/health)

    if [[ "$HEALTH" != *'"status":"healthy"'* ]]; then

        echo "INCIDENT DETECTED: Backend service unhealthy"

        echo "Collecting diagnostics..."

        docker compose ps backend
        docker logs enterprise-backend-integrated --tail 30

        echo "Attempting automated remediation..."

        docker compose up -d --force-recreate backend

        sleep 10

        HEALTH=$(curl -s --max-time 5 http://localhost:8003/health)

        if [[ "$HEALTH" == *'"status":"healthy"'* ]]; then
            echo "RECOVERY SUCCESSFUL"
            generate_report "backend-integrated" "Backend Service Failure" "Recovered Successfully"
        else
            echo "RECOVERY FAILED"
            generate_report "backend-integrated" "Backend Service Failure" "Recovery Failed"
        fi

    else
        echo "Backend service is healthy."
    fi
}

check_database() {

    echo "Checking PostgreSQL Service..."

    DB_STATUS=$(docker inspect -f '{{.State.Status}}' enterprise-postgres 2>/dev/null)

    if [[ "$DB_STATUS" != "running" ]]; then

        echo "INCIDENT DETECTED: PostgreSQL unavailable"

        echo "Collecting diagnostics..."

        docker compose ps postgres
        docker logs enterprise-postgres --tail 30 2>&1

        echo "Attempting automated remediation..."

        docker start enterprise-postgres

        sleep 10

        HEALTH=$(curl -s --max-time 5 http://localhost:8003/health)

        if [[ "$HEALTH" == *'"database":"healthy"'* ]]; then
            echo "RECOVERY SUCCESSFUL"
            generate_report "postgres" "Database Connection Failure" "Recovered Successfully"
        else
            echo "RECOVERY FAILED"
            generate_report "postgres" "Database Connection Failure" "Recovery Failed"
        fi

    else
        echo "PostgreSQL service is healthy."
    fi
}



check_auth_service() {

    echo "Checking Authentication Service..."

    HEALTH=$(curl -s --max-time 5 http://localhost:8001/health)

    if [[ "$HEALTH" != *'"status":"healthy"'* ]]; then

        echo "INCIDENT DETECTED: Authentication service unavailable"

        echo "Affected Service: auth-service"

        echo "Collecting diagnostics..."

        docker compose ps auth-service
        docker logs enterprise-auth-service --tail 30 2>&1

        echo "Running diagnostic checks..."

        docker inspect -f '{{.State.Status}}' enterprise-auth-service 2>/dev/null

        echo "Attempting automated remediation..."

        docker compose up -d --force-recreate auth-service

        sleep 10

        HEALTH=$(curl -s --max-time 5 http://localhost:8001/health)

        if [[ "$HEALTH" == *'"status":"healthy"'* ]]; then
            echo "RECOVERY SUCCESSFUL"
            generate_report "auth-service" "Authentication Service Unavailable" "Recovered Successfully"
        else
            echo "RECOVERY FAILED"
            generate_report "auth-service" "Authentication Service Unavailable" "Recovery Failed"
        fi

    else
        echo "Authentication service is healthy."
    fi
}



check_backend
check_database
check_auth_service
