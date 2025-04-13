import textwrap
import time

def post_thread(client, title, body, url, hashtags=None):
    print(f"✍️ Tweeting thread for: {title}")
    hashtag_text = " ".join(hashtags or [])

    wrapped = textwrap.wrap(body, width=250)
    tweet_parts = []

    for part in wrapped:
        tweet_parts.append(part)

    # Add the link + hashtags in the last tweet
    if tweet_parts:
        tweet_parts[-1] += f"\n\n🔗 {url}\n{hashtag_text}"
    else:
        tweet_parts.append(f"🔗 {url}\n{hashtag_text}")

    try:
        prev_tweet = None
        for i, part in enumerate(tweet_parts):
            # Add 1/N prefix only if multiple tweets
            prefix = f"{i+1}/{len(tweet_parts)} " if len(tweet_parts) > 1 else ""
            text = f"{prefix}{part}"

            tweet = client.create_tweet(
                text=text,
                in_reply_to_tweet_id=prev_tweet.id if prev_tweet else None
            )

            prev_tweet = tweet.data
            print(f"✅ Posted: {text[:50]}...")
            time.sleep(3)  # Delay between tweets to avoid rate limits

        print("🧵 Thread posted successfully.")

    except Exception as e:
        print("❌ Error posting tweet:", e)
        if "429" in str(e):
            print("⏳ Rate limit hit. Sleeping for 15 minutes...")
            time.sleep(900)
