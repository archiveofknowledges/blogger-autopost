import openai
import os
import base64
import requests

from config import OPENAI_MODEL

def safe_openai_request(messages):
    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ GPT 요청 실패: {e}")
        return f"<p><em>⚠️ Failed to generate content due to an error: {str(e)}</em></p>"

def generate_image(prompt):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response["data"][0]["url"]
        return image_url
    except Exception as e:
        print(f"⚠️ 이미지 생성 실패: {e}")
        return None

def format_post(title, summary, body, source=None, topics=None):
    """
    Generates an AdSense-optimized blog post with HTML formatting, GPT fallback, and image insertion.
    """

    # System prompt for AdSense-style formatting
    system_prompt = """
You are a professional blog writer creating high-quality, AdSense-optimized posts for an English-speaking audience.

Format the article using clean HTML structure:
- <h1> for title
- <p><em>...</em></p> summary
- <h2> for each section (2–3 sections max)
- Short paragraphs (3–5 lines max)
- <ul> lists if useful
- <p><strong>Source:</strong> <a href='...'>...</a></p> at the end if applicable
- Keep the tone professional and informative (no emojis or casual slang).
"""

    # Combine message
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

    # Get GPT content (with exception handling)
    content = safe_openai_request(messages)

    # Get related image
    image_url = generate_image(title)
    if image_url:
        image_html = f"<p><img src='{image_url}' alt='Related image' style='max-width:100%; height:auto; border-radius:12px;'></p>\n"
        content = image_html + content

    # Append tags if available
    if topics:
        tags = ", ".join(topics)
        content += f"\n\n<p><strong>Tags:</strong> {tags}</p>"

    return content
