---
mode: agent
agent: infra-ci
name: infra-ci-prompt
description: "Prompt for the infra-ci agent. Creates and updates GitHub Actions CI workflows for Terraform validation, linting, planning, and gated apply across multiple environments."
---

### Requirements

1. **Workflow Triggers:** Push to `main` and `workflow_dispatch` with environment input. Optionally support PR triggers for plan-only.
2. **Jobs:** `fmt`, `validate`, `plan`, and `apply` stages. Plan must be environment-specific.
3. **Environment Matrix:** Support `dev`, `staging`, `prod` with environment-specific `tfvars` files and variable mappings.
4. **Approval Gates:** Production `apply` must require manual GitHub Environment approval. Non-prod may auto-apply.
5. **Linting:** Optional `tflint` integration with configurable severity.
6. **Notifications:** Post status to Slack or email via GitHub Secrets. Include plan summary in job output.
7. **State Backend:** Use `S3_STATE_BUCKET` and `DDB_LOCK_TABLE` GitHub Secrets for remote state config.

### Constraints

- GitHub Actions syntax — no third-party CI platforms
- Secrets referenced as `${{ secrets.SECRET_NAME }}` — never hardcode values
- Terraform version configurable via `terraform_version` input (default `1.7.0`)
- Use `hashicorp/setup-terraform` action for Terraform setup
- Destroy workflows must be manually dispatched with confirmation token

### Success Criteria

- Workflow runs without syntax errors on push
- `plan` outputs a summary that appears in the Actions run log
- `apply` for prod blocks until manual approval
- Notifications fire on completion and failure
- README snippet documents required secrets and environment setup

### Usage Template

```
Create/update an infra CI workflow with:
- Environments: [comma-separated list]
- Terraform version: [version]
- Approval required for: [environments]
- Notifications to: [Slack webhook secret name]
- [Optional] Include tflint job
- [Optional] Include terratest job
Show the diff and wait for my confirmation before applying.
```

### Chat Example

```
User: Create an infra.yml workflow for dev, staging, prod.
- Terraform 1.7.0
- Prod requires manual approval
- Slack notifications via SLACK_WEBHOOK_URL
- Include tflint
```

Agent (expected):
- Scans repo for existing workflow files and Terraform layout
- Drafts `infra.yml` with all requested jobs
- Shows diffs and waits for confirmation before applying patches
