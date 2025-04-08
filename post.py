import importlib
import datetime
import os
import requests
import random
import time

# 환경변수: GitHub Secrets 기준
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
BLOG_ID = "2146078384292830084"

# 카테고리별 포스트 수 설정
CATEGORY_CONFIG = {
    "scholar": 10,
    "economy": 1,
    "minecraft": 3,
    "credit_cards": 1,
    "finance": 1,
    "insurance": 1
}

# ENV 디버깅
print("🔎 ENV CHECK")
print("CLIENT_ID:", CLIENT_ID[:4] if CLIENT_ID else "❌ Missing")
print("CLIENT_SECRET:", CLIENT_SECRET[:4] if CLIENT_SECRET else "❌ Missing")
print("REFRESH_TOKEN:", REFRESH_TOKEN[:4] if REFRESH_TOKEN else "❌ Missing")

# Google Access Token 발급
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

        print("🔍 Raw response from Google:")
        print(response.status_code)
        print(response.text)

        response.raise_for_status()
        return response.json()["access_token"]
    except Exception as e:
        print(f"❌ Error getting access token: {e}")
        return None

# Blogger 포스트 업로드
def create_post(post, access_token):
    post_data = {
        "title": post["title"],
        "content": post["content"],
        "labels": [post["category"]] + post.get("tags", [])
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
            print(f"✅ Posted: {post['title']}")
        else:
            print(f"❌ Failed: {post['title']} → {response.text}")
    except Exception as e:
        print(f"❌ Error posting '{post['title']}': {e}")

# 더미 post_data 생성 (기본 구조 + 내용 샘플은 각 모듈에서)
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
        return {
            "indicator_name": "Consumer Price Index",
            "indicator_value": "3.2%",
            "summary": "Inflation is showing early signs of cooling down this quarter."
        }
    elif category == "minecraft":
        return {
            "year": 2025,
            "mods": ["OptiFine", "Create", "Twilight Forest"],
            "category": "Visual + Exploration"
        }
    elif category == "credit_cards":
        return {
            "card_name": "Platinum Plus",
            "benefits": "5% cashback on groceries, travel insurance included",
            "issuer": "Bank of GPT",
            "target_audience": "Young professionals"
        }
    elif category == "finance":
        return {
            "topic": "Retirement Planning",
            "target_group": "Millennials",
            "advice": "Start early with a Roth IRA and low-fee index funds.",
            "recommended_plan": "Fidelity Growth Fund"
        }
    elif category == "insurance":
        return {
            "insurance_type": "Health Insurance",
            "coverage": "Inpatient + outpatient + dental",
            "tips": "Compare premiums vs. deductibles to find your ideal balance.",
            "source": "Healthcare.gov"
        }
    else:
        return {}

# 메인 실행 함수
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

                # 제목이 중복되지 않도록 타임스탬프나 숫자 추가
                now = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
                if "unique" not in post["title"].lower():
                    post["title"] = f"{post['title']} ({now})"

                create_post(post, access_token)
                time.sleep(2)  # rate limit 대응

        except Exception as e:
            print(f"❌ Error in category '{category}': {e}")

if __name__ == "__main__":
    main()
