# Site Reliability Engineering – Reliability Objectives

## 1. Service Level Indicators (SLIs)

The following indicators are used to measure platform reliability:

### Availability SLI
Percentage of successful service health checks.

Availability SLI = Successful Requests / Total Requests × 100

### Latency SLI
Measures the response time of backend API requests.

### Error Rate SLI
Measures the percentage of failed requests.

Error Rate = Failed Requests / Total Requests × 100

### Recovery Time SLI
Measures the time required for a failed service to recover and become healthy.

---

## 2. Service Level Objectives (SLOs)

| Metric | Objective |
|---|---|
| Availability | ≥ 99.5% |
| Successful Requests | ≥ 99.5% |
| Error Rate | ≤ 0.5% |
| API Latency | 95% of requests below 2 seconds |
| Recovery Time | Service recovery within 5 minutes |

---

## 3. Service Level Agreements (SLAs)

The Enterprise DevSecOps Platform targets:

- 99.5% monthly service availability.
- Maximum error rate of 0.5%.
- 95% of API requests should complete within 2 seconds.
- Critical services should recover within 5 minutes.

---

## 4. Error Budget

The availability target is 99.5%.

This allows:

Error Budget = 100% - 99.5%

Error Budget = 0.5%

For a 30-day month:

30 days × 24 hours = 720 hours

Allowed downtime:

0.5% of 720 hours = 3.6 hours

Therefore, the monthly error budget allows approximately 3 hours and 36 minutes of downtime.

---

## 5. Availability Target

The platform availability target is:

≥ 99.5%

Availability is measured using Prometheus monitoring and service health metrics.

---

## 6. Latency Target

The latency objective is:

95% of backend API requests should complete within 2 seconds.

Slow requests are investigated using Prometheus metrics and Jaeger distributed tracing.

---

## 7. Recovery Objectives

Recovery objectives for critical services:

| Objective | Target |
|---|---|
| Detection Time | Within 1 minute |
| Recovery Time | Within 5 minutes |
| Monitoring Detection | Prometheus |
| Root Cause Investigation | Jaeger and Grafana |
