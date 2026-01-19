import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    # 1. Register Farmer
    payload = {
        "name": "Ramesh Kumar",
        "language": "Hindi",
        "location": "Punjab",
        "farm_size": 5.5,
        "soil_type": "Loam",
        "irrigation_type": "Drip",
        "primary_crop": "Wheat"
    }
    
    print("Testing Registration...")
    response = requests.post(f"{BASE_URL}/farmer/register", json=payload)
    if response.status_code == 200:
        print("Registration Success:", response.json())
        farmer_id = response.json()["id"]
    else:
        print("Registration Failed:", response.text)
        return

    # 2. Get Farmer
    print(f"\nTesting Get Profile ({farmer_id})...")
    response = requests.get(f"{BASE_URL}/farmer/{farmer_id}")
    if response.status_code == 200:
        print("Get Profile Success:", response.json())
    else:
        print("Get Profile Failed:", response.status_code)

    # 3. Update Farmer
    update_payload = payload.copy()
    update_payload["name"] = "Ramesh Kumar Updated"
    
    print(f"\nTesting Update Profile ({farmer_id})...")
    response = requests.put(f"{BASE_URL}/farmer/{farmer_id}", json=update_payload)
    if response.status_code == 200:
        print("Update Success:", response.json())
    else:
        print("Update Failed:", response.status_code)

if __name__ == "__main__":
    test_api()
