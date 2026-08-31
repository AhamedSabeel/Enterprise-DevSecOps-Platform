terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region  = "ap-south-1"
  profile = "enterprise-devsecops"
}

module "networking" {
  source = "../../modules/networking"

  environment         = "dev"
  network_name        = "enterprise-dev"
  vpc_cidr            = "10.0.0.0/16"
  public_subnet_cidr  = "10.0.1.0/24"
  private_subnet_cidr = "10.0.2.0/24"
  availability_zone   = "ap-south-1a"
}


module "security" {
  source = "../../modules/security"

  environment = "dev"
  vpc_id      = module.networking.vpc_id
}


module "compute" {
  source = "../../modules/compute"

  environment       = "dev"
  instance_name     = "enterprise-dev-application"
  instance_type     = "t3.micro"
  subnet_id         = module.networking.public_subnet_id
  security_group_id = module.security.application_security_group_id
}
