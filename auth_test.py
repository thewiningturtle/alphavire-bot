import os
import tweepy

print("\n🔍 Testing individual credentials:")

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

print("✅ API_KEY is set:", API_KEY[:4] + "..." if API_KEY else "❌ MISSING")
print("✅ API_SECRET is set:", API_SECRET[:4] + "..." if API_SECRET else "❌ MISSING")
print("✅ ACCESS_TOKEN is set:", ACCESS_TOKEN[:4] + "..." if ACCESS_TOKEN else "❌ MISSING")
print("✅ ACCESS_SECRET is set:", ACCESS_SECRET[:4] + "..." if ACCESS_SECRET else "❌ MISSING")

print("\n🔐 Testing OAuth1 connection to Twitter...")

try:
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    user = api.verify_credentials()
    print("✅ Twitter OAuth authentication successful.")
    print(f"🔁 Authenticated as: @{user.screen_name}")
except Exception as e:
    print("❌ Twitter OAuth authentication FAILED:", e)
