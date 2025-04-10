import openai
import os
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

TOPIC_TYPES = [
    "Top 5 Minecraft Mods in 2025",
    "Best Resource Packs for Immersion",
    "Coolest Survival Multiplayer Servers (SMP)",
    "Top 3 Adventure Maps You Must Try",
    "Funniest Mods You Didn’t Know Existed",
    "Best Minecraft Mods for Building & Decoration",
    "Beginner-Friendly Modpacks in CurseForge",
    "What’s Hot on PlanetMinecraft This Month",
    "Most Popular Mods Among YouTubers Right Now",
    "Top Redstone Creations That Blew Our Minds"
]

def generate_minecraft_post():
    topic = random.choice(TOPIC_TYPES)

    prompt = f"""
Write a blog post for U.S.-based Minecraft players. Topic: "{topic}".
Use a casual, community-style tone like you'd find on Reddit or a fan blog.
Use HTML tags only. Avoid Markdown or backticks.
Structure with <h2> for title, <h3> for subheadings, and <p> for body text.
Mention 3–5 specific mods, maps, or servers (can be fictional or realistic).
Include platforms like CurseForge or PlanetMinecraft. Reference at least one YouTuber.
End with a source line like "Based on Minecraft community trends from Reddit and YouTube".
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a Minecraft blogger writing for casual U.S. players."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.85,
            max_tokens=1100
        )

        content = response.choices[0].message.content.strip()

        content += '<p style="font-size: 0.9em; color: gray;">Source: Based on Minecraft community trends from Reddit and YouTube.</p>'

        return {
            "title": topic,
            "content": content,
            "category": "minecraft",
            "tags": [
                "minecraft", "mods", "resource packs", "servers", "smp",
                "curseforge", "planetminecraft", "community", "1.20+", "trending"
            ]
        }

    except Exception as e:
        return {
            "title": "Minecraft Post (Error)",
            "content": f"<p>⚠️ Failed to generate Minecraft post due to: {e}</p>",
            "category": "minecraft",
            "tags": ["minecraft", "error"]
        }
