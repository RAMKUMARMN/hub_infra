# Reusable prompts and templates for `hub_infra`

Short task template:

"You are a Terraform infrastructure specialist for the `hub_infra` repo. Task: {{TASK}}. Relevant files: {{FILES}}. Constraints: keep changes minimal, run `terraform fmt` and `terraform validate` in suggestions. Provide a short commit message and a one-paragraph PR description."

Commit message template:

"infra: {{scope}} - {{summary}}"

PR description template:

"Summary: {{one-line}}

What changed:
- {{bullet list of changes}}

Why:
- {{reason}}

Testing:
- Commands to run locally: `terraform fmt`, `terraform validate`, `terraform plan` (describe expected output)."

Code review checklist:
- Minimal change set
- Terraform formatting applied
- No hard-coded secrets
- Outputs and variables updated if needed
