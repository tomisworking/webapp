variable "aws_region" {
  description = "AWS region to deploy to"
  type        = string
  default     = "eu-central-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "ssh_ingress_cidr" {
  description = "CIDR allowed to SSH into EC2 instances (use your IP/32 in production)"
  type        = string
  default     = "0.0.0.0/0"
}

variable "db_username" {
  description = "Master username for RDS PostgreSQL"
  type        = string
  default     = "forumadmin"
}

variable "db_password" {
  description = "Master password for RDS PostgreSQL"
  type        = string
  sensitive   = true
}

variable "rds_instance_class" {
  description = "Instance class for RDS PostgreSQL (use db.t3.micro for free tier)"
  type        = string
  default     = "db.t3.micro"
}

variable "rds_engine_version" {
  description = "PostgreSQL engine version for RDS"
  type        = string
  default     = "15.4"
}

variable "frontend_bucket_name" {
  description = "Globally-unique S3 bucket name for React builds (e.g. forum-frontend-builds-tomek-2024)"
  type        = string
}
