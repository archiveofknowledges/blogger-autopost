import openai
import requests
import datetime
import random
import matplotlib.pyplot as plt

# 필요한 API와 키 설정
OPENAI_API_KEY = "your-openai-api-key"
BLOGGER_API_KEY = "your-blogger-api-key"

# 함수 정의
def generate_scholar_post():
    # 학술적 포스트 생성 (OpenAI를 이용하여)
    response = openai.completions.create(
        model="gpt-4-turbo",  # 최신 모델 사용 (gpt-4-turbo)
        prompt="Write an academic blog post based on recent research in AI",
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def generate_economy_post():
    # 경제 지표 포스트 생성 (웹 크롤링 및 분석)
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    data = response.json()
    economy_data = data['rates']
    post = f"Today's economy update: USD to EUR exchange rate is {economy_data['EUR']}."
    return post

def generate_minecraft_post():
    # 마인크래프트 관련 추천 글 생성
    post = "Top Minecraft Mods for 2025"
    mods = ["Mod 1", "Mod 2", "Mod 3"]
    return f"Check out these amazing Minecraft mods: {', '.join(mods)}."

def generate_financial_post():
    # 대출, 세금, 보험 관련 포스트
    post = "Understanding Mortgage Rates and How They Affect You"
    return post

def create_post(title, content, category):
    # 포스트를 생성하는 함수
    post_data = {
        'title': title,
        'content': content,
        'category': category,
        'date': datetime.datetime.now().strftime("%Y-%m-%d")
    }
    
    # Blogger API 사용해서 포스트 업로드
    response = requests.post(
        "https://www.googleapis.com/blogger/v3/blogs/your_blog_id/posts/",
        headers={"Authorization": f"Bearer {BLOGGER_API_KEY}"},
        json=post_data
    )
    
    if response.status_code == 200:
        print(f"Successfully posted: {title}")
    else:
        print(f"Failed to post: {title}, Error: {response.text}")

def main():
    # 각 카테고리별 포스트 생성
    scholar_post = generate_scholar_post()
    economy_post = generate_economy_post()
    minecraft_post = generate_minecraft_post()
    financial_post = generate_financial_post()

    # 포스트 제목 설정
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
