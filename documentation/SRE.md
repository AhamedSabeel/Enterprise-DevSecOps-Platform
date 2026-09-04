# Site Reliability Engineering (SRE)

## 1. Service Level Indicators (SLI)

The platform uses the following Service Level Indicators:

### Availability SLI
Measures the percentage of successful HTTP requests.

Formula:

Successful Requests / Total Requests × 100

### Latency SLI
Measures HTTP request response time using Prometheus metrics.

Metric:

http_request_duration_seconds

### Error Rate SLI
Measures the percentage of failed HTTP requests.

Formula:

Failed Requests / Total Requests × 100


## 2. Service Level Objectives (SLO)

The platform defines the following reliability objectives:

- Availability SLO: 99.9%
- Error Rate SLO: Less than 0.1%
- Latency SLO: 95% of requests must complete within 500 milliseconds.


## 3. Service Level Agreement (SLA)

The platform reliability commitment is:

- Service Availability: 99.9%
- Maximum Error Rate: 0.1%
- Target Response Time: 95% of requests below 500 milliseconds.


## 4. Error Budget

The availability target is 99.9%.

This allows an error budget of:

0.1% failed requests.

The error budget represents the acceptable amount of service failure before the reliability objective is violated.


## 5. Availability Target

Target:

99.9% Availability

Prometheus metrics are used to monitor successful and failed HTTP requests.


## 6. Latency Target

Target:

95% of HTTP requests must complete within 500 milliseconds.

The following Prometheus metric is used:

http_request_duration_seconds


## 7. Recovery Objectives

The platform defines the following recovery objectives:

- Recovery Time Objective (RTO): 15 minutes
- Recovery Point Objective (RPO): 5 minutes

The monitoring and observability stack assists engineers in detecting failures and investigating incidents quickly.


## Reliability Monitoring

Grafana dashboards visualize:

- Request volume
- Service availability
- Error rate
- Request latency
- SLO compliance
- Error budget status

Prometheus collects the metrics used to measure these reliability objectives.
