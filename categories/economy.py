import openai
import os
import datetime
import random

openai.api_key = os.getenv("OPENAI_API_KEY")

ECON_INDICATORS = [
    "Consumer Price Index (CPI)",
    "Unemployment Rate",
    "Federal Funds Rate",
    "Gross Domestic Product (GDP)",
    "Personal Consumption Expenditures (PCE)",
    "Producer Price Index (PPI)",
    "Retail Sales",
    "U.S. Treasury Yield Curve",
    "ISM Manufacturing Index",
    "Initial Jobless Claims"
]

def generate_economy_post():
    indicator = random.choice(ECON_INDICATORS)
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    prompt = f"""
    Write a casual, human-like blog post in HTML format about the economic indicator "{indicator}" for a U.S.-based audience.
    - Explain the indicator in plain language, as if you're writing a Reddit post.
    - Use short and long sentences mixed, include a few rhetorical questions, and vary the paragraph lengths.
    - Mention a fictional recent number and what it might mean for everyday people.
    - Format the text using basic HTML like <h2>, <p>, and <ul> if helpful.
    - Wrap it up with something slightly opinionated or speculative (e.g. "maybe we're heading for a slowdown?").
    - Date: {today}.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a financial blogger who writes casually but accurately for U.S. readers."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.85,
            max_tokens=1400
        )

        content = response.choices[0].message.content.strip()
        title = f"What's Going On With {indicator}? [{today}]"

        tags = [
            "us economy", "economic update", indicator.lower(),
            "daily economics", "finance", "market trends", "data analysis"
        ]

        return {
            "title": title,
            "content": content,
            "category": "economy",
            "tags": tags
        }

    except Exception as e:
        return {
            "title": f"US Economy Update (Error)",
            "content": f"⚠️ Failed to generate economy post due to: {e}",
            "category": "economy",
            "tags": ["economy", "error"]
        }
