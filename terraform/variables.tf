variable "region" {
  description = "AWS region (Learner Lab allows us-east-1 / us-west-2)"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "Needs ~2 vCPU / 4 GB for Docker + k3s"
  type        = string
  default     = "t3.medium"
}

variable "key_path" {
  description = "Where to save the generated SSH private key (Jenkins passes this)"
  type        = string
  default     = "./deploy-key.pem"
}
