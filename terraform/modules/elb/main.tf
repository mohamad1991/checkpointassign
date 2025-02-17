resource "aws_lb" "elb" {
  name               = "checkpoint-elb-mohamad"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.elb_sg.id]
  subnets           = var.subnet_ids
}
