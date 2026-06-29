---
mode: agent
agent: infra-planner
name: infra-planner-prompt
description: "Prompt for the infra-planner agent. Generates structured implementation plans for new Terraform modules, Mosquitto config, CI workflows, or refactoring."
---

### Requirements

1. **Explore the codebase** to understand current module structure, existing modules, and code patterns.
2. **Produce a numbered step-by-step plan** covering each file change required.
3. **Identify dependencies** between steps (e.g., create variables before using them in main.tf).
4. **Risk assessment** — flag destructive, state-modifying, or security-sensitive changes.
5. **Validation plan** — list `terraform fmt`, `validate`, `plan` commands for each stage.

### Constraints

- Do not implement code — output the plan only
- Reference specific file paths relative to repo root
- For Terraform work, follow the existing module conventions (tags, variable style, output patterns)

### Output Format

```
## Implementation Plan: [Title]

### Step 1: [File path]
Action: create | modify | delete
Details: [what to add/change]

### Step 2: ...
...

### Risk Assessment
- [Critical/Medium/Low] risks identified
- [Specific items]

### Validation Checklist
- [ ] `terraform fmt` on modified files
- [ ] `terraform validate` on each module
```

### Usage Template

```
Plan the implementation of [describe task]. 
Consider [constraints or special requirements].
```

### Chat Example

```
User: Plan the implementation of an ElastiCache Redis module with encryption in transit, multi-AZ, and CloudWatch alarms for cache hit rate.
```

Agent (expected):
- Explores `terraform/modules/` for conventions from existing modules
- Produces a step-by-step plan listing files to create, resource types, variables, and validation steps
- Does not write any code
