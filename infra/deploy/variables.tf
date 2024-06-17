variable "prefix" {
  description = "Prefix for resources in AWS"
  default     = "mpfx"
}

variable "project" {
  description = "Project name for tagging resources"
  default     = "my-app"
}

variable "contact" {
  description = "Contact name for tagging resources"
  default     = "felipejsborges@outlook.com"
}

variable "db_username" {
  description = "Username for the recipe app api database"
  default     = "myuser"
}

variable "db_password" {
  description = "Password for the Terraform database"
}

variable "ecr_proxy_image" {
  description = "Path to the ECR repo with the proxy image"
  default     = "339712875811.dkr.ecr.us-east-1.amazonaws.com/recipe-app-api-proxy"
}

variable "ecr_app_image" {
  description = "Path to the ECR repo with the API image"
  default     = "339712875811.dkr.ecr.us-east-1.amazonaws.com/recipe-app-api-app"
}

variable "django_secret_key" {
  description = "Secret key for Django"
}

locals {
  prefix = "${var.prefix}-${terraform.workspace}"
}

data "aws_region" "current" {}