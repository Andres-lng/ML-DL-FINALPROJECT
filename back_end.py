"""
TeleLink Communications - FastAPI Backend
Customer Analytics & Service Optimization Platform
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import pandas as pd
from typing import Optional
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Initialize FastAPI app
app = FastAPI(
    title="TeleLink Customer Analytics API",
    description="ML-powered customer churn prediction and CLV estimation",
    version="2.0.0"
)
# After creating the FastAPI app, add:
app.mount("/static", StaticFiles(directory="static"), name="static")

# this route to serve the frontend:
@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")
 

# Configure CORS to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained models at startup
try:
    churn_model = joblib.load("best_churn_model_trf.pkl")
    clv_model = joblib.load("best_clv_model_lnr.pkl")
    print("✓ Models loaded successfully!")
except Exception as e:
    print(f"✗ Error loading models: {e}")
    churn_model = None
    clv_model = None


# Request model for customer data
class CustomerData(BaseModel):
    accountLength: int = Field(..., description="Account length in days", ge=0)
    state: str = Field(..., description="Customer state code", min_length=2, max_length=2)
    areaCode: str = Field(..., description="Area code", min_length=3, max_length=3)
    internationalPlan: str = Field(..., description="International plan (yes/no)")
    voiceMailPlan: str = Field(..., description="Voice mail plan (yes/no)")
    numberOfVmailMessages: int = Field(..., description="Number of voicemail messages", ge=0)
    totalDayCalls: int = Field(..., description="Total day calls", ge=0)
    totalEveCalls: int = Field(..., description="Total evening calls", ge=0)
    totalNightCalls: int = Field(..., description="Total night calls", ge=0)
    totalIntlCalls: int = Field(..., description="Total international calls", ge=0)
    customerServiceCalls: int = Field(..., description="Customer service calls", ge=0)

    class Config:
        json_schema_extra = {
            "example": {
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
        }


# Response model for predictions
class PredictionResponse(BaseModel):
    churn_probability: float = Field(..., description="Probability of customer churn (0-1)")
    churn_risk: str = Field(..., description="Risk level: Low, Medium, or High")
    estimated_clv: float = Field(..., description="Estimated Customer Lifetime Value in USD")
    recommendation: str = Field(..., description="Recommended action for customer retention")
    confidence: str = Field(..., description="Model confidence level")


def prepare_input_data(customer: CustomerData) -> pd.DataFrame:
    """
    Convert customer data to DataFrame format expected by models.
    Must match the exact feature names and order from training.
    """
    # Create DataFrame with exact column names from training
    data = pd.DataFrame({
        'Account length': [customer.accountLength],
        'International plan': [customer.internationalPlan],
        'Voice mail plan': [customer.voiceMailPlan],
        'Number vmail messages': [customer.numberOfVmailMessages],
        'Total day calls': [customer.totalDayCalls],
        'Total eve calls': [customer.totalEveCalls],
        'Total night calls': [customer.totalNightCalls],
        'Total intl calls': [customer.totalIntlCalls],
        'Customer service calls': [customer.customerServiceCalls],
        'State': [customer.state],
        'Area code': [customer.areaCode]
    })
    
    return data


def get_recommendation(churn_prob: float, clv: float) -> str:
    """Generate actionable recommendation based on churn risk and CLV."""
    """WE SHOULD USE "0.3" AS OUR THRESHOLD TO ALIGN WITH OUR CLASSIFICATION MODEL"""
    if churn_prob >= 0.3:
        if clv > 30000:
            return "🚨 CRITICAL: High-value customer at severe risk. Immediate executive intervention required. Offer premium retention package."
        else:
            return "⚠️ HIGH PRIORITY: Customer likely to churn. Assign dedicated account manager and offer targeted incentives within 24 hours."
    elif churn_prob >= 0.15:
        if clv > 30000:
            return "📞 PROACTIVE: Valuable customer showing warning signs. Schedule personal check-in call and present loyalty rewards."
        else:
            return "👀 MONITOR: Elevated churn risk detected. Increase engagement through personalized offers and service improvements."
    else:
        if clv > 40000:
            return "⭐ NURTURE: High-value loyal customer. Continue VIP treatment and explore upsell opportunities."
        else:
            return "✅ MAINTAIN: Healthy customer relationship. Continue standard engagement and periodic satisfaction surveys."


"""WE SHOULD USE "0.3" AS OUR THRESHOLD TO ALIGN WITH OUR CLASSIFICATION MODEL"""
def get_confidence_level(churn_prob: float) -> str:
    """Determine model confidence based on prediction probability."""
    
    # Very High confidence: probability extremely low or extremely high
    if churn_prob < 0.1 or churn_prob > 0.9:
        return "Very High"
    
    # High confidence: still far from 0.5, but not extreme
    elif (0.1 <= churn_prob < 0.2) or (0.8 < churn_prob <= 0.9):
        return "High"
    
    # Moderate confidence: moderately far from 0.5
    elif (0.2 <= churn_prob < 0.3) or (0.7 < churn_prob <= 0.8):
        return "Moderate"
    
    # Low confidence: close to uncertainty zone
    else:
        return "Low"


@app.get("/online")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "TeleLink Customer Analytics API",
        "version": "2.0.0",
        "models_loaded": churn_model is not None and clv_model is not None
    }


@app.get("/health")
async def health_check():
    """Detailed health check including model status."""
    return {
        "status": "healthy" if (churn_model and clv_model) else "degraded",
        "churn_model": "loaded" if churn_model else "not loaded",
        "clv_model": "loaded" if clv_model else "not loaded",
        "api_version": "2.0.0"
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_customer(customer: CustomerData):
    """
    Predict customer churn probability and lifetime value.
    
    This endpoint analyzes customer data and returns:
    - Churn probability (0-1 scale)
    - Risk categorization (Low/Medium/High)
    - Estimated Customer Lifetime Value (CLV)
    - Actionable recommendations
    """
    # Check if models are loaded
    if churn_model is None or clv_model is None:
        raise HTTPException(
            status_code=503,
            detail="ML models not loaded. Please ensure model files are available."
        )
    
    try:
        # Prepare input data
        input_data = prepare_input_data(customer)
        
        # Predict churn probability
        churn_prob = churn_model.predict_proba(input_data)[0][1]  # Probability of class 1 (churn)
        
        # Predict CLV
        estimated_clv = clv_model.predict(input_data)[0]
        
        # Determine risk level
        # """WE SHOULD USE "0.3" AS OUR THRESHOLD TO ALIGN WITH OUR CLASSIFICATION MODEL"""
        if churn_prob > 0.3:
            risk_level = "High"
        elif churn_prob > 0.15:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        # Generate recommendation
        recommendation = get_recommendation(churn_prob, estimated_clv)
        
        # Get confidence level
        confidence = get_confidence_level(churn_prob)
        
        return PredictionResponse(
            churn_probability=float(churn_prob),
            churn_risk=risk_level,
            estimated_clv=float(estimated_clv),
            recommendation=recommendation,
            confidence=confidence
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )


@app.post("/batch-predict")
async def batch_predict(customers: list[CustomerData]):
    """
    Batch prediction endpoint for multiple customers.
    Returns predictions for all customers in the request.
    """
    if churn_model is None or clv_model is None:
        raise HTTPException(
            status_code=503,
            detail="ML models not loaded."
        )
    
    try:
        results = []
        for customer in customers:
            input_data = prepare_input_data(customer)
            churn_prob = churn_model.predict_proba(input_data)[0][1]
            estimated_clv = clv_model.predict(input_data)[0]
            
            risk_level = "High" if churn_prob > 0.4 else "Medium" if churn_prob > 0.2 else "Low"
            
            results.append({
                "churn_probability": float(churn_prob),
                "churn_risk": risk_level,
                "estimated_clv": float(estimated_clv),
                "recommendation": get_recommendation(churn_prob, estimated_clv),
                "confidence": get_confidence_level(churn_prob)
            })
        
        return {"predictions": results, "count": len(results)}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch prediction error: {str(e)}"
        )


@app.get("/stats")
async def get_statistics():
    """
    Return aggregate statistics and insights.
    In production, this would query a database.
    """
    return {
        "total_customers": 1_200_000,
        "active_customers": 1_029_600,
        "churned_customers": 170_400,
        "churn_rate": 0.142,
        "avg_clv": 32_450,
        "monthly_revenue": 8_900_000,
        "high_risk_customers": 168_000,
        "medium_risk_customers": 216_000,
        "low_risk_customers": 816_000
    }


if __name__ == "__main__":
    # Run the server
    print("🚀 Starting TeleLink Customer Analytics API...")
    print("📊 Loading ML models...")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📖 API documentation at: http://localhost:8000/docs")
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
