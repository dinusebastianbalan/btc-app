module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  # Details
  name            = "${var.name}-${local.name}"
  cidr            = var.cidr
  azs             = var.azs
  public_subnets  = var.public_subnets
  private_subnets = var.private_subnets

  # NAT Gateways - Outbound Communication
  enable_nat_gateway = var.enable_nat_gateway
  single_nat_gateway = var.single_nat_gateway

  # DNS Parameters in VPC
  enable_dns_hostnames = true
  enable_dns_support   = true

  # Additional tags for the VPC
  tags     = local.tags
  vpc_tags = local.tags

  # Additional tags
  # Additional tags for the public subnets
  public_subnet_tags = {
    Name = "VPC Public Subnets"
  }
  # Additional tags for the private subnets
  private_subnet_tags = {
    Name = "VPC Private Subnets"
  }

  # Instances launched into the Public subnet should be assigned a public IP address. Specify true to indicate that instances launched into the subnet should be assigned a public IP address
  map_public_ip_on_launch = true
}

resource "aws_ecr_repository" "my_ecr-api" {
  name = "my-ecr-api"
}


resource "aws_ecr_repository" "my_ecr-btc" {
  name = "my-ecr-btc"
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = var.cluster_name
  cluster_version = "1.29"

  subnet_ids                     = module.vpc.private_subnets
  vpc_id                         = module.vpc.vpc_id
  cluster_endpoint_public_access = true

  node_security_group_tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = null
  }
  # Cluster access entry
  # To add the current caller identity as an administrator
  enable_cluster_creator_admin_permissions = true

}

# module "eks_managed_node_group" {
#   source = "terraform-aws-modules/eks/aws//modules/eks-managed-node-group"

#   name            = "separate-eks-mng"
#   cluster_name    = module.eks.cluster_name
#   cluster_version = "1.29"

#   subnet_ids = module.vpc.private_subnets

#   cluster_primary_security_group_id = module.eks.cluster_primary_security_group_id
#   vpc_security_group_ids            = [module.eks.node_security_group_id]

#   min_size     = 2
#   max_size     = 10
#   desired_size = 2

#   instance_types = ["t3.medium"]
#   capacity_type  = "ON_DEMAND"

#   labels = {
#     Environment = "test"
#     GithubRepo  = "terraform-aws-eks"
#     GithubOrg   = "terraform-aws-modules"
#   }

#   tags = {
#     Environment = "dev"
#     Terraform   = "true"
#   }
# }