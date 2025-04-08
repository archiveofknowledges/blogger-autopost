# categories/minecraft.py

import openai
import os
import random

openai.api_key = os.getenv("OPENAI_API_KEY")

TOPIC_TYPES = [
    "Top 5 Minecraft Mods in 2025",
    "Best Resource Packs for Immersion",
    "Coolest Survival Multiplayer Servers (SMP)",
    "Top 3 Adventure Maps You Must Try",
    "Funniest Mods You Didn’t Know Existed",
    "Best Minecraft Mods for Building & Decoration",
    "Beginner-Friendly Modpacks in CurseForge",
    "What’s Hot on PlanetMinecraft This Month"
]

def generate_minecraft_post():
    topic = random.choice(TOPIC_TYPES)

    prompt = f"""
Write a friendly and engaging Minecraft blog post targeting U.S.-based players. Topic: "{topic}".
Use an energetic, casual tone. Recommend 3–5 specific mods, servers, maps, or resource packs (fictional or inspired by real ones).
Mention platforms like CurseForge, PlanetMinecraft, or popular YouTubers where appropriate.
Use 4–6 short paragraphs. Include at least one call to action at the end.
End with something like “source: based on community trends from Reddit and YouTube”.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a Minecraft blogger writing for casual players in the U.S."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=1100
        )

        content = response.choices[0].message.content.strip()
        title = topic

        tags = [
            "minecraft", "mods", "resource packs", "servers", "smp", 
            "curseforge", "planetminecraft", "1.20+", "community picks"
        ]

        return {
            "title": title,
            "content": content,
            "category": "minecraft",
            "tags": tags
        }

    except Exception as e:
        return {
            "title": "Minecraft Fun Post (Error)",
            "content": f"⚠️ Failed to generate minecraft post due to: {e}",
            "category": "minecraft",
            "tags": ["minecraft", "error"]
        }
