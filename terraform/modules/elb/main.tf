resource "aws_lb" "elb" {
  name               = "checkpoint-elb-mohamad"
  internal           = false
  load_balancer_type = "application"
  security_groups    = var.security_group
  subnets           = var.subnet
}

# Create a Target Group for EKS
resource "aws_lb_target_group" "eks" {
  name        = "elb-target-group"
  port        = "8080"
  protocol    = "HTTP"
  vpc_id      = var.vpc
  target_type = "instance"  # Use "ip" if targeting pods directly
}

# ALB Listener to Forward Requests to EKS
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.elb.arn
  port              = 80
  protocol         = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.eks.arn
  }
}