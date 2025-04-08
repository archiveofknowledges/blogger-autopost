import openai
import requests
import datetime
import random
import matplotlib.pyplot as plt

# 필요한 API와 키 설정
OPENAI_API_KEY = "your-openai-api-key"
BLOGGER_API_KEY = "your-blogger-api-key"
BLOG_ID = "your_blog_id"

# 포스트 생성 함수들

def generate_scholar_post():
    # 학술적 포스트 생성 (OpenAI를 이용하여)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Write an academic blog post based on recent research in AI",
        max_tokens=500,
        temperature=0.7
    )
    post = response.choices[0].text.strip()
    post = f"### Introduction\n{post}\n\n### Conclusion\nThis is a detailed analysis on the topic."
    return post

def generate_economy_post():
    # 경제 지표 포스트 생성 (웹 크롤링 및 분석)
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    data = response.json()
    economy_data = data['rates']
    post = f"Today's economy update: USD to EUR exchange rate is {economy_data['EUR']}.\n\n"
    
    # 시각화 추가 (예: 환율 변동 차트)
    currencies = list(economy_data.keys())[:10]  # 상위 10개 통화
    values = [economy_data[currency] for currency in currencies]
    
    plt.bar(currencies, values)
    plt.xlabel("Currency")
    plt.ylabel("Exchange Rate")
    plt.title("Top 10 Exchange Rates (USD Base)")
    plt.xticks(rotation=45)
    
    # 그래프 저장
    chart_path = "/tmp/economy_chart.png"
    plt.savefig(chart_path)
    post += f"\n\n![Exchange Rates Chart]({chart_path})"
    
    return post

def generate_minecraft_post():
    # 마인크래프트 관련 추천 글 생성
    post = "Top Minecraft Mods for 2025"
    mods = ["Mod 1", "Mod 2", "Mod 3"]
    post += f"\n\nThese mods will enhance your Minecraft experience in 2025. Don't miss out on these amazing mods!"
    
    # 추가 이미지나 유용한 링크 삽입 (애드센스 친화적)
    post += "\n\nFor more information, check out the following resources:\n\n[Learn More About Minecraft Mods](https://www.minecraft.net/)"
    return post

def generate_financial_post():
    # 대출, 세금, 보험 관련 포스트
    post = "Understanding Mortgage Rates and How They Affect You"
    post += "\n\nThis post will break down the concept of mortgage rates and provide tips on how to choose the best options for your financial situation."
    
    # 애드센스 친화적인 링크 삽입
    post += "\n\nFor the best mortgage rates, visit [Best Mortgage Rates](https://www.example.com/mortgage-rates)."
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
        f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/",
        headers={"Authorization": f"Bearer {BLOGGER_API_KEY}"},
        json=post_data
    )
    
    if response.status_code == 200:
        print(f"Successfully posted: {title}")
    else:
        print(f"Failed to post: {title}, Error: {response.text}")

def schedule_posts():
    # 카테고리별 포스트 생성 및 스케줄링
    # 학술적 포스트 10개
    scholar_posts = [generate_scholar_post() for _ in range(10)]
    
    # 경제 지표 포스트 1개
    economy_post = generate_economy_post()
    
    # 마인크래프트 관련 포스트 1개
    minecraft_post = generate_minecraft_post()
    
    # 금융 관련 포스트 1개
    financial_post = generate_financial_post()

    # 포스트 제목 설정
    posts = [
        {"title": "AI Research Trends", "content": random.choice(scholar_posts), "category": "Scholar"},
        {"title": f"Economy Update [{datetime.datetime.now().strftime('%d.%m.%y')}]", "content": economy_post, "category": "Economy"},
        {"title": "Top Minecraft Mods for 2025", "content": minecraft_post, "category": "Minecraft"},
        {"title": "Understanding Mortgage Rates", "content": financial_post, "category": "Financial"}
    ]

    for post in posts:
        create_post(post["title"], post["content"], post["category"])

def main():
    # 자동으로 포스트를 생성하고 업로드하는 함수 호출
    schedule_posts()

if __name__ == "__main__":
    main()
