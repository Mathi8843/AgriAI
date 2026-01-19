import requests

BASE_URL = "http://127.0.0.1:8000"

def test_market():
    test_cases = [
        ("rice", "chennai"),
        ("rice", "unknown_city"),
        ("wheat", None),
        ("unknown_crop", "delhi")
    ]
    
    print("Testing Market Price Module...")
    
    for crop, location in test_cases:
        params = {"crop": crop}
        if location:
            params["location"] = location
            
        try:
            response = requests.get(f"{BASE_URL}/market/price", params=params)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success | {crop} @ {data['location']}: {data['price']} {data['unit']}")
            else:
                print(f"❌ Failed | {crop}: {response.status_code}")
        except Exception as e:
            print(f"❌ Error | {crop}: {e}")

if __name__ == "__main__":
    test_market()
