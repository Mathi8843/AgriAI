from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
import shutil
import os

# Create tables
# WARNING: Dropping all tables to handle schema change for Auth. 
# In production, use migrations (Alembic).
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://example.com', 'http://localhost:3000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import nlp
import ml_service
import market_service
from typing import Optional

# Startup Event to train/load model
@app.on_event("startup")
def startup_event():
    ml_service.train_model()

# Request Models
class IntentRequest(BaseModel):
    farmer_id: str
    query: str

class CropRequest(BaseModel):
    farmer_id: str
    N: float
    P: float
    K: float
    ph: float
    temperature: float
    humidity: float
    rainfall: float

@app.get("/market/price")
def get_market_price(crop: str, location: Optional[str] = None):
    return market_service.get_market_price(crop, location if location else "")

@app.post("/crop/recommend")
def recommend_crop(request: CropRequest):
    features = {
        "N": request.N,
        "P": request.P,
        "K": request.K,
        "ph": request.ph,
        "temperature": request.temperature,
        "humidity": request.humidity,
        "rainfall": request.rainfall
    }
    
    crop, confidence, explanation = ml_service.predict_crop(features)
    
    return {
        "recommended_crop": crop,
        "confidence": round(confidence, 2),
        "explanation": explanation
    }

@app.post("/voice/query")
async def voice_query(farmer_id: str, file: UploadFile = File(...)):
    # 1. Save uploaded file
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # 2. Transcribe
        # Note: raw audio from phone might need conversion (e.g. m4a to wav). 
        # SpeechRecognition prefers WAV. We might need pydub here if frontend sends m4a.
        # For now assuming frontend ensures compatible format or valid header.
        text = voice_service.transcribe_audio(file_location)
        
        # 3. Orchestrate
        if not text:
            response_text = "Sorry, I couldn't hear you clearly."
        else:
            response_text = orchestrator.process_query(text, farmer_id)
            
        # 4. Generate Audio Response
        audio_filename = voice_service.text_to_speech(response_text)
        audio_url = f"/static/{audio_filename}"
        
        return {
            "transcription": text,
            "text_response": response_text,
            "audio_url": audio_url
        }
        
    except Exception as e:
        print(f"Voice Error: {e}")
        return {"error": str(e)}
    finally:
        # Cleanup
        if os.path.exists(file_location):
            os.remove(file_location)

@app.post("/nlp/intent")
def detect_intent(request: IntentRequest):
    result = nlp.classify_intent(request.query)
    # If intent is CROP_RECOMMENDATION, Frontend should calculate if it has all data 
    # to call /crop/recommend immediately or ask user form.
    return result

@app.post("/auth/signup", response_model=models.FarmerResponse)
def signup(farmer: models.FarmerCreate, db: Session = Depends(get_db)):
    # Check if username exists
    db_user = db.query(models.Farmer).filter(models.Farmer.username == farmer.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Hash password
    hashed_password = auth.get_password_hash(farmer.password)
    
    # Create Farmer
    db_farmer = models.Farmer(
        username=farmer.username,
        password_hash=hashed_password,
        name=farmer.name,
        language=farmer.language,
        location=farmer.location,
        farm_size=farmer.farm_size,
        soil_type=farmer.soil_type,
        irrigation_type=farmer.irrigation_type,
        primary_crop=farmer.primary_crop
    )
    
    db.add(db_farmer)
    db.commit()
    db.refresh(db_farmer)
    return db_farmer

@app.post("/auth/login")
def login(login_data: models.FarmerLogin, db: Session = Depends(get_db)):
    farmer = db.query(models.Farmer).filter(models.Farmer.username == login_data.username).first()
    if not farmer:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    if not auth.verify_password(login_data.password, farmer.password_hash):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    return {
        "id": farmer.id,
        "username": farmer.username,
        "name": farmer.name
    }

# Original endpoint kept for compatibility but pointed to signup logic if needed, 
# or just removed. Let's keep /farmer/register pointing to signup but simplified, 
# assuming frontend now hits /auth/signup.


@app.get("/farmer/{farmer_id}", response_model=models.FarmerResponse)
def get_farmer_profile(farmer_id: str, db: Session = Depends(get_db)):
    farmer = db.query(models.Farmer).filter(models.Farmer.id == farmer_id).first()
    if farmer is None:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return farmer

@app.put("/farmer/{farmer_id}", response_model=models.FarmerResponse)
def update_farmer_profile(farmer_id: str, farmer_update: models.FarmerCreate, db: Session = Depends(get_db)):
    db_farmer = db.query(models.Farmer).filter(models.Farmer.id == farmer_id).first()
    if db_farmer is None:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    for key, value in farmer_update.dict().items():
        setattr(db_farmer, key, value)
    
    db.commit()
    db.refresh(db_farmer)
    return db_farmer

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
