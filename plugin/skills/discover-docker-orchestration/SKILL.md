---
name: discover-docker-orchestration
description: Map containerization strategies, Docker Compose services, and startup scripts.
---

# Discover Docker Orchestration

Analyze the local and containerized deployment architecture.

## Focus Areas
- Service definitions (`docker-compose.yml`)
- Container initialization (`start.sh`)
- Custom Dockerfiles (e.g., `ai/ai_router/Dockerfile`)

## Goals
- Identify all microservices running in the composed environment.
- Document port mappings, volume mounts, and network bridges.

## Output
Return:
- Container orchestration map
- Service networking matrix

## Workflow
1. Route the hub folder agent to plugin/skills for this specific skill folder.
2. Invoke the native `discoverInfraArchitecture` tool to map the root compose structures.
3. Use `findResource` targeting "Dockerfile" or "docker-compose".
4. Return the containerization architecture.
