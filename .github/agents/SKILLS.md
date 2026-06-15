---
name: infra-agent-skills
description: Skills for the `hub_infra` assistant: GitHub Actions workflow generation, Terraform configuration, state backend setup, and safe IaC maintenance. The agent helps maintainers set up and manage Terraform-based infrastructure in the repository, with a strong emphasis on safety and human oversight for production-impacting changes.
---
# Infra Agent — Skills Catalog

This document describes the skills, inputs/outputs, tools, safety constraints, and example prompts the `infra-agent` (see `infra agent.agent.md`) supports for the `hub_infra` repository.

**Purpose**
- Provide a compact, discoverable list of the agent's actionable capabilities so maintainers can quickly know what to ask and what to expect.

**Quick summary**
- **Primary domain:** Terraform-based AWS infrastructure (modules, top-level config, state backends).
- **Primary outputs:** repository patches/diffs, GitHub Actions workflow files, CI job templates, README snippets, and PR-ready descriptions.
- **Primary safety posture:** Prepare and validate IaC; never autonomously modify live production state without explicit maintainer confirmation.

## Capabilities

- Generate or update GitHub Actions workflows to run `terraform fmt`, `terraform validate`, `terraform plan`, and (when authorized) `terraform apply`.
- Create per-environment workflows or a single multi-environment workflow accepting an `environment` input (`dev`, `staging`, `prod`).
- Configure Terraform remote state in S3 and (recommended) DynamoDB for locking; generate backend config and suggested secret names.
- Produce repository patches via `apply_patch` (small, focused edits) and provide diffs for review before applying.
- Run static checks in CI: `terraform fmt`, `terraform validate`, optional `tflint` integration.
- Outline integration test jobs (TerraTest/Inspec) and provide example test harness snippets.
- Draft PR descriptions, risk notes, and post-apply verification checklists.
- Create a safe `destroy` job template guarded by typed confirmation and restricted to manual dispatch.

## Inputs the agent expects (ask if missing)
- `environment` — which environment to target: `dev`, `staging`, `prod`.
- `s3_state_bucket` or repo secret name `S3_STATE_BUCKET` — Terraform state bucket.
- `dynamodb_lock_table` or repo secret name `DDB_LOCK_TABLE` — optional lock table.
- `aws_region` — region to use (default `us-east-1` if unspecified).
- `tfvar_files` or mapping of `tfvars` for environment-specific values (non-sensitive examples OK in repo; sensitive values must be in GitHub Secrets.)
- `notification` config — repo secret name for `SLACK_WEBHOOK_URL` or `NOTIFICATION_EMAIL`.

## Outputs the agent produces
- New or modified workflow YAML files in `/.github/workflows/` (e.g., `infra.yml`).
- README / docs snippets describing required secrets and how to run the workflow.
- PR-ready changelog/summary and verification checklist.
- Patches (diffs) applied with `apply_patch` when given explicit permission.

## Tools the agent uses
- `apply_patch` — create or update repo files (used only after human confirmation for impactful changes).
- `read_file`, `file_search`, `grep_search` — inspect repo layout and find modules or TF files.
- `manage_todo_list` — track multi-step tasks and report progress back to the maintainer.
- `run_in_terminal` — only if explicitly requested; otherwise the agent outputs commands for maintainers to run locally or in CI.

## Safety, boundaries, and policies

- Never request or accept raw secrets in chat messages. Instead, the agent asks for secret *names* (e.g., `S3_STATE_BUCKET`, `AWS_ACCESS_KEY_ID`) and instructs maintainers to set them in GitHub Secrets.
- Never perform `terraform apply` against production without an explicit confirmation token: `CONFIRM_PROD_CHANGE` (maintainer must provide this token before the agent takes any action that would modify `prod` Terraform configs or automated apply steps).
- No direct cloud API operations (no create/delete of cloud resources outside Terraform flows prepared in the repo).
- No automatic PR merging or repo-level approvals — the agent drafts, explains, and optionally creates patches/PRs after explicit permission.

## Confirmation and escalation rules
- Low-risk edits (formatting, docs, `terraform fmt` enforcement): agent may apply patches after a single maintainer approval.
- Medium-risk edits (module changes, variable additions that do not change production applies): require an explicit approval message before applying patches.
- High-risk edits (changes that enable or run `apply` in `prod`, change state backend, or alter sensitive variables): require the typed confirmation `CONFIRM_PROD_CHANGE` and a second acknowledgment (e.g., "I understand this will affect production state").

## Example prompts (how to ask the agent)
- "Create a single `infra.yml` workflow that supports `dev`, `staging`, `prod`; use `S3_STATE_BUCKET` and `DDB_LOCK_TABLE` repo secrets; require approval for `prod` applies; post results to Slack via `SLACK_WEBHOOK_URL`."
- "Add a `backup_retention` variable to `modules/rds` with documentation and update `README` — show me the patch before applying."
- "Draft a `destroy` workflow that requires typed confirmation `DESTROY` and logs the operator who invoked it."

## Typical workflows the agent supports

1. Discovery: scan repo for `modules/*`, `main.tf`, `variables.tf`, and existing `tfvars` files.
2. Draft: create a draft `infra.yml` with `fmt`, `validate`, `plan` stages and optional `tflint` and integration-test jobs.
3. Review: produce a PR description, risk summary, and required secrets docs.
4. Apply (human-gated): upon confirmation, the agent can apply small, non-production patches or add CI steps; production applies require `CONFIRM_PROD_CHANGE`.

## Minimal IAM guidance (examples, non-exhaustive)
- Use least-privilege policies for the CI role or user. Example capabilities your Actions runner needs (granular policies recommended):
  - S3: `s3:GetObject`, `s3:PutObject`, `s3:DeleteObject`, `s3:ListBucket` on the state bucket.
  - DynamoDB: `dynamodb:PutItem`, `dynamodb:GetItem`, `dynamodb:DeleteItem`, `dynamodb:Query` on lock table.
  - STS: `sts:AssumeRole` (if using cross-account roles) limited by `Condition`.
  - RDS / ElastiCache / EC2 / other services: permissions required only for the resources Terraform will manage; prefer scoped roles per-module.

## Error handling & troubleshooting behavior
- If `terraform validate` or `tflint` fails, the agent returns a concise diagnostics summary and suggests fixes.
- If `terraform plan` shows unexpected deletes or high-risk changes, the agent highlights them, explains likely causes, and recommends rollback or manual inspection steps.

## How progress is reported
- The agent uses `manage_todo_list` to break tasks into steps (discover → draft → patch → verify) and will report the current step and completed steps in chat messages.

## Where to find the agent's configuration and prompts
- Agent behavior is documented in `/.github/agents/infra agent.agent.md` and the repository prompt lives at `/.github/prompts/infra-prompt.prompt.md`.

## Maintenance notes
- Keep `SKILLS.md` aligned with `infra agent.agent.md` and `infra-prompt.prompt.md` — update all three when adding new capabilities (for example, support for a new linter or a different test harness).

---
If you'd like, I can now create or update a `/.github/workflows/infra.yml` based on these skills, or edit `SKILLS.md` wording to be more terse or more detailed for new maintainers.
