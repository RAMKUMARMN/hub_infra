---
name: infra-multi-env
description: Manage Terraform infrastructure across dev, staging, and prod environments with environment-specific configuration files, variable overrides, and safety gates for production.
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Mon, 29 Jun 2026 00:00:00 GMT
---

# Multi-Environment Infrastructure Management

## Contents
- [Directory Layout](#directory-layout)
- [Environment Variables](#environment-variables)
- [tfvars Strategy](#tfvars-strategy)
- [Workspace vs Directory Separation](#workspace-vs-directory-separation)
- [Promotion Flow](#promotion-flow)
- [Safety Gates](#safety-gates)

## Directory Layout

### Option A: Single root with environment tfvars

```
terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── versions.tf
├── modules/
│   ├── vpc/
│   ├── rds/
│   ├── elasticache/
│   └── s3/
├── dev.tfvars
├── staging.tfvars
└── prod.tfvars
```

### Option B: Environment directories (stronger isolation)

```
terraform/
├── modules/
│   ├── vpc/
│   ├── rds/
│   ├── elasticache/
│   └── s3/
├── dev/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── backend.tf
│   └── terraform.tfvars
├── staging/
│   ├── main.tf
│   ...
└── prod/
    ├── main.tf
    ...
```

## Environment Variables

| Variable | Convention |
|---|---|
| `environment` | `"dev"`, `"staging"`, `"prod"` |
| `instance_class` | Smaller in dev, larger in prod |
| `multi_az` | `false` for dev/staging, `true` for prod |
| `backup_retention` | Short in dev, longer in prod |
| `alarm_evaluation_periods` | Higher in prod to reduce pager fatigue |

## tfvars Strategy

```hcl
# dev.tfvars
environment      = "dev"
instance_class   = "db.t3.medium"
multi_az         = false
backup_retention = 1
enable_alarms    = false

# staging.tfvars
environment      = "staging"
instance_class   = "db.t3.large"
multi_az         = false
backup_retention = 7
enable_alarms    = true

# prod.tfvars
environment      = "prod"
instance_class   = "db.r5.large"
multi_az         = true
backup_retention = 30
enable_alarms    = true
```

## Workspace vs Directory Separation

| Method | Pros | Cons |
|---|---|---|
| Workspaces | Single state file per workspace, simple | Workspace state stored together; risk of cross-workspace reference errors |
| Directories | Complete isolation, separate backends | More files, some duplication |

For `hub_infra`, use **directory separation** (Option B) for stronger production isolation.

## Promotion Flow

```
dev → plan/apply → staging → plan/apply → prod → plan (review) → apply (manual gate)
```

1. Changes are tested in `dev` first.
2. Same module code is promoted to `staging` with `staging.tfvars`.
3. After staging validation, create a PR for `prod` environment.
4. Production `apply` requires manual approval via GitHub Environments.

## Safety Gates

| Gate | Implementation |
|---|---|
| Plan review | `terraform plan` output is visible in CI logs before apply |
| Manual approval | GitHub Environment with required reviewers for `prod` |
| Confirmation token | Destroy workflows require typed `DESTROY` |
| State backup | S3 versioning on state bucket; rollback by restoring version |
| Change freeze | Optional CODEOWNERS approval for `prod/` directory changes |
