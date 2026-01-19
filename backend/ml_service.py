import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import shap
import os

# Global Model & Explainer
model = None
explainer = None
label_encoder = None
feature_names = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

def train_model():
    global model, explainer, label_encoder
    
    csv_path = "dataset/Crop_recommendation.csv"
    if not os.path.exists(csv_path):
        print("Dataset not found! Skipping training.")
        return

    print("Loading dataset...")
    df = pd.read_csv(csv_path)
    
    X = df[feature_names]
    y = df["label"]

    # Encode Labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    # Train Random Forest
    print("Training Random Forest...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    print(f"Model Accuracy on Test: {model.score(X_test, y_test):.2f}")

    # Setup SHAP Explainer
    # TreeExplainer is fast for trees
    print("Initializing SHAP Explainer...")
    explainer = shap.TreeExplainer(model)
    
    print("ML Service Ready.")

def predict_crop(features: dict):
    if not model:
        return None, 0.0, ["Model not trained"]

    # Convert input dict to DataFrame
    input_df = pd.DataFrame([features], columns=feature_names)
    
    # Predict
    prediction_idx = model.predict(input_df)[0]
    predicted_crop = label_encoder.inverse_transform([prediction_idx])[0]
    
    # Confidence
    probs = model.predict_proba(input_df)[0]
    confidence = float(probs[prediction_idx])

    # Explain with SHAP
    explanation = explain_prediction(input_df)

    return predicted_crop, confidence, explanation

def explain_prediction(input_df):
    """
    Generates human-readable explanation using SHAP values.
    """
    shap_values = explainer.shap_values(input_df)
    
    # For multiclass, shap_values is a list of arrays (one for each class).
    # We need the array for the predicted class.
    prediction_idx = model.predict(input_df)[0]
    
    # shap_values[prediction_idx] -> shape (1, n_features)
    # We want the first sample
    vals = shap_values[prediction_idx][0]
    
    # Create (feature, shap_value) pairs
    feature_contributions = list(zip(feature_names, vals))
    
    # Sort by absolute impact (descending)
    feature_contributions.sort(key=lambda x: abs(x[1]), reverse=True)
    
    reasons = []
    for feature, impact in feature_contributions[:3]: # Top 3 reasons
        # Heuristic to translate to text
        # If impact is positive -> it supported this class
        # If input value is high/low relative to something? 
        # For simplicity, we just state the feature and its value roughly
        
        val = input_df.iloc[0][feature]
        
        if impact > 0:
            if feature == "rainfall" and val > 150:
                reasons.append(f"High Rainfall ({val}mm) suits this crop")
            elif feature == "temperature" and val > 25:
                 reasons.append(f"Warm temperature ({val}°C)")
            elif feature == "temperature" and val < 20:
                 reasons.append(f"Cool temperature ({val}°C)")
            else:
                 reasons.append(f"Suitable {feature} levels ({val})")
        
    if not reasons:
        reasons = ["Generalized favorable conditions"]
        
    return reasons

# Initialize on import (if script runs) or manual call
if __name__ == "__main__":
    train_model()
