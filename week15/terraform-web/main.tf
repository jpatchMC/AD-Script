terraform {
    cloud {
      organization = "Josh-AdvScrpt"
      workspaces {
        name = "JoshDemo"
    }
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = var.region
}
data "aws_availability_zones" "available" {
  #region  = var.region
  state = "available"
}
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "my-vpc"
  cidr = var.VPC

  azs             = data.aws_availability_zones.available.zone_ids
  private_subnets = var.private_subnet_cidr_blocks
  public_subnets  = var.public_subnet_cidr_blocks

  #enable_nat_gateway = true
  #enable_vpn_gateway = true

  tags = {
    Terraform = "true"
    Environment = "JoshDemo"
  }
}
module "vote_service_sg" {
  source = "terraform-aws-modules/security-group/aws"

  name        = "web-sg"
  description = "Security group for user-service with http ports open"
  vpc_id      = module.vpc.vpc_id

  #ingress_cidr_blocks      = ["0.0.0.0/0"]
  #ingress_rules            = ["http-80-tcp"]
  #egress_rules             = ["all-all"]
  ingress_with_cidr_blocks = [
    {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      description = "HTTP"
      cidr_blocks = "0.0.0.0/0"
    }
  ]
  egress_with_cidr_blocks  =[
    {
      from_port   = -1
      to_port     = -1
      protocol    = "-1"
      description = "All protocols"
      cidr_blocks = "0.0.0.0/0"  
    }
  ]
}
data "aws_ami" "AMI" {
  owners = ["amazon"]
  most_recent = true
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

module "ec2_instance" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "~> 3.0"

  name = "josh-web-server"

  ami                    = data.aws_ami.AMI.image_id
  instance_type          = "t2.micro"
  key_name               = "vockey"
  monitoring             = true
  vpc_security_group_ids = [module.vote_service_sg.security_group_id]
  subnet_id              = module.vpc.public_subnets[1] #"subnet-0457dfb972e2a8143" 
  user_data = templatefile("${path.module}/init-scipt.sh", {
    file_content = "JOSH PATCH"
  })

  tags = {
    Terraform   = "true"
    Environment = "JoshDemo"
  }
}
output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = module.ec2_instance.public_ip
}
output "Azs" {
  value = data.aws_availability_zones.available.zone_ids
}
output "publicsub" {
  value = module.vpc.public_subnets
}
