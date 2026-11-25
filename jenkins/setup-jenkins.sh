#!/bin/bash
# One-time setup for the Jenkins EC2 instance (Ubuntu 24.04).
# Installs: Java 21, Jenkins LTS, Docker + Compose, Terraform, Ansible.
#
# Usage (on the Jenkins EC2 instance):
#   curl -fsSL https://raw.githubusercontent.com/Mudafa/Sweet-Scoop/main/jenkins/setup-jenkins.sh | bash
#   (or copy this file over and run: bash setup-jenkins.sh)
set -euo pipefail

echo "===== Base packages, Java 21, Docker, Ansible ====="
sudo apt-get update
sudo apt-get install -y fontconfig openjdk-21-jre git curl wget unzip gnupg \
  python3 docker.io docker-compose-v2 ansible
sudo systemctl enable --now docker

echo "===== Jenkins LTS ====="
# Jenkins rotated its repo signing key in Dec 2025 -> jenkins.io-2026.key
sudo mkdir -p /etc/apt/keyrings
sudo wget -qO /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" \
  | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

echo "===== Terraform ====="
wget -qO- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor --yes -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/hashicorp.list > /dev/null

sudo apt-get update
sudo apt-get install -y jenkins terraform

echo "===== Let Jenkins use Docker ====="
sudo usermod -aG docker jenkins
sudo usermod -aG docker ubuntu || true
sudo systemctl restart jenkins

# Folder for Terraform state + the generated SSH key (kept outside the job workspace)
sudo mkdir -p /var/lib/jenkins/sweet-scoop
sudo chown jenkins:jenkins /var/lib/jenkins/sweet-scoop

echo
echo "===== Versions ====="
java -version 2>&1 | head -1
docker --version
docker compose version
terraform version | head -1
ansible --version | head -1
echo
echo "Jenkins is starting on http://$(curl -s https://checkip.amazonaws.com):8080"
echo "Initial admin password:"
sleep 15
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
