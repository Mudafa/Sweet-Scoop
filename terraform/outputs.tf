output "public_ip" {
  description = "Public IP of the deployment server (used by Ansible)"
  value       = aws_instance.app.public_ip
}

output "instance_id" {
  value = aws_instance.app.id
}
