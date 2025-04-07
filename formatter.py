import openai
import os
from datetime import datetime
import hashlib

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_tags(summary):
    prompt = f"""Extract 3–5 relevant tags from the following academic summary. Return them as a comma-separated list:

"{summary}"
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    tags_text = response.choices[0].message.content.strip()
    return [tag.strip() for tag in tags_text.split(",") if tag.strip()]

def generate_image_url(title, summary):
    # hash the title to keep image name deterministic
    unique_id = hashlib.md5(title.encode()).hexdigest()
    return f"https://dummyimage.com/600x400/cccccc/000000.png&text={unique_id[:6]}"

def format_post(post_data):
    title = post_data.get("title")
    summary = post_data.get("summary")
    category = post_data.get("category")
    source = post_data.get("source")
    topics = ", ".join(post_data.get("topics", []))
    date = datetime.today().strftime("%Y-%m-%d")

    # 제목 스타일 설정
    if category == "economy":
        post_title = f"{title} ({date})"
    else:
        post_title = title

    # GPT로 전문적인 요약 생성
    prompt = f"""You are a professional blog writer targeting an academic and economic audience in the United States.
Based on the following content, generate a clean and professional blog post in English. Use 1–2 paragraphs. Do not include emojis.

Content:
"{summary}"
"""
    gpt_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    body = gpt_response.choices[0].message.content.strip()

    # GPT 태그 추출
    tags = generate_tags(summary)

    # 이미지 생성 (임시 더미 이미지)
    image_url = generate_image_url(title, summary)

    content_html = f"""
<p><img src="{image_url}" alt="Related visual for the article" style="max-width:100%;"/></p>
<p>{body}</p>
<p><strong>Source:</strong> <a href="{source}" target="_blank">{source}</a></p>
<p><strong>Topics:</strong> {topics}</p>
"""

    return {
        "title": post_title,
        "content": content_html,
        "labels": tags,
        "category": category
    }
