---
mode: agent
agent: infra-agent
name: infra-agent-prompt
description: 
  A system prompt for the `hub_infra` assistant. It defines the agent's role as a focused infrastructure helper for the repository, outlines allowed tools, behavior rules, response format, safety heuristics, and developer hints to ensure safe and effective assistance with infrastructure provisioning and management tasks.
---

### Requirements:

1.  **Automated Infrastructure Provisioning:**
    *   The workflow should be triggered on pushes to the `main` branch and on manual `workflow_dispatch` events.
    *   It must provision infrastructure using Terraform.
    *   Terraform state should be stored securely in an S3 bucket.
    *   Terraform plan and apply steps should be separated, with a manual approval step for `apply` in production environments.
    *   Support for multiple environments (e.g., `dev`, `staging`, `prod`) with environment-specific configurations.
    *   Secrets (e.g., AWS access keys, Terraform variables) must be securely managed using GitHub Secrets.

2.  **Infrastructure Validation and Testing:**
    *   Include a step to validate Terraform configuration using `terraform validate`.
    *   Optionally, integrate with a linter (e.g., `tflint`) for code quality checks.
    *   Run integration tests against the provisioned infrastructure (e.g., using `inspec` or `terratest`).

3.  **Infrastructure Destruction (Optional but Recommended):**
    *   Provide a mechanism to destroy infrastructure, ideally triggered manually with strong safeguards.

4.  **Notifications and Reporting:**
    *   Send status notifications (success/failure) to a designated Slack channel or email address.
    *   Generate a summary of the Terraform plan in the GitHub Actions run output.

### Constraints:

*   **Cloud Provider:** AWS.
*   **IaC Tool:** Terraform.
*   **CI/CD Platform:** GitHub Actions.
*   **Security:** Adhere to the principle of least privilege for all AWS credentials. Do not hardcode sensitive information.
*   **Idempotency:** Terraform operations must be idempotent.
*   **Modularity:** Terraform configurations should be modular and reusable.

### Success Criteria:

*   A successful `push` to `main` for a non-production environment automatically provisions the infrastructure without manual intervention.
*   A successful `push` to `main` for a production environment generates a Terraform plan and waits for manual approval before applying.
*   All Terraform commands execute without errors.
*   Infrastructure validation and testing steps pass successfully.
*   Notifications are sent correctly upon workflow completion.
*   The workflow is easily maintainable and can be extended to support additional environments or cloud providers in the future.

### Usage Template (copy-paste)

Below are ready-to-use prompt templates you can paste to the `infra-agent` chat to generate workflows, patches, and documentation. Replace bracketed values before sending.

- Minimal workflow request:

```
Create a single `/.github/workflows/infra.yml` that supports `dev`, `staging`, and `prod`.
Inputs:
- default environment: `dev`
- s3_state_bucket secret name: `S3_STATE_BUCKET`
- dynamodb_lock_table secret name: `DDB_LOCK_TABLE`
- aws_region: `us-east-1`
- notification secret name: `SLACK_WEBHOOK_URL`

Produce: the workflow YAML, a README snippet listing required secrets, and a PR-ready summary. Show diffs and wait for my confirmation before applying patches. Do NOT enable automatic `apply` for `prod`.
```

- Full, explicit request with options:

```
Generate a GitHub Actions workflow `/.github/workflows/infra.yml` with these behaviours:
- Triggers: `push` to `main`, `workflow_dispatch`.
- Jobs: `fmt` (`terraform fmt`), `validate` (`terraform validate`), `plan` (environment-specific plan), optional `tflint`, optional `integration-tests` using `terratest`.
- Backend: Use S3 state (`S3_STATE_BUCKET`) and DynamoDB lock table (`DDB_LOCK_TABLE`).
- Environments: `dev`, `staging`, `prod` (prod requires manual approval before `apply`).
- Notifications: post summary and failures to Slack via `SLACK_WEBHOOK_URL`.

Inputs to set: `S3_STATE_BUCKET`, `DDB_LOCK_TABLE`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `SLACK_WEBHOOK_URL` (all stored as GitHub Secrets).

Deliverables: workflow file, README snippet for secrets and usage, PR body template, and a verification checklist. Provide diffs and wait for approval before applying changes. Require `CONFIRM_PROD_CHANGE` for any production-impacting edits.
```

- Confirmation example (when agent asks to apply prod changes):

```
I confirm the proposed changes and authorize edits, including production workflow changes.
Confirmation token: CONFIRM_PROD_CHANGE
I understand this may affect production state.
```

### Chat example (copy-paste)

Use these short chat transcripts to interact with the `infra-agent`. Paste, edit the bracketed values, and send.

- Minimal flow (generate draft, review, then apply non-prod):

```
User: Create a single `/.github/workflows/infra.yml` that supports `dev`, `staging`, and `prod`.
Inputs: default environment `dev`, state bucket secret `S3_STATE_BUCKET`, lock table secret `DDB_LOCK_TABLE`, aws_region `us-east-1`, slack secret `SLACK_WEBHOOK_URL`.
Output: workflow YAML, README snippet for required secrets, PR summary. Show diffs and wait for my confirmation before applying patches.
```

Agent (expected):
- Scans repository for Terraform layout (reports found files/modules).
- Produces draft `infra.yml` and README snippet, and shows a unified diff.
- Asks: "Do you want me to apply these changes to the repo? (yes/no)" — for non-prod changes it may proceed after `yes`.

- Full flow with production approval (generate + gated apply):

```
User: Generate an infra workflow as above. Prepare plan and apply for prod but do NOT auto-apply; require manual confirmation.
```

Agent (expected):
- Scans repo and drafts files, shows diffs and plan command examples.
- Asks for final confirmation for any production-impacting edits and shows the explicit confirmation token to use.

User (to approve production edits):
```
I confirm the proposed changes and authorize edits, including production workflow changes.
Confirmation token: CONFIRM_PROD_CHANGE
I understand this may affect production state.
```

Agent (after confirmation):
- Applies patches via `apply_patch`, commits or opens a PR (or provides the patch if you requested manual application).
- Posts a short post-change checklist and recommended verification commands (e.g., `terraform plan -var-file=...`).

If the agent needs missing inputs (e.g., S3 bucket name), it will ask a single targeted question such as: "Please confirm the `S3_STATE_BUCKET` secret name to use."