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
You are a U.S.-based economics blogger. Write an HTML-formatted blog post on the indicator "{indicator}" with today's date ({today}).
Explain the indicator simply, mention how it's measured, and present a fictional but reasonable recent data point.
Use <h2>, <h3>, <p> for structure. No Markdown. Add source names like FRED or BEA at the bottom as references.
Add variety in paragraph length and human tone.
"""

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1400
    )

    content = response.choices[0].message.content.strip()
    title = f"{indicator} [{today}]"

    tags = ["US economy", "economic indicators", indicator, "inflation", "interest rates", "finance", "FRED", "investment"]

    return {
        "title": title,
        "content": content,
        "category": "economy",
        "tags": tags
    }
