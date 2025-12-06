<<<<<<< Updated upstream
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
=======
📞 TeleLink Communications - Customer Analytics Platform

An AI-powered customer churn prediction and lifetime value estimation system for telecommunications providers.

🎯 Project Overview
TeleLink Communications serves over 1.2 million customers across the United States and faces three critical challenges:
 + Rising customer churn rates (14.2%)
 + Difficulty in accurate revenue forecasting
 + Unpredictable usage patterns affecting operational costs

This platform uses Machine Learning to:

Predict customer churn with up to 95% accuracy
Estimate Customer Lifetime Value (CLV) for strategic planning
Provide actionable recommendations for retention strategies


🏗️ System Architecture
┌─────────────────────────────────────────────────────────────────┐
│                        USER'S BROWSER                           │
│                   (Accesses via Web Browser)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP Request
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       AWS EC2 INSTANCE                          │
│                        (t2.micro)                               │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              DOCKER CONTAINER                             │ │
│  │                                                           │ │
│  │  ┌─────────────────────────────────────────────────┐    │ │
│  │  │           FASTAPI APPLICATION                   │    │ │
│  │  │                                                 │    │ │
│  │  │  ┌──────────────┐      ┌───────────────────┐  │    │ │
│  │  │  │   Frontend   │      │   Backend API     │  │    │ │
│  │  │  │              │      │                   │  │    │ │
│  │  │  │  index.html  │◄────►│   backend.py     │  │    │ │
│  │  │  │  (Static)    │      │   (FastAPI)      │  │    │ │
│  │  │  └──────────────┘      └─────────┬─────────┘  │    │ │
│  │  │                                  │            │    │ │
│  │  │                                  ▼            │    │ │
│  │  │                        ┌──────────────────┐  │    │ │
│  │  │                        │   ML MODELS      │  │    │ │
│  │  │                        │                  │  │    │ │
│  │  │                        │ 1. Churn Model   │  │    │ │
│  │  │                        │    (Random       │  │    │ │
│  │  │                        │     Forest)      │  │    │ │
│  │  │                        │                  │  │    │ │
│  │  │                        │ 2. CLV Model     │  │    │ │
│  │  │                        │    (Linear       │  │    │ │
│  │  │                        │     Regression)  │  │    │ │
│  │  │                        └──────────────────┘  │    │ │
│  │  └─────────────────────────────────────────────┘    │ │
│  │                                                      │ │
│  │  Port 8000 (Internal) ──► Port 80 (External)       │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
Data Flow
User Input (Customer Data)
         │
         ▼
   Web Browser (HTML/JS)
         │
         ▼
   HTTP POST Request
         │
         ▼
   FastAPI Backend
         │
         ├──► Validate Input (Pydantic)
         │
         ├──► Preprocess Data (Sklearn Pipeline)
         │
         ├──► Load ML Models (.pkl files)
         │
         ├──► Make Predictions
         │         ├─► Churn Probability
         │         └─► Customer Lifetime Value
         │
         ├──► Generate Risk Level (Low/Medium/High)
         │
         ├──► Create Recommendation
         │
         ▼
   JSON Response
         │
         ▼
   Display Results in Browser

🚀 Quick Start Guide
Prerequisites
What You Need:

✅ AWS Account (free tier works!)
✅ Basic command line knowledge
✅ SSH key pair for EC2
✅ 15 minutes of your time

What's Included:

+ 2 Pre-trained ML models
+ Professional web interface
+ Automated deployment scripts
+ Real-time predictions


📦 Installation
Option 1: Local Development (Testing)
Step 1: Clone Repository
bashgit clone https://github.com/Andres-lng/ML-DL-FINALPROJECT.git
cd ML-DL-FINALPROJECT
Step 2: Install Dependencies
bashpip install -r requirements.txt
Step 3: Run Application
bashpython backend.py
Step 4: Access Application
Open browser: http://localhost:8000

Option 2: AWS EC2 Deployment (Production Demo)
Step 1: Launch EC2 Instance

Go to AWS Console → EC2 → Launch Instance
Configure:

Name: telelink-demo
AMI: Amazon Linux 2023
Type: t2.micro (Free Tier)
Key Pair: Create or select existing
Security Group: Allow HTTP (80), HTTPS (443), SSH (22)


Click Launch

Step 2: Connect to EC2
ssh -i your-key.pem ec2-user@YOUR_EC2_IP
Step 3: Clone Repository
[git clone ML-DL-FINALPROJECT](https://github.com/Andres-lng/ML-DL-FINALPROJECT.git)
cd ML-DL-FINALPROJECT
Step 4: Initial Setup (One-Time)
bash setup-ec2.sh
Step 5: Deploy Application
bash deploy.sh
Step 6: Access Your Application
http://YOUR_EC2_PUBLIC_IP
That's it! 🎉 Your application is now live!

📁 Project Structure
telelink-analytics/
│
├── 📄 backend.py                    # FastAPI application (Backend + Frontend server)
├── 📄 index.html                    # Web interface (Frontend)
├── 🤖 best_churn_model.pkl         # Trained Random Forest model
├── 🤖 best_clv_model.pkl           # Trained Linear Regression model
├── 📄 requirements.txt              # Python dependencies
│
├── 🐳 Dockerfile                    # Docker container configuration
├── 📄 .dockerignore                 # Files to exclude from Docker
│
├── 🚀 setup-ec2.sh                  # EC2 initial setup script
├── 🚀 deploy.sh                     # Deployment script
│
├── 📊 FinalProject_ANLT202.ipynb   # Model training notebook
│
└── 📖 README.md                     # This file

🔧 Technology Stack
Backend

FastAPI - Modern Python web framework
Scikit-learn - Machine learning library
Pandas - Data manipulation
Joblib - Model serialization
Uvicorn - ASGI server

Frontend

HTML5 - Structure
CSS3 - Styling (Responsive design)
Vanilla JavaScript - Interactivity (No frameworks!)

Machine Learning

Random Forest Classifier - Churn prediction (95% accuracy)
Linear Regression - CLV estimation (R² = 0.89)
SMOTE - Handling imbalanced data
StandardScaler - Feature normalization

Deployment

Docker - Containerization
AWS EC2 - Cloud hosting
Amazon Linux 2023 - Operating system


📊 Machine Learning Models
Model 1: Churn Prediction (Classification)
Algorithm: Tuned Random Forest Classifier
Performance Metrics:

✅ Accuracy: 95.2%
✅ Precision: 93.8%
✅ Recall: 89.4%
✅ F1-Score: 91.5%

Features Used:

Account length
Call volumes (day/evening/night/international)
Customer service calls
International plan status
Voicemail plan status
Geographic data (state, area code)

Output:

Churn probability (0-100%)
Risk level (Low/Medium/High)
Confidence score


Model 2: Customer Lifetime Value (Regression)
Algorithm: Linear Regression Pipeline
Performance Metrics:

✅ R² Score: 0.89
✅ MAE: $2,450
✅ RMSE: $3,120

Features Used:

Account length
Monthly charges (day/evening/night/international)
Service plan indicators
Usage patterns

Output:

Estimated CLV in dollars
Revenue forecast


🎮 How to Use
1. Access the Application
Open your browser and navigate to:

Local: http://localhost:8000
EC2: http://YOUR_EC2_IP

2. Enter Customer Data
Fill in the form with customer information:

Account Details: Length, state, area code
Service Plans: International plan, voicemail plan
Usage Data: Call volumes, voicemail messages
Support: Customer service calls

3. Click "Analyze Customer"
The system will:

Validate your input
Process the data
Run predictions through both models
Display results in ~1-2 seconds

4. Review Results
You'll see:

    Churn Risk: Probability and risk level
    CLV Estimate: Predicted lifetime value
    Recommendation: Specific action to take
    Confidence: Model certainty level

5. Take Action
Based on the risk level:

🔴 High Risk: Immediate retention action required
🟡 Medium Risk: Proactive engagement needed
🟢 Low Risk: Maintain regular engagement


🎯 Use Cases
For Customer Service Teams

Identify at-risk customers before they churn
Prioritize retention efforts based on CLV
Personalize customer interactions

For Marketing Teams

Target high-value customers for upselling
Design retention campaigns for at-risk segments
Optimize marketing spend based on CLV

For Executive Leadership

Forecast revenue more accurately
Make data-driven strategic decisions
Track customer health metrics in real-time

For Data Analytics Teams

Monitor model performance
Generate insights from prediction patterns
Identify key churn drivers


🔍 API Documentation
Once deployed, access interactive API documentation at:
http://YOUR_IP/docs
Main Endpoints
1. Health Check
httpGET /health
Response:
json{
  "status": "healthy",
  "churn_model": "loaded",
  "clv_model": "loaded",
  "api_version": "2.0.0"
}
2. Predict Customer
httpPOST /predict
Content-Type: application/json
Request:
json{
  "accountLength": 128,
  "state": "CA",
  "areaCode": "415",
  "internationalPlan": "no",
  "voiceMailPlan": "yes",
  "numberOfVmailMessages": 25,
  "totalDayCalls": 110,
  "totalEveCalls": 85,
  "totalNightCalls": 95,
  "totalIntlCalls": 3,
  "customerServiceCalls": 1
}
Response:
json{
  "churn_probability": 0.23,
  "churn_risk": "Medium",
  "estimated_clv": 32450.50,
  "recommendation": " PROACTIVE: Valuable customer showing warning signs...",
  "confidence": "High"
}
3. Get Statistics
httpGET /stats
4. Batch Predictions
httpPOST /batch-predict


📞 Contact
TeleLink Analytics Team

<div align="center">
Made with ❤️ for TeleLink Communications
Empowering data-driven decisions through AI
</div>
>>>>>>> Stashed changes
