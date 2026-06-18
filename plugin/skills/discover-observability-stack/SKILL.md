---
name: discover-observability-stack
description: Map OpenTelemetry tracing, Prometheus metrics, ELK logging, and Grafana dashboards.
---

# Discover Observability Stack

Analyze how the infrastructure monitors system health and AI performance.

## Focus Areas
- Distributed Tracing (OpenTelemetry)
- Metrics Collection (Prometheus)
- Centralized Logging (ELK Stack)
- Dashboards and Alerts (Grafana, AlertManager)

## Goals
- Document the cross-cutting monitoring layers defined in the architecture.
- Identify where metric scraping endpoints and log shippers are configured.

## Output
Return:
- Observability and telemetry topology map

## Workflow
1. Route the hub folder agent to plugin/skills for this specific skill folder.
2. Invoke `discoverInfraArchitecture` and `findResource` targeting "Prometheus", "Grafana", or "ELK".
3. Return the observability architecture map.
