# categories/credit_cards.py

import openai
import os
import random

openai.api_key = os.getenv("OPENAI_API_KEY")

TARGET_GROUPS = [
    "Young Professionals looking to build credit",
    "Frequent Travelers who want top-tier travel rewards",
    "Families looking for everyday cash back options",
    "College Students starting their credit journey",
    "People rebuilding credit after a rough patch"
]

def generate_credit_cards_post():
    target = random.choice(TARGET_GROUPS)

    prompt = f"""
Write an AdSense-optimized, informative blog post for U.S. readers about credit card recommendations for: "{target}".
Include 2–3 recommended credit cards (they can be fictional or based on real patterns), explain their benefits, rewards programs, annual fees, and who they’re best for.
Structure the post into 4–6 paragraphs. Add a brief tip on how to choose the right card and how to get approved.
End the post with a note like: "Based on current offers from major U.S. banks and credit card companies as of 2025."
Use a helpful and slightly authoritative tone.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a U.S.-based personal finance blog writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=1200
        )

        content = response.choices[0].message.content.strip()
        title = f"Best Credit Cards for {target}"

        tags = [
            "credit cards", "rewards", "cash back", "travel points",
            "credit building", "finance tips", "U.S. credit system"
        ]

        return {
            "title": title,
            "content": content,
            "category": "credit_cards",
            "tags": tags
        }

    except Exception as e:
        return {
            "title": "Recommended Credit Cards (Error)",
            "content": f"⚠️ Failed to generate credit card post due to: {e}",
            "category": "credit_cards",
            "tags": ["credit cards", "error"]
        }
