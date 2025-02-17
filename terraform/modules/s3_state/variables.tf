variable "state_bucket_name" {
  description = "S3 bucket for Terraform state"
  type        = string
  default     = "checkpoint-state-bucket-mohamad"
}

variable "dynamodb_table_name" {
  description = "DynamoDB table for state locking"
  type        = string
  default     = "terraform-locks"
}
