resource "aws_efs_file_system" "media" {
  encrypted = true
}

resource "aws_security_group" "efs" {
  description = "Access rules for the EFS service."
  name        = "${local.prefix}-efs"
  vpc_id      = aws_vpc.main.id
}

resource "aws_vpc_security_group_ingress_rule" "from_ecs_to_efs" {
  security_group_id            = aws_security_group.efs.id
  referenced_security_group_id = aws_security_group.ecs_service.id
  ip_protocol                  = "tcp"
  from_port                    = 2049
  to_port                      = 2049
}

resource "aws_efs_mount_target" "media_a" {
  file_system_id  = aws_efs_file_system.media.id
  subnet_id       = aws_subnet.private_a.id
  security_groups = [aws_security_group.efs.id]
}

resource "aws_efs_mount_target" "media_b" {
  file_system_id  = aws_efs_file_system.media.id
  subnet_id       = aws_subnet.private_b.id
  security_groups = [aws_security_group.efs.id]
}

resource "aws_efs_access_point" "media" {
  file_system_id = aws_efs_file_system.media.id

  root_directory {
    path = "/api/media"

    creation_info {
      owner_gid   = 101
      owner_uid   = 101
      permissions = "755"
    }
  }
}
