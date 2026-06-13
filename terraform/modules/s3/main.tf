variable "app_name" { type = string }
variable "environment" { type = string }

resource "aws_s3_bucket" "files" {
  bucket = "${var.app_name}-files-${var.environment}"

  tags = { Name = "${var.app_name}-files-${var.environment}" }
}

resource "aws_s3_bucket_versioning" "files" {
  bucket = aws_s3_bucket.files.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "files" {
  bucket = aws_s3_bucket.files.id

  rule {
    id     = "archive-old-files"
    status = "Enabled"

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    filter { prefix = "uploads/" }
  }
}

resource "aws_s3_bucket_public_access_block" "files" {
  bucket                  = aws_s3_bucket.files.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "bucket_name" { value = aws_s3_bucket.files.bucket }
output "bucket_arn" { value = aws_s3_bucket.files.arn }
