import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_article(title, url):
    try:
        prompt = (
            f"Summarize the following news article title in 2–3 lines for a Twitter audience.\n\n"
            f"Title: {title}\n"
            f"Link: {url}\n\n"
            f"Keep it factual, engaging, and suitable for investors.\n"
            f"Don't mention the word 'summary'."
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can upgrade to gpt-4 later
            messages=[
                {"role": "system", "content": "You are a financial analyst writing tweet-sized summaries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )

        summary = response['choices'][0]['message']['content'].strip()
        return summary

    except Exception as e:
        print("❌ OpenAI summary failed:", e)
        return None
