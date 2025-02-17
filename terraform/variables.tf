variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-1"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "eks_cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "checkpoint-eks-mohamad"
}


variable "ecs_cluster_name" {
  description = "ECS cluster name"
  type        = string
  default     = "checkpoint-ecs-mohamad"
}