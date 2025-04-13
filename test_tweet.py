import os
import tweepy

auth = tweepy.OAuth1UserHandler(
    os.getenv("API_KEY"),
    os.getenv("API_SECRET"),
    os.getenv("ACCESS_TOKEN"),
    os.getenv("ACCESS_SECRET")
)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("✅ Auth passed!")

    status = api.update_status("✅ This is a test tweet from Railway bot.")
    print("✅ Tweet posted successfully!", status.id)
except Exception as e:
    print("❌ Failed:", e)
