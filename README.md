# TeleLink Communications — AI-Powered Customer Churn & CLV Prediction Platform

---

# 🎯 1. Project Overview

TeleLink Communications serves over **1.2 million customers** across the United States and faces three major challenges:

- Rising customer churn (**14.2%**)  
- Difficulty forecasting long-term revenue  
- Unpredictable usage patterns affecting operational costs  

This project delivers an **end-to-end AI platform** that:

- Predicts customer churn with high sensitivity (recall-focused)  
- Estimates Customer Lifetime Value (CLV)  
- Supports strategic, data-driven retention decision-making  
- Offers a **cloud-deployed** web application for real-time analysis  

The solution integrates **classical machine learning**, **deep learning**, and **cloud technologies**.

---

# 📘 2. Dataset & Preprocessing 

### Key Characteristics  
- ~3,300 total records (train + test)
- 20+ features including:
  - State, Area code, International plan  
  - Call minutes & charges  
  - Customer service calls  
- Churn rate: **~14.5%** (imbalanced)

### Preprocessing Steps  
✔ One-Hot Encoding for categorical features  
✔ StandardScaler for numeric features  
✔ SMOTE for class imbalance  
✔ Remove leakage features in CLV modeling  
✔ Unified preprocessing **Pipelines** for all models  

---

# 🔢 3. Classification Task — Customer Churn Prediction

### Goal  
Predict whether a customer will **churn (1)** or **stay (0)**.

### Why Recall Matters  
Missing a true churner costs the company more than a false alarm.  
Therefore **recall is the primary metric**.

### Models  
- Logistic Regression  
- Random Forest  
- **Tuned Random Forest**  
- **Deep Learning Classification Model**  

### Summary  
- Best classical model: **Tuned Random Forest**  
- Best overall recall: **Deep Learning Model**  
- Business recommendation → **Deep Learning (maximize detection)**  

---

# 💵 4. Regression Task — Customer Lifetime Value (CLV)

### Goal  
Predict **Customer Lifetime Value** → projected revenue per customer.

### Why CLV Matters  
Helps TeleLink optimize:
- Marketing spending  
- Retention budgeting  
- Pricing strategies  
- Revenue forecasting  

### Models  
- **Linear Regression (Best performance)**  
- Gradient Boosting  
- Tuned Gradient Boosting  
- Deep Learning Regression Model  

---

# 📊 5. Model Comparison Summary

## Classification
| Model | Accuracy | Precision | Recall | F1 Score | Notes |
|-------|----------|-----------|--------|----------|-------|
| Logistic Regression | 0.714 | 0.274 | 0.611 | 0.378 | High recall |
| Random Forest | 0.859 | 0.511 | 0.242 | 0.329 | Low recall |
| **Tuned Random Forest** | **0.867** | **0.552** | **0.337** | **0.418** | Best classical |
| **Deep Learning** | 0.688 | 0.258 | **0.632** | 0.366 | **Best recall** |

## Regression
| Model | MAE | RMSE | R² |
|--------|-------|--------|------|
| **Linear Regression (Best)** | **852.48** | **1085.32** | **0.9343** |
| Gradient Boosting | 864.33 | 1095.70 | 0.9330 |
| Tuned Gradient Boosting | 863.97 | 1092.35 | 0.9334 |
| Deep Learning | 881.64 | 1121.07 | 0.9299 |

---

# 🧪 6. How to Run Experiments Locally

### Step 1 — Clone Repository
```bash
git clone https://github.com/Andres-lng/ML-DL-FINALPROJECT.git
cd ML-DL-FINALPROJECT
```

### Step 2 — Virtual Environment
```bash
python -3.11 -m venv .venv
source .venv/bin/activate        # macOS/Linux
.\.venv\Scriptsctivate         # Windows
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Launch Notebook
```bash
jupyter notebook
```

### Step 5 — Open Notebook
```
FinalProject_ANLT202.ipynb
```

---

# 🔁 7. How to Reproduce Results

### Classification  
- Run full preprocessing pipeline 
- Apply SMOTE to balance the churn classes 
- Train Tuned RF (RandomizedSearchCV, scoring = F1) / Deep Learning (class weights + threshold = 0.3)
Expected recall:
```
≈ 0.63 (Deep Learning)
```
- Note: Results are reproducible when using fixed random seeds (e.g., random_state=42 and TensorFlow seeds).

### Regression  
- Run preprocessing (same as classification, but without SMOTE)
- Train Linear Regression  
Expected R²:
```
≈ 0.934
```

---

# 🏗️ 8. Cloud Deployment System Architecture

### High-Level Architecture  
![High-Level Architecture Diagram](https://github.com/user-attachments/assets/08d74f51-3c93-4f0b-a5ff-3a7662723751)

### Data Flow  
![Telelink (1)](https://github.com/user-attachments/assets/c7e00af4-4b4e-4d7e-a232-3135a60fae93)

---

# ☁️ 9. Deployment Guide (Local + Cloud)

## **Option 1: Local**
```bash
python backend.py
```
Visit:
```
http://localhost:8000
```

---

## **Option 2: AWS EC2 Deployment (Production Demo)**

### Step 1 — Launch EC2 Instance
- Navigate: **AWS Console → EC2 → Launch Instance**
- Configure:
  - Name: `telelink-demo`
  - AMI: **Amazon Linux 2023**
  - Instance Type: **t2.micro (Free Tier)**
  - Key Pair: Create or choose existing  
  - Security Group: Allow **80 (HTTP)**, **443 (HTTPS)**, **22 (SSH)**  
- Click **Launch**

### Step 2 — Connect to EC2
```bash
ssh -i your-key.pem ec2-user@YOUR_EC2_IP
```

### Step 3 — Clone Repository
```bash
git clone https://github.com/Andres-lng/ML-DL-FINALPROJECT.git
cd ML-DL-FINALPROJECT
```

### Step 4 — Initial One-Time Setup
```bash
bash setup-ec2.sh
```

### Step 5 — Deploy Application
```bash
bash deploy.sh
```

### Step 6 — Access Application
```
http://YOUR_EC2_PUBLIC_IP
```
Your application is now live!

---

# 🧰 Technology Stack

## Backend  
- FastAPI  
- Scikit-learn  
- Pandas  
- Joblib  
- Uvicorn  

## Frontend  
- HTML5 (Structure)  
- CSS3 (Responsive UI)  

## Machine Learning  
- Random Forest (Churn)  
- Linear Regression (CLV)  
- SMOTE for imbalance  
- StandardScaler  

## Deployment  
- Docker  
- AWS EC2  
- Amazon Linux 2023  

---

# 🖥️ 10. How to Use the Web App

1. Open the app : http://www.infosecurity.homes/ 
3. Enter customer details  
4. Click **Analyze Customer**  
5. View:
   - Churn probability  
   - Risk level  
   - CLV prediction  
   - Recommended action  

---

# ⚠️ 11. Current Limitations

- CLV is artificially simulated, not real company data  
- Precision is low in churn model despite strong recall  
- Deep learning models lightly tuned only  
- Some telecom-specific features may not generalize  

---

# 🚀 12. Future Improvements

- Replace simulated CLV with real customer revenue history  
- Tune deep learning layers, dropout, learning rate  
- Use business cost optimization to adjust classification threshold  
- Improve precision while maintaining recall  
- Consider LSTM/Transformers for sequential usage data  

---

# 📎 References

Kaggle Dataset: https://www.kaggle.com/datasets/mnassrib/telecom-churn-datasets/data  

