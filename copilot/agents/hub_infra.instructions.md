
When asked to make changes follow these steps:

1. Scope: Identify the minimal files to change. List them explicitly.
2. Propose: Provide a short plan (3 bullets) before editing.
3. Implement: Show the patch or exact edits (diff). Keep each file change minimal.
4. Validate: Include commands the developer should run (`terraform fmt`, `terraform validate`).
5. PR: Provide a one-paragraph PR description and a concise commit message.

Do NOT:
- Modify unrelated files.
- Add secrets in code.

If a change affects modules, update `terraform/terraform.tfvars.example` and `variables.tf` where applicable.
  