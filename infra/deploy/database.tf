############
# Database #
############

resource "aws_db_subnet_group" "main" {
  name = "${local.prefix}-main"
  subnet_ids = [
    aws_subnet.private_a.id,
    aws_subnet.private_b.id
  ]
}

resource "aws_security_group" "rds" {
  description = "Allow access to the RDS database instance."
  name        = "${local.prefix}-rds"
  vpc_id      = aws_vpc.main.id
}

resource "aws_vpc_security_group_ingress_rule" "allow_tls_ipv4" {
  security_group_id = aws_security_group.rds.id
  cidr_ipv4         = aws_vpc.main.cidr_block
  ip_protocol       = "tcp"
  from_port         = 5432
  to_port           = 5432
}

resource "aws_db_instance" "main" {
  identifier        = local.prefix
  db_name           = "my_db"
  allocated_storage = 20
  storage_type      = "gp2"
  engine            = "postgres"
  # engine_version             = "15.3"
  auto_minor_version_upgrade = false
  instance_class             = "db.t3.micro"
  username                   = var.db_username
  password                   = var.db_password
  skip_final_snapshot        = true # for real projects should be false
  db_subnet_group_name       = aws_db_subnet_group.main.name
  multi_az                   = false
  vpc_security_group_ids     = [aws_security_group.rds.id]
}
