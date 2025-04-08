import os
import datetime
import requests
import openai
from categories import scholar
from categories import html

# ✅ 환경변수
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")
openai.api_key = os.environ.get("OPENAI_API_KEY")
BLOG_ID = "2146078384292830084"

# ✅ Blogger Access Token 발급
def get_access_token():
    if not (CLIENT_ID and CLIENT_SECRET and REFRESH_TOKEN):
        print("❌ Missing CLIENT_ID / CLIENT_SECRET / REFRESH_TOKEN")
        return None

    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }

    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print("✅ Access token received")
        return access_token
    else:
        print("❌ Failed to get access token:", response.text)
        return None

# ✅ Blogger 포스트 업로드
def create_post(title, content, category, tags):
    access_token = get_access_token()
    if not access_token:
        print("❌ Cannot post without access token.")
        return

    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    post_data = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
        "labels": [category] + tags
    }

    response = requests.post(url, headers=headers, json=post_data)
    if response.status_code == 200:
        print(f"✅ Posted: {title}")
    else:
        print(f"❌ Failed: {title} → {response.text}")

# ✅ main(): scholar + html 1개씩 테스트
def main():
    print("🚀 Starting test post: scholar + html (no delay)")

    scholar_post = scholar.generate_scholar_post()
    create_post(
        title=scholar_post["title"],
        content=scholar_post["content"],
        category=scholar_post["category"],
        tags=scholar_post["tags"]
    )

    html_post = html.generate_html_post()
    create_post(
        title=html_post["title"],
        content=html_post["content"],
        category=html_post["category"],
        tags=html_post["tags"]
    )

if __name__ == "__main__":
    main()
