output "vpc_id" {
  value = module.networking.vpc_id
}

output "public_subnet_id" {
  value = module.networking.public_subnet_id
}

output "private_subnet_id" {
  value = module.networking.private_subnet_id
}

output "application_security_group_id" {
  value = module.security.application_security_group_id
}

output "application_instance_id" {
  description = "ID of the application EC2 instance"
  value       = module.compute.instance_id
}

output "application_instance_public_ip" {
  description = "Public IP address of the application EC2 instance"
  value       = module.compute.instance_public_ip
}
