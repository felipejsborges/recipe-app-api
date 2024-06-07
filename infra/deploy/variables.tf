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

locals {
  prefix = "${var.prefix}-${terraform.workspace}"
}

data "aws_region" "current" {}