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
    "Initial Jobless Claims",
    "Consumer Sentiment Index",
    "Core Inflation Rate",
    "Labor Force Participation Rate"
]

def generate_economy_post():
    indicator = random.choice(ECON_INDICATORS)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    title = f"{indicator} [{today}]"

    prompt = f"""
Write an engaging and informative HTML-formatted blog post for U.S. readers explaining the current state of the economic indicator: "{indicator}".
Your writing should sound natural, like an email newsletter from a financial blogger—not overly technical.
Structure the post in HTML using <h2> for the title, <h3> for sections, <p> for text. Use varied sentence lengths and paragraph styles.

Include:
- A plain-English explanation of what "{indicator}" is
- Its latest (fictional) reported value and what that implies
- How it affects regular consumers or investors
- A conclusion with a mild outlook

Finish with a line citing public data sources like FRED or BLS. No markdown.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a financial writer who explains economics in a casual yet clear style for the U.S. audience."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.72,
            max_tokens=1300
        )

        content = response.choices[0].message.content.strip()
        content += '\n<p style="font-size: 0.9em; color: gray;">Sources: Based on data and trends from FRED, BLS, BEA, and Investopedia summaries.</p>'

        return {
            "title": title,
            "content": content,
            "category": "economy",
            "tags": [
                "US economy", "economic indicators", indicator,
                "inflation", "interest rates", "finance", "FRED", "investment"
            ]
        }

    except Exception as e:
        return {
            "title": f"US Economy Update (Error)",
            "content": f"<p>⚠️ Failed to generate economy post due to: {e}</p>",
            "category": "economy",
            "tags": ["economy", "error"]
        }
