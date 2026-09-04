import subprocess
import json
from datetime import datetime
from pathlib import Path


REPORT_DIR = Path("ai-operations/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_DATA_DIR = Path("ai-operations/sample-data")


def run_command(command):
    """Execute a shell command and return the output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.strip()

    except Exception as error:
        return f"COMMAND ERROR: {error}"


def collect_container_logs():
    """Collect recent logs from important containers."""

    containers = [
        "enterprise-backend-load-balancer",
        "enterprise-postgres",
        "enterprise-redis",
        "enterprise-auth-service",
        "enterprise-worker"
    ]

    collected_logs = {}

    for container in containers:
        output = run_command(
            f"docker logs --tail 100 {container} 2>&1"
        )
        collected_logs[container] = output

    return collected_logs


def collect_historical_incidents():
    """Collect historical incident logs for operational analysis."""

    incidents = {}

    if not SAMPLE_DATA_DIR.exists():
        return incidents

    for log_file in SAMPLE_DATA_DIR.glob("*.log"):
        try:
            incidents[f"Historical Incident: {log_file.name}"] = (
                log_file.read_text()
            )
        except Exception:
            pass

    return incidents


def classify_error(line):
    """Classify common DevOps and application errors."""

    line_lower = line.lower()

    # DNS / service discovery errors
    if (
        "could not translate host name" in line_lower
        or "name resolution" in line_lower
        or "dns" in line_lower
    ):
        return "DNS / Service Discovery Error"

    # Database errors
    if (
        "database" in line_lower
        or "postgres" in line_lower
        or "psycopg2" in line_lower
        or "sqlalchemy" in line_lower
    ):
        return "Database Error"

    # Container errors
    if (
        "crashloop" in line_lower
        or "exit code" in line_lower
        or "container terminated" in line_lower
        or "oom" in line_lower
    ):
        return "Container Error"

    # Network errors
    if (
        "connection refused" in line_lower
        or "network" in line_lower
        or "timeout" in line_lower
    ):
        return "Network Error"

    # Application errors
    if (
        "exception" in line_lower
        or "traceback" in line_lower
        or "error" in line_lower
        or "failed" in line_lower
    ):
        return "Application Error"

    return "Unknown Error"


def analyze_logs(logs):
    """Analyze logs and identify warnings and errors."""

    findings = []

    keywords = [
        "error",
        "exception",
        "traceback",
        "failed",
        "warning",
        "crashloop",
        "exit code",
        "temporary failure"
    ]

    for source, content in logs.items():

        lines = content.splitlines()

        for line in lines:

            if any(
                keyword in line.lower()
                for keyword in keywords
            ):

                findings.append({
                    "source": source,
                    "log": line.strip(),
                    "classification": classify_error(line)
                })

    return findings


def collect_container_stats():
    """Collect CPU and memory usage from Docker."""

    output = run_command(
        "docker stats --no-stream "
        "--format '{{json .}}'"
    )

    stats = []

    for line in output.splitlines():

        try:
            stats.append(json.loads(line))
        except json.JSONDecodeError:
            pass

    return stats


def analyze_performance(stats):
    """Identify potential performance anomalies."""

    anomalies = []

    for container in stats:

        name = container.get("Name", "Unknown")
        cpu = container.get("CPUPerc", "0%")
        memory = container.get("MemPerc", "0%")

        try:
            cpu_value = float(cpu.replace("%", ""))
            memory_value = float(memory.replace("%", ""))

            if cpu_value > 80:
                anomalies.append(
                    f"High CPU usage detected in {name}: {cpu}"
                )

            if memory_value > 80:
                anomalies.append(
                    f"High memory usage detected in {name}: {memory}"
                )

        except ValueError:
            pass

    return anomalies


def suggest_root_cause(findings, anomalies):
    """Generate root-cause suggestions."""

    suggestions = []

    classifications = {
        finding["classification"]
        for finding in findings
    }

    if "DNS / Service Discovery Error" in classifications:
        suggestions.append(
            "Possible DNS or service discovery failure detected. "
            "Check service names, Kubernetes DNS resolution, "
            "network configuration, and namespace settings."
        )

    if "Database Error" in classifications:
        suggestions.append(
            "Possible database connectivity issue detected. "
            "Check PostgreSQL health, credentials, database URL, "
            "and network connectivity."
        )

    if "Network Error" in classifications:
        suggestions.append(
            "Possible network or service communication problem. "
            "Check Docker networking, service availability, "
            "ports, and connectivity between services."
        )

    if "Application Error" in classifications:
        suggestions.append(
            "Application-level failure detected. "
            "Review application logs, recent deployments, "
            "configuration changes, and dependency availability."
        )

    if "Container Error" in classifications:
        suggestions.append(
            "Container instability detected. "
            "Check restart counts, CrashLoopBackOff events, "
            "application startup failures, and resource limits."
        )

    if anomalies:
        suggestions.append(
            "Resource utilization anomaly detected. "
            "Investigate workload patterns and consider "
            "scaling or infrastructure optimization."
        )

    if not suggestions:
        suggestions.append(
            "No major operational issues detected during this analysis."
        )

    return suggestions


def generate_incident_summary(findings, anomalies):
    """Generate a simple incident summary."""

    if not findings and not anomalies:
        return (
            "No significant incidents or performance anomalies "
            "were detected during the analysis period."
        )

    summary = []

    if findings:
        sources = {
            finding["source"]
            for finding in findings
        }

        summary.append(
            f"{len(findings)} operational log finding(s) "
            f"detected from {len(sources)} source(s)."
        )

    if anomalies:
        summary.append(
            f"{len(anomalies)} performance anomaly/anomalies detected."
        )

    classifications = {}

    for finding in findings:
        category = finding["classification"]
        classifications[category] = (
            classifications.get(category, 0) + 1
        )

    if classifications:
        main_categories = ", ".join(classifications.keys())

        summary.append(
            f"Primary incident categories: {main_categories}."
        )

    return " ".join(summary)


def generate_report(findings, anomalies, suggestions, stats):
    """Generate a Markdown operational report."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = f"""# AI-Assisted DevOps Operational Report

## Report Information

- Generated: {timestamp}
- Platform: Enterprise DevSecOps Platform
- Analysis Type: Automated Operational Intelligence

---

## 1. Log Analysis

Total operational findings: **{len(findings)}**

"""

    if findings:

        for finding in findings[:20]:

            report += (
                f"- **Source:** {finding['source']}\n"
                f"  - **Classification:** "
                f"{finding['classification']}\n"
                f"  - **Log:** `{finding['log']}`\n\n"
            )

    else:
        report += "No significant errors or warnings detected.\n"

    report += "\n---\n\n## 2. Error Classification\n\n"

    if findings:

        classifications = {}

        for finding in findings:
            category = finding["classification"]

            classifications[category] = (
                classifications.get(category, 0) + 1
            )

        for category, count in classifications.items():
            report += f"- **{category}:** {count}\n"

    else:
        report += "No errors classified during this analysis.\n"

    report += "\n---\n\n## 3. Incident Summary\n\n"

    report += generate_incident_summary(
        findings,
        anomalies
    )

    report += "\n\n---\n\n## 4. Root Cause Suggestions\n\n"

    for suggestion in suggestions:
        report += f"- {suggestion}\n"

    report += "\n---\n\n## 5. Performance Anomaly Analysis\n\n"

    if anomalies:

        for anomaly in anomalies:
            report += f"- ⚠️ {anomaly}\n"

    else:

        report += (
            "No critical CPU or memory utilization anomalies "
            "were detected.\n"
        )

    report += "\n---\n\n## 6. Infrastructure Utilization\n\n"

    for container in stats:

        report += (
            f"- **{container.get('Name')}** "
            f"| CPU: {container.get('CPUPerc')} "
            f"| Memory: {container.get('MemUsage')}\n"
        )

    report += """

---

## Conclusion

The AI-Assisted DevOps Operations proof-of-concept automatically
collects live operational data from the Docker environment and can
also analyze historical incident logs.

The system performs automated log analysis, error classification,
incident summarization, root-cause suggestions, performance anomaly
identification, and infrastructure utilization analysis.

The component assists DevOps engineers with troubleshooting and
operational decision-making. It does not autonomously modify
production infrastructure.
"""

    filename = (
        REPORT_DIR /
        f"operational-report-"
        f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    )

    filename.write_text(report)

    return filename


def main():

    print("=" * 60)
    print("AI-ASSISTED DEVOPS OPERATIONS ANALYSIS")
    print("=" * 60)

    print("\n[1/5] Collecting live container logs...")

    logs = collect_container_logs()

    print("[2/5] Loading historical incident logs...")

    historical_logs = collect_historical_incidents()

    logs.update(historical_logs)

    print("[3/5] Analyzing logs and classifying errors...")

    findings = analyze_logs(logs)

    print("[4/5] Collecting infrastructure utilization "
          "and identifying anomalies...")

    stats = collect_container_stats()

    anomalies = analyze_performance(stats)

    print("[5/5] Generating incident summary, "
          "root-cause suggestions and report...")

    suggestions = suggest_root_cause(
        findings,
        anomalies
    )

    report = generate_report(
        findings,
        anomalies,
        suggestions,
        stats
    )

    print("\nAnalysis completed successfully.")
    print(f"Operational report generated: {report}")
    print(f"Log findings: {len(findings)}")
    print(f"Performance anomalies: {len(anomalies)}")


if __name__ == "__main__":
    main()
