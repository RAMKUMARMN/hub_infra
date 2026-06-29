---
applyTo: "**/*.tf,**/*.tfvars,**/*.hcl"
---

# Project coding standards for Terraform

Apply the [general coding guidelines](./general-coding.instructions.md) to all code.

## Terraform Guidelines
- Use Terraform >= 1.7.0 with `required_version` constraint
- Use AWS provider — all resources in `us-east-1` unless specified
- Store state in S3 with DynamoDB locking — never local state
- Use consistent module structure: `main.tf`, `variables.tf`, `outputs.tf`
- Tag all resources with `Environment`, `Project`, and `ManagedBy`
- Run `terraform fmt` before committing

## Module Guidelines
- Modules in `terraform/modules/<name>/` following the standard structure
- Each module has a clear single responsibility (VPC, RDS, Redis, S3)
- Expose all configurable values as variables with sensible defaults
- Document variables with descriptions in `variables.tf`
- Output all useful attributes (ARNs, endpoints, IDs) in `outputs.tf`

## Environment Guidelines
- Environments: `dev`, `staging`, `prod`
- Environment-specific values via `.tfvars` files (e.g., `prod.tfvars`)
- `terraform plan` must be reviewed before `terraform apply`
- Production `apply` requires manual approval — no auto-apply
- Use Terraform workspaces or directory separation per environment

## Security Guidelines
- Never hardcode secrets — use Terraform variables set in CI/CD secrets
- Follow least-privilege for IAM roles and policies
- Enable encryption at rest (RDS, S3, ElastiCache)
- Restrict public access — default-deny security groups and S3 bucket policies
- Enable VPC flow logs for network auditing

## Agent Guidelines

This repository uses the following agents:

| Agent | File | Purpose |
|---|---|---|
| `infra-agent` | `.github/agents/infra agent.agent.md` | Coordinator — routes to single-task agents |
| `infra-terraform` | `.github/agents/infra-terraform.agent.md` | Terraform modules (VPC, RDS, ElastiCache, S3) |
| `infra-mosquitto` | `.github/agents/infra-mosquitto.agent.md` | Mosquitto MQTT broker configuration |
| `infra-ci` | `.github/agents/infra-ci.agent.md` | GitHub Actions CI/CD workflows |
| `infra-planner` | `.github/agents/infra-planner.agent.md` | Implementation planning |
| `infra-code-reviewer` | `.github/agents/infra-code-reviewer.agent.md` | Code review before merge |

Prompts are in `.github/prompts/` and skills in `.agents/skills/`.

When asking for help, prefix your request with the agent name:
- "@infra-terraform Add an RDS module with PostgreSQL 16"
- "@infra-mosquitto Add a WebSocket listener on port 9001"
- "@infra-ci Create an infra.yml workflow for dev, staging, prod"
