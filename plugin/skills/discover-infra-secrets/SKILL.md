---
name: discover-infra-secrets
description: Map environment variable schemas, secret injections, and configuration keys.
---

# Discover Infrastructure Secrets

Analyze how the infrastructure securely manages environment-specific configurations.

## Focus Areas
- Environment schemas (`.env.example`, `terraform.tfvars.example`)
- Config loaders (`ai/ai_router/app/core/config.py`)

## Goals
- Map required variables for successful deployment.
- Verify that no hardcoded secrets exist in the repository.

## Output
Return:
- Environment configuration schema

## Workflow
1. Route the hub folder agent to plugin/skills for this specific skill folder.
2. Invoke the `discoverEnvironmentVariables` tool.
3. Return the mapped configuration schema safely.
