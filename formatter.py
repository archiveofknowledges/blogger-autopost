import openai
import os

from config import OPENAI_MODEL

def format_post(title, summary, body, source=None, topics=None):
    """
    Uses OpenAI to rewrite the post into a polished, AdSense-friendly blog post.
    Returns HTML-formatted content.
    """

    system_prompt = """
You are a professional blog writer creating high-quality, AdSense-optimized posts for an English-speaking audience.

Please format the article using clean HTML structure with the following rules:
- Begin with an <h1> title tag (based on the provided title).
- Add a 1-sentence summary below the title in <p><em>...</em></p> format.
- Use <h2> subheadings to divide content into 2–3 main sections.
- Write short paragraphs (3–5 lines max per paragraph).
- Keep tone professional, informative, and clear (no emojis or overly casual tone).
- Add a <ul> list for comparisons or summaries if appropriate.
- End with a <p><strong>Source:</strong> <a href='...'>...</a></p> if a source is provided.
- Do not repeat the title at the top of the article.
"""

    user_prompt = f"""
Title: {title}
Summary: {summary}
Content:
{body}
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.7
    )

    content = response.choices[0].message.content.strip()

    # Append tag info (optional footer)
    if topics:
        tags = ", ".join(topics)
        content += f"\n\n<p><strong>Tags:</strong> {tags}</p>"

    return content
