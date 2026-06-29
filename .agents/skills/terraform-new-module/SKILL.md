---
name: terraform-new-module
description: Create a new Terraform module with the standard structure: main.tf, variables.tf, outputs.tf, versions.tf. Follow the repo conventions for tagging, variable style, and documentation.
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Mon, 29 Jun 2026 00:00:00 GMT
---

# Creating a New Terraform Module

## Contents
- [Standard Structure](#standard-structure)
- [File Templates](#file-templates)
- [Variables](#variables)
- [Outputs](#outputs)
- [Tags](#tags)
- [Validation](#validation)

## Standard Structure

Every module in `terraform/modules/<name>/` follows this layout:

```
terraform/modules/
├── vpc/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── versions.tf
├── rds/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── versions.tf
└── <new-module>/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    └── versions.tf
```

## File Templates

### `main.tf`

```hcl
resource "aws_<resource>" "<name>" {
  # Configuration specific to this resource

  tags = local.tags
}

locals {
  name_prefix = var.name_prefix != null ? var.name_prefix : "hub-${var.environment}"
  tags = {
    Environment = var.environment
    Project     = var.project
    ManagedBy   = "terraform"
  }
}
```

### `variables.tf`

```hcl
variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "project" {
  description = "Project name for resource tagging"
  type        = string
  default     = "hub"
}

variable "name_prefix" {
  description = "Optional prefix for resource names. Defaults to hub-{environment}."
  type        = string
  default     = null
}
```

### `outputs.tf`

```hcl
output "<resource>_id" {
  description = "The ID of the <resource>"
  value       = aws_<resource>.<name>.id
}

output "<resource>_arn" {
  description = "The ARN of the <resource>"
  value       = aws_<resource>.<name>.arn
}
```

### `versions.tf`

```hcl
terraform {
  required_version = ">= 1.7.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

## Variables

| Convention | Guideline |
|---|---|
| Type | Always specify `type` — avoid `any` |
| Description | Always provide `description` |
| Default | Provide sensible defaults; use `null` for required vars |
| Validation | Use `validation` blocks for enum-like constraints |
| Sensitive | Mark `sensitive = true` for secrets/passwords |

## Outputs

- Export all useful attributes: `id`, `arn`, `endpoint`, `security_group_id`, `subnet_ids`
- Use descriptive names prefixed by the resource type (e.g., `rds_endpoint`)
- Always include `description`

## Tags

All resources must have these tags:

| Tag | Source |
|---|---|
| `Environment` | `var.environment` |
| `Project` | `var.project` (default `"hub"`) |
| `ManagedBy` | `"terraform"` |

Use a `locals` block in `main.tf` for the tag map and reference it in every resource.

## Validation

1. `terraform fmt <module-dir>`
2. `terraform validate <module-dir>`
3. Verify all variables appear in `main.tf` and all outputs reference real resource attributes.
