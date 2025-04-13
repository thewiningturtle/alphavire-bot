import os
import tweepy

# 🔐 Load credentials from environment
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# ✅ Authenticate with Twitter using OAuth 1.0a
auth = tweepy.OAuth1UserHandler(
    API_KEY,
    API_SECRET,
    ACCESS_TOKEN,
    ACCESS_SECRET
)

api = tweepy.API(auth)

# ✅ Try tweeting
try:
    api.verify_credentials()
    print("✅ Twitter OAuth 1.0a authentication successful.")
    
    # 🐦 Test tweet
    tweet = api.update_status("🚀 Hello from AlphaVire on Railway! Testing successful. #BotTest")
    print(f"✅ Tweet posted! ID: {tweet.id}")
except Exception as e:
    print("❌ Tweet failed:", e)
