---
name: infra-agent-skills
description: Skills for the `hub_infra` assistant: Terraform module creation, Mosquitto MQTT config, GitHub Actions CI workflows, S3 backend setup, and multi-environment infrastructure management. The coordinator routes requests to single-task agents.
---

# Infra Agent — Skills Catalog

This document describes the skills, inputs/outputs, tools, safety constraints, and example prompts the `infra-agent` (see `infra agent.agent.md`) supports for the `hub_infra` repository.

**Purpose**
- Provide a compact, discoverable list of the agent's actionable capabilities so maintainers can quickly know what to ask and what to expect.

**Quick summary**
- **Primary domain:** Terraform-based AWS infrastructure (modules, top-level config, state backends), Mosquitto MQTT broker, and GitHub Actions CI/CD.
- **Primary outputs:** repository patches/diffs, Mosquitto config files, GitHub Actions workflow files, CI job templates, README snippets, and PR-ready descriptions.
- **Primary safety posture:** Prepare and validate IaC; never autonomously modify live production state without explicit maintainer confirmation.

## Capabilities

### Terraform (handled by `infra-terraform` agent)
- Create or update Terraform modules: VPC, RDS, ElastiCache, S3
- Standard module structure: `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`
- Resource tagging, encryption, and security best practices
- Variable typing, validation blocks, and output documentation

### Mosquitto MQTT (handled by `infra-mosquitto` agent)
- Configure listeners (MQTT, MQTTS, WS, WSS) with port and protocol settings
- Set up password-file or auth-plugin authentication
- Define ACL rules for topic-level access control
- Configure bridges to upstream MQTT brokers
- Set TLS certificate paths and cipher configuration

### CI/CD Workflows (handled by `infra-ci` agent)
- Generate or update GitHub Actions workflows for `terraform fmt`, `validate`, `plan`, `apply`
- Per-environment workflows or a single multi-environment workflow
- Linter integration (`tflint`)
- Manual approval gates for production environments
- Slack notifications

### Infrastructure Skills (reusable guides in `.agents/skills/`)
- `terraform-s3-backend` — S3 state backend with DynamoDB locking
- `terraform-new-module` — Standard module creation template
- `infra-mosquitto-setup` — Mosquitto broker configuration guide
- `infra-ci-workflow` — GitHub Actions CI/CD workflow template
- `infra-multi-env` — Multi-environment tfvars and promotion strategy

## Inputs the agent expects (ask if missing)
- `environment` — which environment to target: `dev`, `staging`, `prod`
- `module` — which Terraform module to create or modify
- `listener` — port and protocol for Mosquitto MQTT
- `s3_state_bucket` or `S3_STATE_BUCKET` secret — Terraform state bucket
- `dynamodb_lock_table` or `DDB_LOCK_TABLE` secret — optional lock table
- `aws_region` — region to use (default `us-east-1` if unspecified)
- `terraform_version` — Terraform version for CI workflows (default `1.7.0`)

## Outputs the agent produces
- New or modified Terraform module files
- Mosquitto configuration files
- Workflow YAML files in `/.github/workflows/`
- README / docs snippets describing required secrets and usage
- PR-ready changelog/summary and verification checklist
- Patches (diffs) applied with agent tools when given explicit permission

## Tools the agent uses
- Repository editing tools for making focused edits
- File search and read tools to inspect repo layout and find relevant files
- Progress tracking tools to manage multi-step tasks

## Safety, boundaries, and policies

- Never request or accept raw secrets in chat messages. Instead, ask for secret *names* and instruct maintainers to set them in GitHub Secrets.
- Never perform `terraform apply` against production without an explicit confirmation token: `CONFIRM_PROD_CHANGE`
- No direct cloud API operations — prepare IaC changes only
- No automatic PR merging or repo-level approvals — draft and explain only

## Confirmation and escalation rules
- Low-risk edits (formatting, docs): apply patches after a single maintainer approval
- Medium-risk edits (module changes, variable additions): require explicit approval before applying
- High-risk edits (changes that modify production applies, state backend, or sensitive variables): require `CONFIRM_PROD_CHANGE` and a second acknowledgment

## Example prompts (how to ask the agent)

### Terraform
- "Add `backup_retention` variable to `modules/rds` with documentation and update README — show me the patch before applying."
- "Create a new ElastiCache Redis module with encryption, multi-AZ, and CloudWatch alarms."

### Mosquitto MQTT
- "Add a WebSocket listener on port 9001 with TLS enabled."
- "Configure a bridge to `mqtt.example.com:1883` forwarding `sensors/#`."

### CI Workflows
- "Create an `infra.yml` workflow supporting `dev`, `staging`, `prod` with manual approval for prod apply."
- "Add a `tflint` job to the existing infra workflow."

## Agent Architecture

The coordinator (`infra-agent`) routes to single-task agents:

| Agent | Responsibility |
|---|---|
| `infra-terraform` | Terraform modules and resources |
| `infra-mosquitto` | Mosquitto MQTT broker config |
| `infra-ci` | GitHub Actions CI workflows |
| `infra-planner` | Implementation planning |
| `infra-code-reviewer` | Code review before merge |

## How progress is reported
- Each agent breaks tasks into steps and reports current/completed steps

## Where to find configuration
- Agent configs: `/.github/agents/*.agent.md`
- Prompts: `/.github/prompts/*.prompt.md`
- Skills: `/.agents/skills/*/SKILL.md`
- Hooks: `/.github/hooks/*.json`
- General guidelines: `/.github/copilot-instructions.md`

## Maintenance notes
- Keep `SKILLS.md` aligned with individual agent files and prompts
- When adding a new skill, create `/.agents/skills/<name>/SKILL.md` and update this catalog
- When adding a new single-task agent, create the agent file, prompt file, register it in the coordinator's handoffs, and add to `opencode.jsonc`
