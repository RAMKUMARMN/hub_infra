---
mode: agent
agent: infra-terraform
name: infra-terraform-prompt
description: "Prompt for the infra-terraform agent. Creates or updates Terraform modules (VPC, RDS, ElastiCache, S3) with consistent structure, proper variable typing, and security best practices."
---

### Requirements

1. **Module Structure:** Follow the standard module layout: `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`.
2. **Resource Tags:** All resources must be tagged with `Environment`, `Project`, and `ManagedBy`.
3. **Encryption:** Enable encryption at rest for RDS, ElastiCache, and S3. Enable encryption in transit where supported.
4. **Backend:** Modules assume S3 backend with DynamoDB locking — never use local state.
5. **Variables:** Expose all configurable values as typed variables with descriptions and sensible defaults. Use `nullable` and `validation` blocks where appropriate.
6. **Outputs:** Export all useful attributes (ARNs, endpoints, IDs, security group IDs).

### Constraints

- Terraform >= 1.7.0 with AWS provider
- All resources in `us-east-1` unless specified
- Follow least-privilege for IAM roles and policies
- `terraform fmt` before completing

### Success Criteria

- Module files compile with `terraform validate`
- `terraform fmt` produces no diffs
- Variables have descriptions and are used in `main.tf`
- Outputs reference the resources they describe
- README snippet is provided for module usage

### Usage Template

```
Add a [resource_type] to the [module_name] module that:
- Creates [describe resource]
- Accepts variables: [list with types and descriptions]
- Outputs: [list of attributes to export]
- Tags resources with the standard tags (Environment, Project, ManagedBy)
Show the diff and wait for my confirmation before applying.
```

### Chat Example

```
User: Add an aws_db_instance for PostgreSQL 16 to the RDS module. 
- Variable for instance_class (default: db.t3.medium)
- Variable for storage_gb (default: 100)
- Enable storage_encrypted = true
- Output the endpoint and ARN
```

Agent (expected):
- Shows the planned changes: adds resource, variables, and outputs
- Applies `terraform fmt` to the new files
- Waits for user confirmation before applying any patches
