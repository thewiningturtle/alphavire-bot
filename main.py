import os
import time
import schedule
import feedparser
import tweepy
from utils import clean_text, extract_summary
from thread_builder import build_thread
from keep_alive import keep_alive

# 🌐 Load credentials from Railway/Replit environment
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# ✅ Authenticate using Twitter v2 Client (Essential Tier Safe)
try:
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_SECRET
    )
    print("✅ Twitter v2 authentication successful.")
except Exception as e:
    print("❌ Twitter v2 authentication failed:", e)

# ✅ RSS feed list
RSS_FEEDS = [
    "https://feeds.reuters.com/reuters/topNews",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://economictimes.indiatimes.com/rssfeedsdefault.cms",
    "https://www.moneycontrol.com/rss/latestnews.xml",
]

# ✅ Track posted headlines to prevent duplicates
posted_headlines = set()

# ✅ Function to fetch and tweet

def fetch_and_tweet():
    print("\n🔍 Checking RSS feeds...")
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        print(f"📥 {len(feed.entries)} headlines fetched from {feed_url}")
        for entry in feed.entries:
            headline = entry.title.strip()
            url = entry.link.strip()

            if headline in posted_headlines:
                print(f"⏭️ Skipping duplicate: {headline}")
                continue

            print(f"⚡ Preparing thread for: {headline}")
            try:
                summary = extract_summary(entry)
                thread = build_thread(headline, summary, url)

                print(f"✍️ Tweeting thread for: {headline}")
                response = client.create_tweet(text=thread[0])  # Safe for v2
                posted_headlines.add(headline)
                time.sleep(5)
            except Exception as e:
                print("❌ Error posting tweet:", e)
            break  # Post only one per feed check

# ✅ Keep-alive server
keep_alive()

# 🕰️ Schedule tweets (UTC time for Railway/Replit)
schedule.every().day.at("04:30").do(fetch_and_tweet)  # 10:00 AM IST
schedule.every().day.at("08:30").do(fetch_and_tweet)  # 2:00 PM IST
schedule.every().day.at("11:30").do(fetch_and_tweet)  # 5:00 PM IST
schedule.every().day.at("13:30").do(fetch_and_tweet)  # 7:00 PM IST
schedule.every().day.at("15:30").do(fetch_and_tweet)  # 9:00 PM IST
schedule.every().day.at("17:30").do(fetch_and_tweet)  # 11:00 PM IST
schedule.every().day.at("19:30").do(fetch_and_tweet)  # 1:00 AM IST

# 🔁 Keep checking every 30s
while True:
    schedule.run_pending()
    time.sleep(30)
