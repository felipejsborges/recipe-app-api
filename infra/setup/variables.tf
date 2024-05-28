variable "tf_state_bucket" {
  description = "Name of S3 bucket in AWS for storing TF state"
  default     = "my-app-api-state"
}

variable "tf_state_lock_table" {
  description = "Name of DynamoDB table for TF state locking"
  default     = "my-app-api-tf-lock"
}

variable "project" {
  description = "Project name for tagging resources"
  default     = "my-app"
}

variable "contact" {
  description = "Contact name for tagging resources"
  default     = "felipejsborges@outlook.com"
}
