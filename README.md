# CheckpointAssign

## Overview
In this repository you will find three folders, the first one is Terraform inside of it you will find the Iac project.
The second folder is microservice1 you can find in it two folder ci and cd in the ci there are file for the Python code and the Dockerfile in the cd you find the templates for deploying this microservice to EKS.
In the third folder you will find the second microservice the arch similar to the previous one.

## Architecture

### **1. Infrastructure**
- **Cloud Provider:** [AWS]
- **Container Orchestration:** [EKS]
- **Networking:** [VPC, Load Balancer]
- **Storage:** [S3]

### **2. Application Architecture**
- **Backend:** [Python (Flask)]
- **Frontend:** [ELB]
- **Database:** [S3]
- **Messaging Queue:** [SQS]

### **3. Deployment**
- **Infrastructure as Code (IaC):** [Terraform]
- **CI/CD Pipeline:** GitHub Actions for automated builds and deployments

### **4. Comments**
- In the Terraform project I encountered an authentication issue because of it the ELB and the EKS did not created successfully.
- With regards to the CD jobs I could not test it because the EKS in not ready
- With regards to the bouns sections I would do it using Promithus and Grafana, however, because of the EKS issue I did not create it.