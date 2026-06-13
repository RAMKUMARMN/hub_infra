terraform {
  required_version = ">= 1.7.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Uncomment to store state in S3 (recommended for team use)
  # backend "s3" {
  #   bucket = "cixiohub-terraform-state"
  #   key    = "prod/terraform.tfstate"
  #   region = "ap-south-1"
  # }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.app_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

# ──────────────────────────────────────────
# Modules
# ──────────────────────────────────────────

module "vpc" {
  source      = "./modules/vpc"
  app_name    = var.app_name
  environment = var.environment
}

module "s3" {
  source      = "./modules/s3"
  app_name    = var.app_name
  environment = var.environment
}

module "rds" {
  source      = "./modules/rds"
  app_name    = var.app_name
  environment = var.environment
  db_password = var.db_password
  vpc_id      = module.vpc.vpc_id
  subnet_ids  = module.vpc.private_subnet_ids
  sg_id       = module.vpc.rds_sg_id
}

module "elasticache" {
  source      = "./modules/elasticache"
  app_name    = var.app_name
  environment = var.environment
  vpc_id      = module.vpc.vpc_id
  subnet_ids  = module.vpc.private_subnet_ids
  sg_id       = module.vpc.redis_sg_id
}
