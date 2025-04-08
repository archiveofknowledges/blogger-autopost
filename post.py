import importlib
import datetime
import os
import requests
import time

# GitHub Secrets → 환경변수
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
BLOG_ID = "2146078384292830084"

# 카테고리별 자동 포스팅 개수
CATEGORY_CONFIG = {
    "scholar": 10,
    "economy": 1,
    "minecraft": 3,
    "credit_cards": 1,
    "finance": 1,
    "insurance": 1
}

# Blogger Access Token 발급
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
        print("🔍 Google Auth:", response.status_code)
        print(response.text)
        response.raise_for_status()
        return response.json()["access_token"]
    except Exception as e:
        print(f"❌ Access Token Error: {e}")
        return None

# Blogger에 포스트 업로드
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
        print(f"❌ Blogger API Error: {e}")

# 메인 실행
def main():
    access_token = get_access_token()
    if not access_token:
        print("❌ Cannot proceed without access token.")
        return

    for category, count in CATEGORY_CONFIG.items():
        try:
            module = importlib.import_module(f"categories.{category}")
            generate_func = getattr(module, f"generate_{category}_post")

            for _ in range(count):
                post = generate_func()
                create_post(post, access_token)
                time.sleep(2)  # rate limit 대비

        except Exception as e:
            print(f"❌ Error in category '{category}': {e}")

if __name__ == "__main__":
    main()
