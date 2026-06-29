---
name: infra-ci-workflow
description: Create a GitHub Actions workflow for Terraform CI/CD with fmt, validate, plan, and gated apply across multiple environments.
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Mon, 29 Jun 2026 00:00:00 GMT
---

# Infra CI Workflow

## Contents
- [Workflow Layout](#workflow-layout)
- [Triggers](#triggers)
- [Jobs](#jobs)
- [Environment Matrix](#environment-matrix)
- [Approval Gates](#approval-gates)
- [Notifications](#notifications)
- [Destroy Workflow](#destroy-workflow)

## Workflow Layout

```
.github/workflows/
├── infra.yml         # Main plan/apply pipeline
└── destroy.yml       # Guarded destroy
```

## Triggers

```yaml
on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        default: 'dev'
        type: choice
        options:
          - dev
          - staging
          - prod
```

## Jobs

### Recommended order

1. **fmt** — `terraform fmt -check -recursive`
2. **validate** — `terraform validate`
3. **tflint** (optional) — `tflint --format compact`
4. **plan** — `terraform plan -no-color -out=tfplan`
5. **apply** — `terraform apply tfplan` (manual gate for prod)

## Environment Matrix

```yaml
strategy:
  matrix:
    environment: [dev, staging, prod]
    tfvars:
      dev: dev.tfvars
      staging: staging.tfvars
      prod: prod.tfvars
```

Each environment gets its own plan. Use `tfvars` mapping to pass environment-specific values.

## Approval Gates

```yaml
environment:
  name: ${{ matrix.environment }}

# For prod, require manual approval
# Configure GitHub Environments with required reviewers
```

GitHub Environments allow you to set required reviewers for `prod` so the `apply` job blocks until approved.

## Notifications

Post workflow results:

```yaml
- name: Notify Slack
  if: always()
  uses: rtCamp/action-slack-notify@v2
  env:
    SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK_URL }}
    SLACK_TITLE: "Infra ${{ matrix.environment }} ${{ job.status }}"
    SLACK_MESSAGE: "Terraform ${{ github.workflow }} for ${{ matrix.environment }} ${{ job.status }}"
```

## Destroy Workflow

Create a separate `destroy.yml`:

```yaml
name: Destroy Infrastructure
on:
  workflow_dispatch:
    inputs:
      environment:
        required: true
        type: choice
        options: [dev, staging, prod]
      confirm:
        description: 'Type DESTROY to confirm'
        required: true

jobs:
  destroy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    if: inputs.confirm == 'DESTROY'
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
      - run: terraform destroy -auto-approve -var-file=${{ inputs.environment }}.tfvars
```

### Required Secrets

| Secret | Description |
|---|---|
| `S3_STATE_BUCKET` | Terraform state S3 bucket name |
| `DDB_LOCK_TABLE` | DynamoDB lock table name |
| `AWS_ACCESS_KEY_ID` | AWS access key for Terraform |
| `AWS_SECRET_ACCESS_KEY` | AWS secret access key |
| `SLACK_WEBHOOK_URL` | Slack webhook for notifications |
