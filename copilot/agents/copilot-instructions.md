Repository: hub_infra (Terraform + small services)

Overview
- Primary infra: Terraform modules for VPC, RDS, ElastiCache, S3.
- Additional config: `mosquitto/` for MQTT broker configuration and `workflows/ci.yml`.

Guidelines for Copilot responses
- Always reference repository files by path and explain limited, focused changes.
- Do not change unrelated files; propose new files when needed.
- For Terraform edits: run `terraform fmt` and `terraform validate` locally; include commands in your suggestions.
- Provide a one-paragraph PR description and a concise commit message.

Useful commands
```
terraform fmt ./terraform
terraform validate ./terraform
git add -A && git commit -m "<summary>"
```
