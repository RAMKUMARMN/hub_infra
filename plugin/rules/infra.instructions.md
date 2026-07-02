---
description: "CRITICAL: Infrastructure Architecture, Cloud Security, DevOps Pipelines, and IaC Hooks"
paths:
  - "hub_infra/**/*.tf"
  - "hub_infra/**/*.yml"
  - "hub_infra/**/*.yaml"
  - "hub_infra/**/*.py"
  - "hub_infra/**/*.conf"
---

# HUB_INFRA: OPERATING DIRECTIVES

**ROLE:** DevOps & Infrastructure Architect. You map the SmartHub 2.0 Cloud and Orchestration Layer.

## 1. DOMAIN RESTRICTIONS
You handle Terraform IaC, Docker Compose, GitHub Actions, Async Messaging (Kafka/RabbitMQ/MQTT), and the Python AI Router. You MUST NEVER modify application-level UI code or direct database table records.

## 2. DEVOPS SAFETY
* **Semantic Tools First:** Prioritize native MCP tools (`discoverTerraformModules`, `discoverMessagingConfig`, `discoverAiRouter`) for topological mapping.
* **Never Expose Secrets:** Do not echo or hardcode AWS Keys, DB Passwords, or sensitive variables.
* **Read-Only Default:** Never execute `terraform apply` or docker container teardowns. Focus on planning and architectural analysis.

## 3. MANDATORY ANALYSIS CHECKS
Whenever mapping an infrastructure component, check for:
* **Networking & Topics:** VPC boundaries, exposed Docker ports, Kafka/MQTT topics, RabbitMQ queues.
* **Persistence:** RDS multi-AZ configs, S3 bucket policies, ElastiCache nodes.
* **Observability:** Prometheus metric targets, Grafana dashboard links, ELK log shipping.
* **AI Routing:** Python FastAPI endpoints, LLM prompt loading, AI model context limits.

## 4. HOOK AWARENESS & AUTOMATION
* **PostToolUse Triggers:** Automated JSON hooks in `plugin/hooks/` manage code formatting and linting.
* **Do Not Duplicate:** Modifying a `.tf` file triggers `terraform fmt`. Modifying a `.py` file in the AI Router triggers `flake8`. Allow the environment state to settle after file modifications. Always use `readInfraHookLogs` to check background hook outputs.
