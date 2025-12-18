"""
Test script to verify the Twilio webhook endpoint is accessible
"""
import requests

# Replace this with your actual localtunnel URL
TUNNEL_URL = input("Enter your localtunnel URL (e.g., https://xxxx.loca.lt): ").strip()

# Remove trailing slash if present
if TUNNEL_URL.endswith('/'):
    TUNNEL_URL = TUNNEL_URL[:-1]

webhook_url = f"{TUNNEL_URL}/twilio-whatsapp"

# Test with a sample Twilio webhook payload
test_data = {
    "From": "whatsapp:+1234567890",
    "Body": "test message"
}

print(f"\nTesting webhook at: {webhook_url}")
print(f"Sending test data: {test_data}\n")

try:
    response = requests.post(webhook_url, data=test_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body:\n{response.text[:500]}")
    
    if response.status_code == 200:
        print("\n✅ SUCCESS! Your webhook is working!")
    else:
        print(f"\n⚠️  Warning: Received status code {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("❌ ERROR: Could not connect to the URL. Make sure:")
    print("   1. localtunnel is running (lt --port 8000)")
    print("   2. Your FastAPI server is running (uvicorn main:app --host 0.0.0.0 --port 8000)")
    print("   3. The URL is correct")
except Exception as e:
    print(f"❌ ERROR: {e}")






