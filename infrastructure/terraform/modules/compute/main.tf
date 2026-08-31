resource "aws_instance" "application" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [var.security_group_id]

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  root_block_device {
    encrypted = true
  }

  user_data = <<-EOF
#!/bin/bash
dnf update -y

dnf install -y nginx

systemctl enable nginx
systemctl start nginx

echo "<h1>Enterprise DevSecOps Platform</h1>" > /usr/share/nginx/html/index.html
echo "<p>Application server deployed successfully using Terraform on AWS.</p>" >> /usr/share/nginx/html/index.html
EOF

  tags = {
    Name        = var.instance_name
    Environment = var.environment
    Project     = "Enterprise-DevSecOps-Platform"
  }
}

data "aws_ami" "amazon_linux" {
  most_recent = true

  owners = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}
