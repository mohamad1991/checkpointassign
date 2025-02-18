module "vpc" {
  source   = "./modules/vpc"
  vpc_cidr = var.vpc_cidr
}


module "sqs" {
  source = "./modules/sqs"
}

module "s3" {
  source = "./modules/s3"
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = var.eks_cluster_name
  cluster_version = "1.29"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.public_subnets

  enable_irsa = true  # Enables IAM Roles for Service Accounts

  eks_managed_node_groups = {
    default = {
      desired_capacity = 2
      min_size         = 1
      max_size         = 3

      instance_types = ["t3.medium"]
    }
  }
}

/*module "ecs" {
  source       = "terraform-aws-modules/ecs/aws"
  cluster_name = var.ecs_cluster_name
}

module "ecs_service" {
  source = "terraform-aws-modules/ecs/aws//modules/service"

  name            = "my-app-service"
  cluster_arn     = module.ecs.cluster_arn
  cpu            = 256
  memory         = 512
  desired_count  = 2
  launch_type    = "FARGATE"

  subnet_ids = module.vpc.public_subnets
  security_group_rules = {
    ingress_http = {
      type        = "ingress"
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  container_definitions = {
    my-container = {
      image   = "nginx:latest"
      cpu     = 256
      memory  = 512
      essential = true
      port_mappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    }
  }
}*/
