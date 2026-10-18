# Basic System Monitoring with Prometheus and Grafana

## 1. Introduction

This project demonstrates a basic monitoring system using Prometheus, Node Exporter, and Grafana. The purpose is to collect system metrics, monitor the status of monitoring services, and visualize metrics through interactive dashboards.

Docker Compose is used to run all three services together. Prometheus collects metrics, Node Exporter exposes system metrics, and Grafana displays the collected information using graphs and visualization panels.

## 2. How Does the Project Work?

The monitoring system works in the following sequence:

1. **Start the Services:** Docker Compose starts Prometheus, Node Exporter, and Grafana containers.
2. **Expose System Metrics:** Node Exporter exposes metrics through its HTTP endpoint on port `9100`.
3. **Configure Prometheus:** The `prometheus.yml` file specifies which targets Prometheus should monitor.
4. **Collect Metrics:** Prometheus scrapes the configured targets every 15 seconds and stores the collected metrics as time-series data.
5. **Verify Targets:** The Prometheus Targets page displays whether the configured endpoints are reachable. A target showing `UP` indicates that scraping is working.
6. **Connect Grafana:** Grafana is configured with Prometheus as its data source using the Docker service URL `http://prometheus:9090`.
7. **Create Visualizations:** PromQL queries retrieve metrics from Prometheus, and Grafana displays the results in dashboard panels.
8. **Monitor the System:** The dashboard can be used to observe available memory metrics and CPU-related metrics over time.

## 3. Project Architecture

```text
             Docker Compose
                   |
        +----------+----------+
        |          |          |
        v          v          v
   Prometheus  Node Exporter  Grafana
        ^          |
        |          |
        +----------+
        Scrapes metrics
        every 15 seconds

   Grafana queries Prometheus
              |
              v
      Monitoring Dashboard
       Memory and CPU Graphs
```

## 4. Technologies Used

- Docker Desktop
- Docker Compose
- Prometheus
- Node Exporter
- Grafana
- PromQL
- YAML configuration

## 5. Project Structure

```text
Monitoring_Lab/
├── README.md
├── docker-compose.yml
└── prometheus/
    └── prometheus.yml
```

**`docker-compose.yml`:** Defines the Prometheus, Node Exporter, and Grafana services, their ports, and the Prometheus configuration mount.

**`prometheus/prometheus.yml`:** Defines the scrape interval and monitoring targets.

**`README.md`:** Documents the setup, architecture, metric queries, and execution procedure.

## 6. Prometheus Configuration

The `prometheus/prometheus.yml` file contains the following configuration:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["prometheus:9090"]

  - job_name: "node-exporter"
    static_configs:
      - targets: ["node-exporter:9100"]
```

### Explanation

- `scrape_interval: 15s` tells Prometheus to collect metrics every 15 seconds.
- The `prometheus` target monitors the Prometheus service itself.
- The `node-exporter` target collects metrics exposed by Node Exporter.
- Docker service names allow the containers to communicate over their shared Docker network.

## 7. How to Run the Project

### Step 1: Open the project folder

```powershell
cd D:\DOML-LAB\Monitoring_Lab
```

### Step 2: Validate the configuration

```powershell
docker compose config --quiet
```

If no error appears, the configuration is valid.

### Step 3: Start the monitoring services

```powershell
docker compose up -d
```

Docker downloads the required images if they are not already available and starts the containers in the background.

### Step 4: Verify the containers

```powershell
docker compose ps
```

The Prometheus, Node Exporter, and Grafana containers should show a running status.

### Step 5: Check Prometheus targets

Open:

http://localhost:9090/targets

Verify that both `prometheus` and `node-exporter` show the `UP` status.

### Step 6: Open Grafana

Open:

http://localhost:3000

Sign in with the local credentials configured for the Grafana container.

### Step 7: Configure the Prometheus data source

1. Open **Connections → Data sources**.
2. Add a Prometheus data source.
3. Set the server URL to `http://prometheus:9090`.
4. Click **Save & test** and verify the connection.

### Step 8: Create a dashboard

1. Open **Dashboards** and create a new dashboard.
2. Add a visualization with Prometheus as the data source.
3. Select Code mode in the query editor.
4. Enter one of the PromQL queries provided below.
5. Apply the panel and save the dashboard.

## 8. PromQL Queries

### A. Available Memory

```promql
node_memory_MemAvailable_bytes
```

This query returns the available memory reported by Node Exporter, measured in bytes.

### B. CPU Idle Rate

```promql
rate(node_cpu_seconds_total{mode="idle"}[5m])
```

This query calculates the rate of increase of CPU idle time over the previous five minutes, separately for each matching CPU time series.

### C. Approximate CPU Usage Percentage

```promql
100 * (1 - avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])))
```

This query estimates CPU usage percentage from the proportion of time the CPU is not idle.

## 9. Expected Output

- All three Docker containers should start successfully.
- Prometheus should display both configured targets as `UP`.
- Grafana should successfully connect to Prometheus.
- The dashboard should display memory and CPU-related metric graphs.
- The metric graphs should update as new data is collected.

## 10. Limitations

This is a basic monitoring demonstration. In this configuration, Node Exporter runs inside a Linux Docker container and exposes metrics from its Linux environment. It does not automatically provide complete CPU and memory measurements for the Windows host.

The dashboard also does not include alert notifications or long-term external storage configuration.

## 11. Stopping the Services

To stop the monitoring containers, run:

```powershell
docker compose down
```

## 12. Conclusion

The project successfully demonstrates basic monitoring using Prometheus and Grafana. Prometheus collects metrics from configured targets, Node Exporter exposes system metrics, and Grafana visualizes the collected information through dashboard panels.
