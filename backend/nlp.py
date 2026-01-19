from typing import Dict, List, Tuple

# Simple Keyword-based Intent Classification
INTENT_KEYWORDS = {
    "CROP_RECOMMENDATION": ["crop", "grow", "plant", "sow", "cultivate", "harvest", "yield"],
    "DISEASE_DIAGNOSIS": ["disease", "spot", "leaf", "infection", "fungus", "pest", "yellow", "rot"],
    "MARKET_PRICE": ["price", "rate", "market", "cost", "value", "sell"],
    "WEATHER_ADVISORY": ["weather", "rain", "temperature", "forecast", "climate", "humid", "wind"],
    "PROFILE_QUERY": ["profile", "farm", "detail", "info", "my data"],
    "GENERAL_HELP": ["help", "assist", "support", "hello", "hi", "start"]
}

DEFAULT_INTENT = "GENERAL_HELP"
DEFAULT_CONFIDENCE = 0.5

def classify_intent(text: str) -> Dict[str, any]:
    """
    Classifies the user's intent based on keyword matching.
    Returns a dictionary with intent, confidence, and recommended next module route.
    """
    text = text.lower()
    
    best_intent = DEFAULT_INTENT
    max_matches = 0
    total_matches = 0
    
    # Count matches for each intent
    match_counts = {}
    for intent, keywords in INTENT_KEYWORDS.items():
        count = sum(1 for word in keywords if word in text)
        match_counts[intent] = count
        total_matches += count
        
        if count > max_matches:
            max_matches = count
            best_intent = intent
            
    # Calculate confidence based on 'strength' of match relative to others and text length
    # This is a very basic heuristic.
    if max_matches > 0:
        confidence = 0.7 + (0.05 * max_matches) # Base 0.7 + boost for more keywords
        confidence = min(confidence, 0.99)
    else:
        confidence = DEFAULT_CONFIDENCE # Low confidence if no keywords found at all
        best_intent = DEFAULT_INTENT # Fallback if absolutely nothing matches (or maybe GENERAL_HELP)

    # Determine routing
    routes = {
        "CROP_RECOMMENDATION": "/crop/recommend",
        "DISEASE_DIAGNOSIS": "/disease/diagnose",
        "MARKET_PRICE": "/market/prices",
        "WEATHER_ADVISORY": "/weather/details",
        "PROFILE_QUERY": "/farmer/{farmer_id}",
        "GENERAL_HELP": "/help"
    }

    return {
        "intent": best_intent,
        "confidence": round(confidence, 2),
        "next_module": routes.get(best_intent, "/help")
    }
