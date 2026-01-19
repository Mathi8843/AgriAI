import requests

BASE_URL = "http://127.0.0.1:8000"

def test_nlp():
    test_cases = [
        ("Which crop should I grow in winter?", "CROP_RECOMMENDATION"),
        ("I see yellow spots on my leaves", "DISEASE_DIAGNOSIS"),
        ("What is the price of wheat today?", "MARKET_PRICE"),
        ("Will it rain tomorrow?", "WEATHER_ADVISORY"),
        ("Show my farm profile details", "PROFILE_QUERY"),
        ("Hello, who are you?", "GENERAL_HELP"),
        ("Something completely random 12345", "GENERAL_HELP") # Fallback
    ]

    print("Testing NLP Module...")
    
    for query, expected_intent in test_cases:
        payload = {
            "farmer_id": "test-id",
            "query": query
        }
        try:
            response = requests.post(f"{BASE_URL}/nlp/intent", json=payload)
            data = response.json()
            intent = data.get("intent")
            confidence = data.get("confidence")
            
            status = "✅ PASS" if intent == expected_intent else f"❌ FAIL (Got {intent})"
            print(f"{status} | Query: '{query}' -> Intent: {intent} ({confidence})")
        except Exception as e:
            print(f"❌ ERROR | Query: '{query}' -> {str(e)}")

if __name__ == "__main__":
    test_nlp()
