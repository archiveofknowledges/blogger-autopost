# categories/scholar.py

import openai
import os
import random

openai.api_key = os.getenv("OPENAI_API_KEY")

# 무작위 학술 주제 선택 리스트
TOPICS = [
    "transformer models in natural language processing",
    "graph neural networks in biology",
    "quantum computing in cryptography",
    "machine learning in medical imaging",
    "reinforcement learning for robotics",
    "large language models and ethical AI",
    "computer vision in autonomous vehicles",
    "Bayesian optimization in hyperparameter tuning",
    "generative AI for scientific discovery",
    "federated learning in healthcare"
]

def generate_scholar_post():
    topic = random.choice(TOPICS)

    prompt = f"""
Write a detailed academic blog post targeting U.S. readers on the topic: "{topic}".
The post should be 4–6 paragraphs long, well-structured with sections like Introduction, Methodology, Results, and Conclusion.
Use a professional, scholarly tone. Include references to credible sources (e.g., arXiv, Google Scholar) at the end.
Do not use overly technical math. Prioritize clarity and SEO-friendly formatting.
Title should reflect the topic concisely.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an academic blog writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1400
        )

        content = response.choices[0].message.content.strip()
        title = f"Exploring {topic.capitalize()}"

        tags = [
            "AI research", "academic", "machine learning", "deep learning",
            "GPT", topic.split()[0], "US education"
        ]

        return {
            "title": title,
            "content": content,
            "category": "scholar",
            "tags": tags
        }

    except Exception as e:
        return {
            "title": f"AI Research Topic (Error)",
            "content": f"⚠️ Failed to generate post due to: {e}",
            "category": "scholar",
            "tags": ["error", "scholar"]
        }
