from openai import OpenAI
import re

client = OpenAI()

def generate_post(title, abstract):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional academic blogger. Write a well-structured, professional blog post summarizing the given paper abstract in one to two paragraphs. Use markdown formatting where appropriate. Avoid emojis. Target an audience in the United States."
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

def format_post(title, abstract):
    body = generate_post(title, abstract)
    if not body:
        return None

    image_url = generate_image(f"Conceptual illustration for: {title}")
    image_html = f'<img src="{image_url}" alt="{title}" style="max-width:100%;">' if image_url else ""

    full_content = f"""
<h2>{title}</h2>
{image_html}
<div>{body}</div>
"""

    return {
        "title": title,
        "content": full_content
    }

def extract_tags(text):
    # 간단한 키워드 추출 (태그 자동화)
    keywords = re.findall(r'\b[A-Za-z]{4,}\b', text)
    common = set([
        "abstract", "paper", "study", "result", "data", "model", "method",
        "introduction", "conclusion", "research", "analysis", "system"
    ])
    tags = [kw.lower() for kw in set(keywords) if kw.lower() not in common]
    return sorted(tags)[:10]
