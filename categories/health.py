import openai
import random
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

medical_fields = {
    "Orthopedics": ["Knee Pain", "Back Pain"],
    "Internal Medicine": ["Diabetes", "High Blood Pressure"],
    "Dermatology": ["Acne", "Eczema"],
    "Cardiology": ["Heart Disease", "Arrhythmia"]
}

def generate_health_post():
    field = random.choice(list(medical_fields.keys()))
    topic = random.choice(medical_fields[field])

    prompt = f"""
You are a health blogger. Write a helpful and natural-sounding blog post in HTML on "{topic}" under "{field}".
Include <h3> for sections, <p> for paragraphs. Do not use Markdown or backticks.
Use friendly language and vary sentence length. End with practical advice.
"""

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.75,
        max_tokens=1200
    )

    content = response.choices[0].message.content.strip()
    title = f"{topic}: Causes, Symptoms, and What You Can Do"

    tags = [field.lower(), topic.lower(), "health", "wellness", "medical"]

    return {
        "title": title,
        "content": content,
        "category": "health",
        "tags": tags
    }
