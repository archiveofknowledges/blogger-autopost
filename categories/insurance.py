# categories/insurance.py

import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_insurance_post(post_data):
    topic = post_data.get("insurance_type", "Health Insurance")

    prompt = f"""
Write a detailed, AdSense-friendly blog post targeting U.S. readers about the importance of {topic}. 
Include at least 4–6 paragraphs. Make sure to cover:

- Who needs this insurance type
- How coverage works
- Cost-saving strategies
- When to buy it
- How it protects families or individuals

End with a reliable source, like healthcare.gov. Use a professional and informative tone.
Also return a good title for the blog post.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a professional insurance blogger."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1200
        )

        content = response.choices[0].message.content.strip()
        title = f"{topic} Guide for Americans: What You Must Know"

        tags = [
            "insurance", topic.lower(), "financial protection", "healthcare", 
            "US market", "coverage tips", "insurance savings"
        ]

        return {
            "title": title,
            "content": content,
            "category": "insurance",
            "tags": tags
        }

    except Exception as e:
        return {
            "title": f"{topic} Insurance Overview (Error)",
            "content": f"⚠️ Failed to generate insurance post due to: {e}",
            "category": "insurance",
            "tags": ["insurance", "error"]
        }
