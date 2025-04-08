# categories/economy.py

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
Write a detailed and professional blog post targeted at U.S. readers explaining the latest status of the economic indicator: "{indicator}".
Use a tone that is informative, neutral, and slightly analytical. Explain what the indicator is, how it's measured, the most recent value (can be fictional), and what it implies about the economy.
Mention possible impacts on consumers and investors. Include references to sources like FRED, BLS, or BEA at the end.
Use 4–6 paragraphs. Use today's date in the title.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an economics writer for a financial blog targeting U.S. readers."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1300
        )

        content = response.choices[0].message.content.strip()
        title = f"{indicator} [{today}]"

        tags = [
            "US economy", "economic indicators", indicator,
            "inflation", "interest rates", "finance", "FRED", "investment"
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
