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
    response = openai.Completion.create(
        engine="text-davinci-003",
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
    tags = generate_tags(content, category)  # 태그 생성

    post_data = {
        'title': title,
        'content': content,
        'category': category,
        'tags': tags,  # 태그 추가
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

def generate_tags(content, category):
    """
    자동으로 태그를 생성하는 함수
    카테고리와 내용에 맞춰 태그를 생성
    """
    # 기본 태그 목록 (카테고리별로 다르게 설정할 수 있음)
    tags = []

    # 학술적 포스트의 경우
    if category == "Scholar":
        tags = ["AI", "Machine Learning", "Research", "Innovation", "Technology"]

    # 경제 포스트의 경우
    elif category == "Economy":
        tags = ["Economy", "Finance", "Market", "Currency", "Global"]

    # 마인크래프트 포스트의 경우
    elif category == "Minecraft":
        tags = ["Minecraft", "Mods", "Gaming", "Minecraft Server", "Resource Packs"]

    # 금융 포스트의 경우
    elif category == "Financial":
        tags = ["Mortgage", "Loan", "Taxes", "Investment", "Interest Rates"]

    # 기본적으로 내용에서 키워드 추출 (간단한 방법으로 첫 몇 단어를 태그로 추가)
    words = content.split()
    if len(words) > 4:
        for word in words[:5]:  # 첫 5개 단어를 태그로 추가
            if word.lower() not in tags:
                tags.append(word.capitalize())

    return tags[:6]  # 태그는 최대 6개

def main():
    # 각 카테고리별 포스트 생성
    scholar_posts = [generate_scholar_post() for _ in range(10)]  # 학술적 포스트 10개
    economy_posts = [generate_economy_post() for _ in range(1)]  # 경제 지표 포스트 1개
    minecraft_posts = [generate_minecraft_post() for _ in range(3)]  # 마인크래프트 포스트 3개
    financial_posts = [generate_financial_post() for _ in range(3)]  # 금융 관련 포스트 3개

    # 포스트 제목 설정
    posts = [
        {"title": f"AI Research Trends {i+1}", "content": random.choice(scholar_posts), "category": "Scholar"} for i in range(10)
    ] + [
        {"title": f"Economy Update [{datetime.datetime.now().strftime('%d.%m.%y')}] {i+1}", "content": post, "category": "Economy"} for i, post in enumerate(economy_posts)
    ] + [
        {"title": f"Top Minecraft Mods {i+1} for 2025", "content": post, "category": "Minecraft"} for i, post in enumerate(minecraft_posts)
    ] + [
        {"title": f"Understanding Mortgage Rates {i+1}", "content": post, "category": "Financial"} for i, post in enumerate(financial_posts)
    ]

    # 모든 포스트 업로드
    for post in posts:
        create_post(post["title"], post["content"], post["category"])

if __name__ == "__main__":
    main()
