# categories/finance.py

import openai
import os
import random

openai.api_key = os.getenv("OPENAI_API_KEY")

TARGET_GROUPS = [
    "Millennials looking to invest in ETFs",
    "Young professionals starting retirement planning",
    "Families managing monthly household budgets",
    "Seniors preparing for fixed-income retirement",
    "Self-employed individuals seeking tax-efficient investments"
]

def generate_finance_post():
    target = random.choice(TARGET_GROUPS)

    prompt = f"""
Write an informative blog post targeting U.S. readers about smart financial strategies for: "{target}".
Include 2–3 investment or budgeting tips, and mention specific tools, platforms, or institutions (e.g., Fidelity, Vanguard, Robinhood).
Explain each point in a clear, practical way using 4–6 structured paragraphs.
Include a short section on common mistakes to avoid, and close with a recommended next step.
End with a line like: "Source: Based on current trends in U.S. personal finance from 2025 reports by NerdWallet and Investopedia."
Use an accessible but professional tone.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a personal finance advisor writing helpful blog posts for U.S. readers."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.75,
            max_tokens=1300
        )

        content = response.choices[0].message.content.strip()
        title = f"Smart Financial Planning for {target}"

        tags = [
            "finance", "investment", "retirement", "ETFs", "Roth IRA",
            "budgeting", "money management", "personal finance"
        ]

        return {
            "title": title,
            "content": content,
            "category": "finance",
            "tags": tags
        }

    except Exception as e:
        return {
            "title": "Finance Strategy Post (Error)",
            "content": f"⚠️ Failed to generate finance post due to: {e}",
            "category": "finance",
            "tags": ["finance", "error"]
        }
