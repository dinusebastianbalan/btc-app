This project performs the following actions:
- Setup K8s cluster with the latest stable version, with RBAC enabled.

The Cluster should have 2 services deployed – Service A and Service B:
- Service-BTC is a WebServer written in Python that exposes the following:
  - Current value of Bitcoin in USD (updated every 10 seconds taken from an API on the web https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD).
  - Average value over the last 10 minutes.
- Service API is a REST API service, which exposes a single controller that responds 200 status code on GET requests.
- NGINX Ingress controller deployed, and corresponding ingress rules for Service BTC and Service API.
- Service BTC cannot be able to communicate with Service API.



AWS components :
- VPC (2 subnets, 1 private/1 public)
- ECR (for storing application docker image in ECR repository)
- IAM policies
- EKS with the following specs:
  - Managed Node Group with cluster_version 1.29
  - 2 Instance_types of t3.small (On-Demand)
- AWS LB (gateway)
- S3 (storage)
- Route53 (DNS records for domain)

General info: 

- The terraform backend state is configured in S3 bucket.
- The network policy is constructed on the frontend namespace, with a default deny from evrything ( helm/service-api/allow-gateway-ns.yaml) and a allow from gateway namespace (helm/service-api/default-deny-frontend.yaml) (thus blocking backend requests)
- Services are exposed to internet trough ingress resources
  - service-api (5555 port) : helm/service-api/ingress.yaml
  - service-btc (33133 port): helm/service-btc/ingress-btc-avg.yaml; helm/service-btc/ingress-btc-avg.yaml

Helm/deployment
- custom helm charts for each microservices have been created.

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
This job deploys the main applications, ingress controller and configures other settings such as label k8s namespaces; network policy; DNS records.


Example:

Current price of BTC
http://dev.sebastianbalan.com/current_price

<img width="541" alt="image" src="https://github.com/dinusebastianbalan/btc-app/assets/148752145/8a066ecf-df0c-4f4c-87d0-84581078e533">

Average value over the last 10 minutes of BTC
http://dev.sebastianbalan.com/average_price

<img width="529" alt="image" src="https://github.com/dinusebastianbalan/btc-app/assets/148752145/e8075790-59d3-43b8-9830-aec0691893ed">

Sample RestAPI on /
http://dev.sebastianbalan.com/

<img width="427" alt="image" src="https://github.com/dinusebastianbalan/btc-app/assets/148752145/d6a1b1de-326b-4349-908f-804e67247764">


Network policy (deny service-BTC to connect with service-API)

Curl request from service-BTC

<img width="761" alt="image" src="https://github.com/dinusebastianbalan/btc-app/assets/148752145/714ae0e9-bdbb-4a74-aa36-80c3addb4b7f">

Curl request from gateway (internal service)

<img width="958" alt="image" src="https://github.com/dinusebastianbalan/btc-app/assets/148752145/6602cfba-b0d9-4ae5-9006-39cf5dc27785">

Curl request from internet

<img width="451" alt="image" src="https://github.com/dinusebastianbalan/btc-app/assets/148752145/3c99b986-6e91-4c2a-a1cf-e6157832890c">

