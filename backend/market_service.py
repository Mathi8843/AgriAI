import random
from datetime import datetime

# Mock Database of Market Prices
# Structure: Crop -> Location -> Price Info
MARKET_DATA = {
    "rice": {
        "chennai": {"price": 2500, "unit": "INR/quintal"},
        "madurai": {"price": 2450, "unit": "INR/quintal"},
        "default": {"price": 2480, "unit": "INR/quintal"}
    },
    "wheat": {
        "delhi": {"price": 2100, "unit": "INR/quintal"},
        "punjab": {"price": 2050, "unit": "INR/quintal"},
        "default": {"price": 2080, "unit": "INR/quintal"}
    },
    "tomato": {
        "bangalore": {"price": 1200, "unit": "INR/quintal"},
        "chennai": {"price": 1350, "unit": "INR/quintal"},
        "default": {"price": 1250, "unit": "INR/quintal"}
    },
    "potato": {
        "mumbai": {"price": 900, "unit": "INR/quintal"},
        "agra": {"price": 850, "unit": "INR/quintal"},
        "default": {"price": 880, "unit": "INR/quintal"}
    },
    "cotton": {
        "default": {"price": 6200, "unit": "INR/quintal"}
    }
}

def get_market_price(crop: str, location: str = ""):
    crop_lower = crop.lower()
    location_lower = location.lower() if location else "default"
    
    # Check if crop exists
    if crop_lower not in MARKET_DATA:
        # Fallback for unknown crops
        return {
            "crop": crop,
            "location": location if location else "General Market",
            "price": random.randint(1000, 5000), # Random fallback
            "unit": "INR/quintal",
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "note": "Estimated price (Data unavailable)"
        }
    
    crop_data = MARKET_DATA[crop_lower]
    
    # Check if location exists for crop
    if location_lower in crop_data:
        data = crop_data[location_lower]
        loc_name = location
    else:
        data = crop_data["default"]
        loc_name = "National Average" if not location else f"{location} (Avg)"
        
    return {
        "crop": crop,
        "location": loc_name,
        "price": data["price"],
        "unit": data["unit"],
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }
