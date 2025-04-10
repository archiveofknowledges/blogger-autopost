import openai
import os
import random

openai.api_key = os.getenv("OPENAI_API_KEY")

TOPIC_TYPES = [
    "Top 5 Minecraft Mods in 2025",
    "Best Resource Packs for Immersion",
    "Coolest Survival Multiplayer Servers"
]

def generate_minecraft_post():
    topic = random.choice(TOPIC_TYPES)

    prompt = f"""
You're writing for a Minecraft blog for U.S.-based players. Topic: "{topic}".
Use an upbeat, casual voice. Recommend 3–5 fictional or real mods, maps, or servers.
Use <h2>, <h3>, <p> only. Do not use Markdown. End with a line like "Based on Reddit/YouTube community trends".
Vary sentence/paragraph length for authenticity.
"""

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=1200
    )

    content = response.choices[0].message.content.strip()
    title = topic

    tags = ["minecraft", "mods", "servers", "community", "smp", "2025"]

    return {
        "title": title,
        "content": content,
        "category": "minecraft",
        "tags": tags
    }
