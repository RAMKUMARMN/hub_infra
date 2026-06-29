---
name: terraform-s3-backend
description: Configure Terraform remote state in S3 with DynamoDB locking, bucket policies, and backend config generation.
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Mon, 29 Jun 2026 00:00:00 GMT
---

# Configuring S3 Backend for Terraform State

## Contents
- [Prerequisites](#prerequisites)
- [Step-by-step Setup](#step-by-step-setup)
- [Backend Configuration](#backend-configuration)
- [DynamoDB Locking](#dynamodb-locking)
- [Bucket Policies](#bucket-policies)
- [Verification](#verification)

## Prerequisites

1. An S3 bucket already exists (or you have permissions to create one).
2. Terraform >= 1.7.0 with the AWS provider configured.
3. IAM credentials with `s3:GetObject`, `s3:PutObject`, `s3:DeleteObject`, `s3:ListBucket`, and `dynamodb:*` on the lock table.

## Step-by-step Setup

### Task Progress
- [ ] **Step 1: Create the state bucket.** Use `aws s3api create-bucket` or a bootstrap Terraform config.
- [ ] **Step 2: Enable versioning.** `aws s3api put-bucket-versioning --bucket my-state-bucket --versioning-configuration Status=Enabled`
- [ ] **Step 3: Enable encryption.** `aws s3api put-bucket-encryption --bucket my-state-bucket --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'`
- [ ] **Step 4: Create DynamoDB lock table:** `aws dynamodb create-table --table-name terraform-locks --attribute-definitions AttributeName=LockID,AttributeType=S --key-schema AttributeName=LockID,KeyType=HASH --billing-mode PAY_PER_REQUEST`
- [ ] **Step 5: Add backend block** to `terraform/backend.tf` as shown below.
- [ ] **Step 6: Run `terraform init`** to migrate state to the remote backend.

## Backend Configuration

Create `terraform/backend.tf`:

```hcl
terraform {
  backend "s3" {
    bucket         = "my-state-bucket"
    key            = "infra/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

## DynamoDB Locking

DynamoDB prevents concurrent `terraform apply` runs by acquiring a lock:

| Setting | Value |
|---|---|
| Table name | `terraform-locks` |
| Partition key | `LockID` (type String) |
| Billing mode | `PAY_PER_REQUEST` |
| Encryption | AWS managed key (default) |

## Bucket Policies

Follow least-privilege. Example policy for the state bucket:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::ACCOUNT_ID:role/terraform-runner"
      },
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-state-bucket",
        "arn:aws:s3:::my-state-bucket/*"
      ]
    }
  ]
}
```

## Verification

1. Run `terraform init` — should print "Successfully configured the backend 's3'!"
2. Run `terraform plan` — should produce expected output without errors.
3. Check DynamoDB `terraform-locks` table for a lock item during an active `apply`.
