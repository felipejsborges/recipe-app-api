
resource "aws_security_group" "lb" {
  description = "Configure access for the Application Load Balancer"
  name        = "${local.prefix}-alb-access"
  vpc_id      = aws_vpc.main.id
}

resource "aws_vpc_security_group_ingress_rule" "lb_http" {
  cidr_ipv4         = "0.0.0.0/0" # must allow it to redirect to 443
  security_group_id = aws_security_group.lb.id
  ip_protocol       = "tcp"
  from_port         = 80
  to_port           = 80
}

resource "aws_vpc_security_group_ingress_rule" "lb_https" {
  cidr_ipv4         = "0.0.0.0/0"
  security_group_id = aws_security_group.lb.id
  ip_protocol       = "tcp"
  from_port         = 443
  to_port           = 443
}

resource "aws_vpc_security_group_egress_rule" "lb_8000" {
  security_group_id = aws_security_group.lb.id
  cidr_ipv4         = "0.0.0.0/0" # must allow it to redirect to 443
  ip_protocol       = "tcp"
  from_port         = 8000
  to_port           = 8000
}

resource "aws_lb" "api" {
  name               = "${local.prefix}-lb"
  load_balancer_type = "application"
  subnets = [
    aws_subnet.public_a.id,
    # aws_subnet.public_b.id
  ]
  security_groups = [aws_security_group.lb.id]
}

resource "aws_lb_target_group" "api" {
  name        = "${local.prefix}-api"
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"
  port        = 8000

  health_check {
    path = "/api/health-check/"
  }
}

resource "aws_lb_listener" "api" {
  load_balancer_arn = aws_lb.api.arn
  port              = 80
  protocol          = "HTTP" # change to HTTPS when domain is configured

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }
}

# resource "aws_lb_listener" "api" {
#   load_balancer_arn = aws_lb.api.arn
#   port              = "80"
#   protocol          = "HTTP"

#   default_action {
#     type = "redirect"

#     redirect {
#       port        = "443"
#       protocol    = "HTTPS"
#       status_code = "HTTP_301"
#     }
#   }
# }