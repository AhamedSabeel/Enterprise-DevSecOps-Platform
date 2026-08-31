output "instance_id" {
  description = "ID of the application EC2 instance"
  value       = aws_instance.application.id
}

output "instance_public_ip" {
  description = "Public IP address of the application EC2 instance"
  value       = aws_instance.application.public_ip
}
