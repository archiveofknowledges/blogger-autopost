from openai import OpenAI
import os
from datetime import datetime
import hashlib

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# GPT를 이용해 태그 자동 생성
def generate_tags(summary):
    prompt = f"""Extract 3–5 relevant tags from the following academic summary. Return them as a comma-separated list:

"{summary}"
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    tags_text = response.choices[0].message.content.strip()
    return [tag.strip() for tag in tags_text.split(",") if tag.strip()]

# 논문 주제 기반 이미지 URL 생성 (더미 이미지)
def generate_image_url(title, summary):
    unique_id = hashlib.md5(title.encode()).hexdigest()
    return f"https://dummyimage.com/600x400/cccccc/000000.png&text={unique_id[:6]}"

# 블로그 포스트 포맷팅
def format_post(post_data):
    title = post_data.get("title")
    summary = post_data.get("summary")
    category = post_data.get("category")
    source = post_data.get("source")
    topics = ", ".join(post_data.get("topics", []))
    date = datetime.today().strftime("%Y-%m-%d")

    # 포스트 제목 구성
    if category == "economy":
        post_title = f"{title} ({date})"
    else:
        post_title = title

    # GPT에게 본문 작성 요청
    prompt = f"""You are a professional blog writer targeting an academic and economic audience in the United States.
Based on the following content, generate a clean and professional blog post in English. Use 1–2 paragraphs. Do not include emojis.

Content:
"{summary}"
"""
    gpt_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    body = gpt_response.choices[0].message.content.strip()

    # 태그 및 이미지 생성
    tags = generate_tags(summary)
    image_url = generate_image_url(title, summary)

    # 최종 HTML 구성
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
