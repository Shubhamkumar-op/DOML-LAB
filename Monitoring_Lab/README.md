\# Experiment 8: Basic Monitoring with Prometheus and Grafana



\## Aim

To set up Prometheus to monitor system metrics and visualize them using Grafana dashboards.



\## Theory

Prometheus is an open-source monitoring tool that collects and stores metrics. Node Exporter provides system metrics, while Grafana displays the collected metrics using graphs and dashboards.



\## Tools Required

\- Docker Desktop

\- Prometheus

\- Grafana

\- Node Exporter



\## Procedure

1\. Created a project folder named `Monitoring\_Lab`.

2\. Configured Prometheus using `prometheus.yml`.

3\. Created a Docker Compose file for Prometheus, Grafana, and Node Exporter.

4\. Started the services using `docker compose up -d`.

5\. Verified the containers using `docker compose ps`.

6\. Checked Prometheus targets at http://localhost:9090/targets.

7\. Connected Prometheus to Grafana using `http://prometheus:9090`.

8\. Created a Grafana dashboard with memory and CPU metric panels.



\## Prometheus Queries



\*\*Memory:\*\*

```promql

node\_memory\_MemAvailable\_bytes

```



\*\*CPU idle time:\*\*

```promql

rate(node\_cpu\_seconds\_total{mode="idle"}\[5m])

```



\## Output

All three containers started successfully. Both Prometheus targets showed UP, and Grafana displayed the configured monitoring graphs.



\## Result

Basic system monitoring was successfully demonstrated using Prometheus and Grafana.



\## Screenshots

Attach the screenshots of the Prometheus Targets page and Grafana dashboard.



