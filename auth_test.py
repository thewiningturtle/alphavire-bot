import os
import tweepy

# Load from environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

def test_credential(name, value):
    if not value:
        print(f"❌ {name} is missing (None or empty)")
    else:
        print(f"✅ {name} is set")

def test_twitter_auth():
    print("\n🔍 Testing individual credentials:")
    test_credential("API_KEY", API_KEY)
    test_credential("API_SECRET", API_SECRET)
    test_credential("ACCESS_TOKEN", ACCESS_TOKEN)
    test_credential("ACCESS_SECRET", ACCESS_SECRET)

    print("\n🔐 Testing OAuth1 connection to Twitter...")
    try:
        auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
        api = tweepy.API(auth)
        api.verify_credentials()
        print("✅ Twitter OAuth 1.0a authentication SUCCESSFUL.")
    except Exception as e:
        print(f"❌ Twitter OAuth authentication FAILED: {e}")

if __name__ == "__main__":
    test_twitter_auth()
