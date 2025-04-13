import os
import tweepy
from keep_alive import keep_alive

# 🔐 1. Load Twitter API credentials from environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

print("🔐 DEBUG CHECK")
print("API_KEY:", API_KEY[:5], "...[hidden]")
print("ACCESS_TOKEN:", ACCESS_TOKEN[:5], "...[hidden]")

# 🔑 2. Authenticate with Twitter using OAuth 1.0a
try:
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_SECRET
    )
    print("✅ Twitter OAuth1.0a authentication initialized.")
except Exception as e:
    print("❌ Authentication failed:", e)

# 🧪 3. Temporary test tweet to confirm working deployment
try:
    response = client.create_tweet(text="🚀 AlphaVire Test Tweet from Railway!")
    print("✅ Tweet posted successfully.")
except Exception as e:
    print("❌ Tweet failed:", e)

# 🕸️ 4. Start Flask server to stay alive on Railway
keep_alive()
