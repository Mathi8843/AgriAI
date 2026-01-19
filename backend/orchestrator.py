import nlp
import market_service
import ml_service

def process_query(text: str, farmer_id: str) -> str:
    """
    Orchestrate the flow: Text -> Intent -> Action -> Response Text
    """
    # 1. Detect Intent
    intent_result = nlp.classify_intent(text)
    intent = intent_result["intent"]
    confidence = intent_result["confidence"]
    
    print(f"Orchestrator: '{text}' -> {intent} ({confidence})")

    # 2. Add Logic based on Intent
    if intent == "MARKET_PRICE":
        # Extract entities (Simple logic for demo)
        # Check for crop names in text
        found_crop = None
        for crop in ["rice", "wheat", "tomato", "potato", "cotton"]:
            if crop in text.lower():
                found_crop = crop
                break
        
        # Check for location
        found_location = None
        cities = ["chennai", "madurai", "delhi", "punjab", "bangalore", "mumbai"]
        for city in cities:
            if city in text.lower():
                found_location = city
                break
        
        if found_crop:
            data = market_service.get_market_price(found_crop, found_location)
            return f"The price of {data['crop']} in {data['location']} is {data['price']} rupees per quintal."
        else:
            return "I understood you mistakenly asked about market prices, but I couldn't catch the crop name. Please mention a crop like Rice or Wheat."

    elif intent == "CROP_RECOMMENDATION":
        # Voice is hard for full form data. 
        # We can simulate a response or ask them to use the screen.
        return "To recommend the best crop, I need soil details like Nitrogen and pH. Please use the Crop Recommendation section in the app for accurate results."
    
    elif intent == "WEATHER_ADVISORY":
         return "I can't fetch live weather yet, but it looks like a good day for farming."

    elif intent == "GENERAL_HELP":
        return "I can help you with Market Prices, Crop Recommendations, and typical farming questions. Just ask!"

    return "I am not sure how to help with that yet."
