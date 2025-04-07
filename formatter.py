from openai import OpenAI
from datetime import datetime
import re

client = OpenAI()

def generate_post(title, abstract):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional academic blogger. "
                        "Write a clear, well-structured, ad-friendly blog post in English "
                        "based on the paper's title and abstract. "
                        "Keep it concise (1–2 paragraphs), objective, and informative. "
                        "Use minimal emojis, and include bullet points or tables if necessary."
                    )
                },
                {
                    "role": "user",
                    "content": f"Title: {title}\nAbstract: {abstract}"
                }
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("⚠️ GPT 요청 실패: ", e)
        return None


def generate_image(prompt):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return response.data[0].url
    except Exception as e:
        print("⚠️ 이미지 생성 실패: ", e)
        return None


def sanitize_filename(text):
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', text)


def format_post(title, summary, image_url=None):
    now = datetime.utcnow().strftime("%B %d, %Y")

    html = f"<h2>{title}</h2>\n"
    html += f"<p><i>Published: {now}</i></p>\n"
    if image_url:
        html += f'<img src="{image_url}" alt="{title}" style="max-width:100%;"><br/>\n'
    html += f"<div>{summary}</div>\n"

    return html
