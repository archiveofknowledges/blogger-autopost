import openai
import requests
import datetime
import random
import matplotlib.pyplot as plt
import os

# API 키는 환경변수 또는 GitHub Secrets에서 불러오는 게 보안상 안전
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key")
BLOGGER_API_KEY = os.getenv("BLOGGER_API_KEY", "your-blogger-api-key")

# OpenAI 클라이언트 설정
openai.api_key = OPENAI_API_KEY

# 학술적 포스트 생성 (OpenAI ChatCompletion API)
def generate_scholar_post():
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a professional academic blog writer."},
                {"role": "user", "content": "Write a detailed academic blog post based on recent research in AI."}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating scholar post: {e}")
        return "Failed to generate scholar post."

# 경제 지표 포스트 생성
def generate_economy_post():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        economy_data = data['rates']
        post = f"Today's economy update: USD to EUR exchange rate is {economy_data['EUR']}."
        return post
    except Exception as e:
        print(f"Error generating economy post: {e}")
        return "Failed to generate economy post."

# 마인크래프트 추천 글
def generate_minecraft_post():
    mods = ["OptiFine", "Biomes O' Plenty", "JourneyMap", "Tinkers' Construct"]
    return f"Check out these amazing Minecraft mods: {', '.join(mods)}."

# 대출/보험 관련 포스트
def generate_financial_post():
    return "Understanding Mortgage Rates and How They Affect You. Learn how interest rates impact your monthly payments and long-term costs."

# 블로그 포스트 생성 및 업로드
def create_post(title, content, category):
    post_data = {
        'title': title,
        'content': content,
        'category': category,
        'date': datetime.datetime.now().strftime("%Y-%m-%d")
    }

    try:
        response = requests.post(
            "https://www.googleapis.com/blogger/v3/blogs/your_blog_id/posts/",
            headers={"Authorization": f"Bearer {BLOGGER_API_KEY}"},
            json=post_data
        )

        if response.status_code == 200:
            print(f"✅ Successfully posted: {title}")
        else:
            print(f"❌ Failed to post: {title}, Error: {response.text}")
    except Exception as e:
        print(f"Error posting to Blogger: {e}")

# 메인 실행 함수
def main():
    scholar_post = generate_scholar_post()
    economy_post = generate_economy_post()
    minecraft_post = generate_minecraft_post()
    financial_post = generate_financial_post()

    posts = [
        {"title": "AI Research Trends", "content": scholar_post, "category": "Scholar"},
        {"title": f"Economy Update [{datetime.datetime.now().strftime('%d.%m.%y')}]", "content": economy_post, "category": "Economy"},
        {"title": "Top Minecraft Mods for 2025", "content": minecraft_post, "category": "Minecraft"},
        {"title": "Understanding Mortgage Rates", "content": financial_post, "category": "Financial"}
    ]

    for post in posts:
        create_post(post["title"], post["content"], post["category"])

if __name__ == "__main__":
    main()
