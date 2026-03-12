import requests
import json

BASE_URL = "http://localhost:8080"

def test_ner():
    print("Testing NER...")
    text = "Tata Steel Ltd with CIN L27100MH1907PLC000260 deposited ₹ 1,25,000. GSTIN 27AAAAA0000A1Z5."
    try:
        response = requests.post(f"{BASE_URL}/ner", json={"text": text})
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")

def test_sentiment():
    print("\nTesting Sentiment...")
    headlines = ["Profit surges as demand rises", "Regulatory probe into coal mining"]
    try:
        response = requests.post(f"{BASE_URL}/sentiment", json={"headlines": headlines})
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")

def test_score():
    print("\nTesting Scoring...")
    features = {
        "ICR": 4.2,
        "DSCR": 1.8,
        "DE_Ratio": 0.4,
        "Sentiment": 0.7,
        "GST_Gap": 5,
        "Bank_Bounce": 0,
        "Litigation": 0
    }
    try:
        response = requests.post(f"{BASE_URL}/score", json={"features": features})
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Note: Ensure the Flask app is running on port 8080 before running this script.")
    # test_ner()
    # test_sentiment()
    # test_score()
    print("Verification script ready.")
