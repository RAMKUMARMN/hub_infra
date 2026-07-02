# CixioHub Infrastructure

This repository contains the infrastructure configuration, MQTT broker setup, and the intelligent AI router for the CixioHub ecosystem.

## Components

### 1. `ai/` (AI Router)
An intelligent routing engine built with Python and FastAPI that acts as a gateway for LLM requests. It analyzes incoming queries and intelligently routes them to specialized LLM models (e.g., Coding, Reasoning, Vision) or handles general requests using a lightweight router model. It relies on local Ollama models.

### 2. `terraform/`
Contains the Infrastructure as Code (IaC) definitions to provision AWS resources for the CixioHub cloud environment. 
Modules include:
- `vpc`: Core networking and security groups.
- `rds`: PostgreSQL database provisioning.
- `elasticache`: Redis cache setup.
- `s3`: Cloud storage buckets.

### 3. `mosquitto/`
Configuration for the Mosquitto MQTT broker, providing real-time bidirectional communication channels (WebSocket and TCP) for features such as chat, presence, and notifications.

## Development Setup
Please see `.setup-notes` for instructions on setting up your local environment.
