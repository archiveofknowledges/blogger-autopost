import importlib
import datetime
import os
import requests
import random

# Secrets
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
BLOG_ID = "2146078384292830084"

# 카테고리별 포스트 수
CATEGORY_CONFIG = {
    "scholar": 10,
    "economy": 1,
    "minecraft": 3,
    "credit_cards": 1,
    "finance": 1,
    "insurance": 1
}

# 토큰 요청
def get_access_token():
    try:
        response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "refresh_token": REFRESH_TOKEN,
                "grant_type": "refresh_token",
            }
        )

        # 디버깅용 출력 (구글 응답 본문 전체 확인)
        print("🔍 Raw response from Google:")
        print(response.status_code)
        print(response.text)

        response.raise_for_status()
        return response.json()["access_token"]
    except Exception as e:
        print(f"❌ Error getting access token: {e}")
        return None


# 포스트 업로드
def create_post(title, content, category, access_token):
    post_data = {
        "title": title,
        "content": content,
        "labels": [category]
    }

    try:
        response = requests.post(
            f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            json=post_data
        )

        if response.status_code == 200:
            print(f"✅ Posted: {title}")
        else:
            print(f"❌ Failed: {title} → {response.text}")
    except Exception as e:
        print(f"❌ Error posting '{title}': {e}")

# 더미 post_data 자동 생성 (테스트용 또는 실제 추후 모듈 대체 가능)
def generate_dummy_data(category):
    if category == "scholar":
        return {
            "paper_title": f"Deep Learning Approach {random.randint(100,999)}",
            "study_topic": "AI",
            "intro": "This paper explores recent advancements in AI.",
            "literature_review": "Several studies have contributed to this domain...",
            "methodology": "We used a CNN-based architecture with augmentation.",
            "results_and_discussion": "The model achieved 98.7% accuracy...",
            "conclusion": "Further research can improve robustness.",
            "references": "Doe et al. (2023), Smith et al. (2024)"
        }
    elif category == "economy":
        return {"summary": "Today's inflation report shows a mild slowdown."}
    elif category == "minecraft":
        return {"mods": ["OptiFine", "Create", "Twilight Forest"]}
    elif category == "credit_cards":
        return {"card_name": "Platinum Plus", "benefits": "Travel rewards & Cashback"}
    elif category == "finance":
        return {"topic": "ETF vs Mutual Fund", "explanation": "Here’s how they differ..."}
    elif category == "insurance":
        return {"type": "Health Insurance", "tips": "Compare deductibles and coverage"}
    else:
        return {}

# 메인 루프
def main():
    access_token = get_access_token()
    if not access_token:
        print("❌ Cannot continue: access token fetch failed.")
        return

    for category, count in CATEGORY_CONFIG.items():
        try:
            module = importlib.import_module(f"categories.{category}")
            function_name = f"generate_{category}_post"
            generate_func = getattr(module, function_name)

            for _ in range(count):
                post_data = generate_dummy_data(category)
                post = generate_func(post_data)
                create_post(post["title"], post["content"], category, access_token)

        except Exception as e:
            print(f"❌ Error in category '{category}': {e}")

if __name__ == "__main__":
    main()
