variable "region" {
  description = "Region"
  type        = string
  default     = "us-east-1"
}
variable "AZ" {
  description = "Availibilty Zone"
  type        = list(string)
  default     = [
    "us-east-1a",
    "us-east-1b"
  ]
}
variable "VPC" {
  description = "main VPC block"
  type        = string
  default     = "10.0.0.0/16"
}
variable "public_subnet_count" {
  description = "Number of public subnets."
  type        = number
  default     = 2
}

variable "private_subnet_count" {
  description = "Number of private subnets."
  type        = number
  default     = 2
}

variable "public_subnet_cidr_blocks" {
  description = "Available cidr blocks for public subnets."
  type        = list(string)
  default     = [
    "10.0.1.0/24",
    "10.0.2.0/24",
  ]
}

variable "private_subnet_cidr_blocks" {
  description = "Available cidr blocks for private subnets."
  type        = list(string)
  default     = [
    "10.0.101.0/24",
    "10.0.102.0/24",
  ]
}
