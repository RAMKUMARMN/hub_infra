---
name: discover-ci-cd
description: Analyze continuous integration, deployment pipelines, and GitHub Actions.
---

# Discover CI/CD Pipelines

Map the automated deployment and testing workflows.

## Focus Areas
- GitHub Actions workflows (`workflows/ci.yml`)
- Automated testing scripts (`ai/ai_router/tests/`)

## Goals
- Document the trigger conditions for builds and deployments.
- Verify the testing phases (Stress testing, validation).

## Output
Return:
- CI/CD pipeline execution graph

## Workflow
1. Route the hub folder agent to plugin/skills for this specific skill folder.
2. Invoke the native `discoverCiCd` tool to trace the workflow configurations.
3. Return the automation pipeline map.
