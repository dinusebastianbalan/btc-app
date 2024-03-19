This project performs the following actions:
Setup K8s cluster with the latest stable version, with RBAC enabled.
The Cluster should have 2 services deployed – Service A and Service B:
- Service-BTC is a WebServer written in Python that exposes the following:
  - Current value of Bitcoin in USD (updated every 10 seconds taken from an API on the web https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD).
  - Average value over the last 10 minutes.
- Service API is a REST API service, which exposes a single controller that responds 200 status code on GET requests.
- NGINX Ingress controller deployed, and corresponding ingress rules for Service BTC and Service API.
- Service BTC can not be able to communicate with Service API.



AWS components :
● VPC (1 subnets, 1 private/1 public)
● ECR (for storing application docker image in ECR repository)
● IAM policies
● EKS with the following specs:
    ○ Managed Node Group with cluster_version 1.29
    ○ 2 Instance_types of t3.small (On-Demand)
● AWS ALB (gateway)
● S3 (storage)
● Route53 (DNS records for domain)

The terraform backend state is configured in S3 bucket.


Github Workflows :
1. name: Docker Image CI
- trigger on Pull Request being submitted to the main branch with modifications being
made in the app path, i.e. “ 'service-api/** or 'service-btc/**' or manually from Github Actions UI, main branch
This job builds and pushes to ECR the application that is deployed to the EKS cluster
(setting up a tag as variable, i.e. DOCKER_IMAGE_TAG=v0.0.2)
2. name: 'Terraform Plan'
- trigger on Pull request being submitted to the main branch with modifications being
made in the app path, i.e. “- infra/**' or manually from Github Actions UI, main branch
This job performs a terraform plan based on the configuration files from infra path.
3. name: 'Terraform Apply'
- trigger on Merge event/push to main branch or manually from Github Actions UI, main
branch
This job performs a terraform apply based on the configuration files from infra path.
4. name: 'Deploy apps and configs'
- trigger on Merge event/push to main branch or manually from Github Actions UI, main
branch
This job deploys the main application and configures other settings such as label k8s namespaces; network policy; DNS records.


Example:
