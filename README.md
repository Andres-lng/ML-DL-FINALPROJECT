# 🎯 Project Overview
TeleLink Communications serves over 1.2 million customers across the United States and faces three critical challenges:
 + Rising customer churn rates (14.2%)
 + Difficulty in accurate revenue forecasting
 + Unpredictable usage patterns affecting operational costs

This platform uses Machine Learning to:

Predict customer churn with up to 95% accuracy
Estimate Customer Lifetime Value (CLV) for strategic planning
Provide actionable recommendations for retention strategies


# ✅ Architecture System Architecture
## High-Level Architecture Diagram
![High-Level Architecture Diagram](https://github.com/user-attachments/assets/08d74f51-3c93-4f0b-a5ff-3a7662723751)
## Data Flow
![Telelink (1)](https://github.com/user-attachments/assets/c7e00af4-4b4e-4d7e-a232-3135a60fae93)


# 🚀 Quick Start Guide
## 1. Prerequisites
** What You Need: **
 - AWS Account (free tier works!)
 - Basic command line knowledge
 - SSH key pair for EC2
   
** What's Included: **
 - 2 Pre-trained ML models
 - Professional web interface
 - Automated deployment scripts
 - Real-time predictions


## 2. Installation
** Option 1: Local Development (Testing) **
### 1. Step 1: Clone Repository
- git clone https://github.com/Andres-lng/ML-DL-FINALPROJECT.git
- cd ML-DL-FINALPROJECT
### Step 2: Install Dependencies
- pip install -r requirements.txt
### Step 3: Run Application
- python backend.py
### Step 4: Access Application
Open browser: http://localhost:8000

** Option 2: AWS EC2 Deployment (Production Demo) **
### Step 1: Launch EC2 Instance
- Go to AWS Console → EC2 → Launch Instance
- Configure: 1. Name: telelink-demo | 2. AMI: Amazon Linux 2023 | 3. Type: t2.micro (Free Tier) | 4. Key Pair: Create or select existing | 5.Security Group: Allow HTTP (80), HTTPS (443), SSH (22)
- Click Launch
### Step 2: Connect to EC2
- ssh -i your-key.pem ec2-user@YOUR_EC2_IP
### Step 3: Clone Repository
- [git clone ML-DL-FINALPROJECT](https://github.com/Andres-lng/ML-DL-FINALPROJECT.git)
- cd ML-DL-FINALPROJECT
### Step 4: Initial Setup (One-Time)
- bash setup-ec2.sh
### Step 5: Deploy Application
- bash deploy.sh
Step 6: Access Your Application
- http://YOUR_EC2_PUBLIC_IP
- Your application is now live!

# Technology Stack
1. Backend
    FastAPI - Modern Python web framework
    Scikit-learn - Machine learning library
    Pandas - Data manipulation
    Joblib - Model serialization
    Uvicorn - ASGI server

2. Frontend
    HTML5 - Structure
    CSS3 - Styling (Responsive design)
    
3. Machine Learning
    Random Forest Classifier - Churn prediction (95% accuracy)
    Linear Regression - CLV estimation (R² = 0.89)
    SMOTE - Handling imbalanced data
    StandardScaler - Feature normalization

4. Deployment
    Docker - Containerization
    AWS EC2 - Cloud hosting
    Amazon Linux 2023 - Operating system


# 📊 Machine Learning Models
1. Model 1: Churn Prediction (Classification)
    Algorithm: Tuned Random Forest Classifier
    - Performance Metrics: Accuracy: 0.867, Precision: 0.552, Recall: 0.337, F1 Score: 0.418
    - Features Used:
    Account length
    Call volumes (day/evening/night/international)
    Customer service calls
    International plan status
    Voicemail plan status
    Geographic data (state, area code)

    - Output: Churn probability (0-100%) | Risk level (Low/Medium/High) | Confidence score
2. Model 2: Customer Lifetime Value (Regression)
    Algorithm: Linear Regression Pipeline
    - Performance Metrics: MAE: 898.36, RMSE: 1108.81, R²: 0.9328
    - Features Used:
        Account length
        Monthly charges (day/evening/night/international)
        Service plan indicators
        Usage patterns
    - Output:
        Estimated CLV in dollars
        Revenue forecast

# 🎮 How to Use
1. Access the Application
Open your browser and navigate to: + Local: http://localhost:8000 | + EC2: http://www.infosecurity.homes/
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

