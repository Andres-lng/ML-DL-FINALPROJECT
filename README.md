# Cloud Deployment Log — FastAPI ML Model on AWS ECS Fargate

This document records **every step** taken to deploy a FastAPI machine-learning application to the cloud using **Docker + AWS ECR + ECS Fargate + Load Balancer**.  
All sensitive information (AWS Access Keys, Secrets, etc.) has been removed.

---
# ✅ Architecture
<img width="1024" height="1024" alt="Architecture" src="https://github.com/user-attachments/assets/6a7f80e2-0338-4814-b3a7-8c2e8ae204b0" />





# ✅ 1. Create Python Virtual Environment

```
python -m venv .venv
```

Activate it:

```
.\.venv\Scripts\activate
```

---

# ✅ 2. Create `requirements.txt`

Include the necessary packages:

```
fastapi
uvicorn[standard]
joblib
numpy
scikit-learn
jinja2
python-multipart
```

---

# ✅ 3. Create Dockerfile

Your Dockerfile should:

- Pull a lightweight Python image (e.g., python:3.11-slim)
- Set `/app` as the working directory
- Install all dependencies from `requirements.txt`
- Copy the FastAPI code, ML model, and templates
- Run Uvicorn on port 8000

---

# ✅ 4. Create `.dockerignore`

This reduces container size by excluding unnecessary folders:

```
.venv/
__pycache__/
*.pyc
.git
.gitignore
.env
```

---

# ✅ 5. Build the Docker Image

Build locally:

```
docker build -t iris-ml-api .
```

This will:

- Pull python:3.11-slim (first time only)
- Install requirements
- Copy your application

---

# ✅ 6. Run Container Locally

Test your image:

```
docker run -p 8000:8000 iris-ml-api
```

Visit:

```
http://localhost:8000/
```

---

# ✅ 7. Push Your Image to AWS ECR

## 7.1 Install AWS CLI

Download AWS CLI installer:  
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

Configure CLI:

```
aws configure
```

Enter:
- Access Key ID  
- Secret Key  
- Default region (ex: ca-central-1)

---

## 7.2 Create IAM User (in Console)

Create user with **programmatic access**.

Attach permissions:

- `AmazonEC2ContainerRegistryFullAccess`
- `AmazonECS_FullAccess`
- `CloudWatchLogsFullAccess`

Save access keys (DO NOT include in README).

---

## 7.3 Create ECR Repository

1. AWS Console → ECR → Create repository  
2. Repository name: `iris-ml-api`  
3. Copy the `repository URI`

Example:

```
414691912275.dkr.ecr.ca-central-1.amazonaws.com/iris-ml-api
```

---

## 7.4 Authenticate Docker to ECR

```
aws ecr get-login-password --region ca-central-1 | docker login --username AWS --password-stdin 414691912275.dkr.ecr.ca-central-1.amazonaws.com
```

---

## 7.5 Tag and Push Your Image

Tag image:

```
docker tag iris-ml-api:latest 414691912275.dkr.ecr.ca-central-1.amazonaws.com/iris-ml-api:latest
```

Push image:

```
docker push 414691912275.dkr.ecr.ca-central-1.amazonaws.com/iris-ml-api:latest
```

Confirm in AWS Console → Image with tag `latest` appears.

---

# ✅ Step 8 — Create ECS Cluster (Fargate)

### IAM Requirement:
Attach:

```
AmazonEC2ContainerServiceRole
```

### Create the Cluster:

1. ECS → Clusters → Create cluster  
2. Select **Fargate only**  
3. Cluster name: `iris-ml-cluster`  
4. Finish creation

---

# ✅ Step 9 — Create ECS Task Definition

### Task Definition Details:

- Launch type: **AWS Fargate**
- OS: Linux
- CPU: **0.25 vCPU**
- Memory: **0.5 GB**
- Container settings:
  - Image URI: your ECR image
  - Port mapping: **8000**

This defines:

- CPU & memory for your container  
- Which Docker image to run  
- Networking & runtime configuration  

---

# ✅ Step 10 — Create ECS Service (cluster → service → running container)

From your cluster:

1. ECS → Cluster → *Your cluster*
2. Go to "Services" → "Create"
3. Service name: `iris-ml-service`
4. Launch type: **Fargate**
5. Task definition: select the one created
6. Desired tasks: **1**

---

# ✅ Step 11 — Configure Networking & Load Balancer

### VPC
- Use **default VPC**

### Subnets
- Select **two public subnets**

### Security Group
Create a new SG:

Inbound rules:

| Type | Port | Source |
|------|-------|--------|
| HTTP | 80 | 0.0.0.0/0 |

### Load Balancer
- Create new **Application Load Balancer**
- Internet-facing
- Listener: **HTTP : 80**

### Target Group
- Create new TG
- Port: **8000**
- Health check path: `/`

### Auto-assign Public IP
✔ Enabled

Create service.

---

# ✅ Step 12 — Get Public URL

1. Go to **EC2 → Load Balancers**
2. Select: `iris-ml-lb`
3. Copy DNS name

Example:

```
http://iris-ml-lb-123456.ca-central-1.elb.amazonaws.com/
```

Open in browser → FastAPI UI should load.

---

# ❗ If Load Balancer Shows 504 Timeout

Check **Target Group → Targets → Health details**

If showing **"Request timed out"**, fix by editing the **task security group**:

Add inbound rule:

```
Type: Custom TCP
Port range: 8000
Source: 0.0.0.0/0
```

After saving, target will become **Healthy**.

---
