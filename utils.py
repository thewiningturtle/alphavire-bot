import feedparser
import json
import random
import requests
import time
from thread_builder import post_thread

HISTORY_FILE = "history.json"

RSS_FEEDS = [
    "https://feeds.reuters.com/reuters/topNews",
    "https://economictimes.indiatimes.com/rssfeedsdefault.cms",
    "https://www.moneycontrol.com/rss/latestnews.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
]

FALLBACK_TEMPLATES = [
    "Markets are reacting sharply to new developments.",
    "This update may influence investor sentiment.",
    "Analysts see opportunities amid the shift.",
    "Time to revisit portfolios amid the latest news.",
    "Here's a key update shaping today's market."
]

HASHTAGS = ["#Breaking", "#StockMarket", "#Finance", "#India", "#Markets"]


def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)["posted"]
    except:
        return []

def save_to_history(headline):
    try:
        history = load_history()
        history.insert(0, headline)
        history = history[:50]
        with open(HISTORY_FILE, "w") as f:
            json.dump({"posted": history}, f)
    except Exception as e:
        print("❌ Error saving history:", e)


def fetch_and_tweet(client):
    print("🔍 Checking RSS feeds...")

    for _ in range(len(RSS_FEEDS)):
        url = random.choice(RSS_FEEDS)
        feed = feedparser.parse(url)
        print(f"📥 {len(feed.entries)} headlines fetched from {url}")
        if feed.entries:
            break
    else:
        print("⚠️ All RSS feeds returned 0 headlines. Skipping tweet.")
        return

    history = load_history()

    for entry in feed.entries:
        headline = entry.title.strip()
        if headline in history:
            print(f"⏭️ Skipping duplicate: {headline}")
            continue

        print(f"⚡ Preparing thread for: {headline}")

        # 🧠 Use headline if short, else fallback to template
        if len(headline) <= 250:
            summary = headline
        else:
            summary = random.choice(FALLBACK_TEMPLATES)

        try:
            post_thread(
                client,
                title=headline,
                body=summary,
                url=entry.link,
                hashtags=HASHTAGS
            )
            save_to_history(headline)
            time.sleep(10)
            break
        except Exception as e:
            print("❌ Error posting thread:", e)
            if "429" in str(e):
                print("⏳ Sleeping for 60 seconds due to rate limiting...")
                time.sleep(60)
            break


def fetch_market_update(client):
    try:
        print("📊 Fetching market update...")
        nifty = get_yahoo_quote("^NSEI")
        sensex = get_yahoo_quote("^BSESN")

        if not nifty or not sensex:
            print("⚠️ Market data unavailable.")
            return

        tweet = (
            f"📊 MARKET UPDATE\n"
            f"Nifty 50: {nifty['price']} {nifty['change']}\n"
            f"Sensex: {sensex['price']} {sensex['change']}\n"
            f"Updated: 2 PM IST"
        )
        print(f"⚡ Tweeting market update:\n{tweet}")
        api.update_status(...)
    except Exception as e:
        print("❌ Error posting market update:", e)


def get_yahoo_quote(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        r = requests.get(url).json()
        meta = r['chart']['result'][0]['meta']
        price = meta['regularMarketPrice']
        prev_close = meta['previousClose']
        change = price - prev_close
        pct = (change / prev_close) * 100
        emoji = "🔼" if change > 0 else "🔽"
        return {
            "price": f"{price:.2f}",
            "change": f"{emoji} {abs(change):.2f} ({pct:.2f}%)"
        }
    except Exception as e:
        print(f"❌ Error fetching {symbol}:", e)
        return None
