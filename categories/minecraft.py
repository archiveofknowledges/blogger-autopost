import openai
import os
import random

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_minecraft_post():
    topics = [
        "Top 5 Minecraft Mods in 2025",
        "Best Resource Packs for Immersion",
        "Coolest Survival Multiplayer Servers (SMP)",
        "Top 3 Adventure Maps You Must Try",
        "Funniest Mods You Didn’t Know Existed",
        "Best Minecraft Mods for Building & Decoration",
        "Beginner-Friendly Modpacks in CurseForge",
        "What’s Hot on PlanetMinecraft This Month"
    ]
    selected_topic = random.choice(topics)

    prompt = (
        f"You are a Minecraft blogger writing for casual U.S.-based players. Your post should be friendly, energetic, and helpful. "
        f"Topic: '{selected_topic}'. Mention 3–5 cool mods, servers, maps, or packs. Reference CurseForge, PlanetMinecraft, Reddit, or YouTubers. "
        "Write 4–6 fun paragraphs in clean HTML (no Markdown or backticks). Use <h2> for the title, <h3> for subheadings, <p> for text. End with a CTA."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You're a fun Minecraft blogger with a tone like Reddit + YouTube gaming community."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=1300
        )

        full_content = response.choices[0].message.content.strip()

        if "<pre><code" in full_content:
            parts = full_content.split("<pre><code", 1)
            content = parts[0].strip()
            code_block = "<pre><code" + parts[1]
        else:
            content = full_content
            code_block = ""

        return {
            "title": selected_topic,
            "content": content,
            "code": code_block,
            "category": "minecraft",
            "tags": [
                "minecraft", "mods", "resource packs", "servers", "smp",
                "curseforge", "planetminecraft", "1.20+", "community picks"
            ]
        }

    except Exception as e:
        print(f"❌ Error generating minecraft post: {e}")
        return None
