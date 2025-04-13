import requests
from bs4 import BeautifulSoup
import random
import re
import os
from tweepy import OAuth1UserHandler, API

# --- Helper functions ---

def extract_og_image(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")
        og_image = soup.find("meta", property="og:image")
        return og_image["content"] if og_image else None
    except Exception as e:
        print("❌ Error extracting OG image:", e)
        return None

def extract_summary(title):
    try:
        # Simulated summary line
        phrases = [
            "Here's what you need to know 👇",
            "Key insight from this update 👇",
            "Get the quick summary 👇"
        ]
        return f"{title}\n\n{random.choice(phrases)}"
    except Exception:
        return title

def generate_hashtags(text, max_tags=3):
    keywords = re.findall(r'\b[A-Z][a-z]{2,}\b', text)
    keywords = list(set(k.lower() for k in keywords))[:max_tags]
    return " ".join([f"#{kw.capitalize()}" for kw in keywords if kw])

# --- Main tweet function ---

def post_tweet_with_image(client, text, url):
    print("🔎 Extracting OG image from:", url)
    image_url = extract_og_image(url)

    if not image_url:
        print("⚠️ No image found. Tweeting text only.")
        try:
            client.create_tweet(text=text)
            print("✅ Tweeted without image.")
        except Exception as e:
            print("❌ Error posting plain tweet:", e)
        return

    try:
        # Download the image temporarily
        image_data = requests.get(image_url).content
        with open("temp_img.jpg", "wb") as f:
            f.write(image_data)

        # Upload image using v1.1 API
        auth = OAuth1UserHandler(
            os.getenv("API_KEY"),
            os.getenv("API_SECRET"),
            os.getenv("ACCESS_TOKEN"),
            os.getenv("ACCESS_TOKEN_SECRET")
        )
        api_v1 = API(auth)
        media = api_v1.media_upload("temp_img.jpg")

        tweet_text = f"{extract_summary(text)}\n\n{generate_hashtags(text)}"
        tweet_text = tweet_text[:275]  # Safety limit for tweet length

        client.create_tweet(text=tweet_text, media_ids=[media.media_id])
        print("✅ Tweeted with image.")
    except Exception as e:
        print("❌ Error posting tweet with image:", e)
