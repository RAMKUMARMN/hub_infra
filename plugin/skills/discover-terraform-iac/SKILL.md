---
name: discover-terraform-iac
description: Map Infrastructure as Code (IaC) modules, state, and AWS resource definitions.
---

# Discover Terraform IaC

Analyze the Terraform directory to map the cloud resource topology.

## Focus Areas
- AWS Resource Modules (`modules/vpc`, `modules/rds`, `modules/s3`, `modules/elasticache`)
- Variables and Outputs (`variables.tf`, `outputs.tf`)
- Environment configurations (`terraform.tfvars.example`)

## Goals
- Map the cloud infrastructure components and their relationships.
- Verify network boundaries (VPC) and persistence layers (RDS, S3).

## Output
Return:
- Cloud resource topology map
- Module dependency graph

## Workflow
1. Route the hub folder agent to plugin/skills for this specific skill folder.
2. Invoke the native `discoverTerraformModules` tool to trace IaC definitions.
3. Invoke `discoverInfrastructureResources` for a broad cloud capability scan.
4. Return the infrastructure blueprint.
