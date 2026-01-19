import requests

BASE_URL = "http://127.0.0.1:8000"

def test_ml():
    # Rice-like conditions
    payload = {
        "farmer_id": "test-farmer",
        "N": 90,
        "P": 42,
        "K": 43,
        "ph": 6.5,
        "temperature": 20.8,
        "humidity": 82.0,
        "rainfall": 202.9
    }
    
    print("Testing Crop Recommendation...")
    try:
        response = requests.post(f"{BASE_URL}/crop/recommend", json=payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Success!")
            print(f"Recommended: {data['recommended_crop']}")
            print(f"Confidence: {data['confidence']}")
            print("Explanation:")
            for reason in data['explanation']:
                print(f" - {reason}")
        else:
            print(f"❌ Failed: {response.status_code} {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_ml()
